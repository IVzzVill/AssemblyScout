"""Filtro de seguridad de corto alcance para la base simulada."""

import json
import math
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String


class SafetyGate(Node):
    """Conserva un único publicador hacia el control diferencial."""

    def __init__(self):
        super().__init__('safety_gate')
        self.declare_parameter('input_topic', '/assemblyscout/cmd_vel_raw')
        self.declare_parameter('output_topic', '/assemblyscout/cmd_vel')
        self.declare_parameter('stop_distance', 0.20)
        self.declare_parameter('slow_distance', 0.60)
        self.declare_parameter('detection_distance', 0.65)
        self.declare_parameter('side_stop_distance', 0.18)
        self.declare_parameter('sensor_timeout_sec', 0.50)
        self.declare_parameter('command_timeout_sec', 0.50)

        self.command = Twist()
        self.command_time = None
        self.ranges = {'front': None, 'left': None, 'right': None}
        self.range_times = {'front': None, 'left': None, 'right': None}

        self.create_subscription(
            Twist, self.get_parameter('input_topic').value,
            self.command_callback, 10)
        for name in self.ranges:
            self.create_subscription(
                LaserScan, f'/assemblyscout/range/{name}/scan',
                lambda message, sensor=name: self.scan_callback(sensor, message), 10)

        self.publisher = self.create_publisher(
            Twist, self.get_parameter('output_topic').value, 10)
        # Contrato de estado reutilizable por la interfaz, el registro y el
        # futuro sensor físico. El contenido usa el esquema JSON v1.
        self.status_publisher = self.create_publisher(
            String, '/assemblyscout/safety/status', 10)
        self.create_timer(0.05, self.publish_safe_command)
        self.last_status = None
        self.get_logger().info(
            'Filtro activo: el frente reduce o detiene el avance; los laterales informan proximidad.')

    def command_callback(self, message):
        self.command = message
        self.command_time = time.monotonic()

    def scan_callback(self, sensor, message):
        valid = [value for value in message.ranges if math.isfinite(value)]
        self.ranges[sensor] = min(valid) if valid else math.inf
        self.range_times[sensor] = time.monotonic()

    def fresh_distance(self, sensor, now):
        stamp = self.range_times[sensor]
        timeout = self.get_parameter('sensor_timeout_sec').value
        if stamp is None or now - stamp > timeout:
            return None
        return self.ranges[sensor]

    def sensor_state(self, sensor, distance):
        """Clasifica una lectura sin depender de la orden de movimiento."""
        if distance is None:
            return 'unknown'
        if sensor == 'front':
            if distance <= self.get_parameter('stop_distance').value:
                return 'blocked'
            if distance <= self.get_parameter('detection_distance').value:
                return 'caution'
            return 'free'
        if distance <= self.get_parameter('side_stop_distance').value:
            return 'blocked'
        if distance <= self.get_parameter('detection_distance').value:
            return 'caution'
        return 'free'

    def publish_sensor_status(self, now, distances):
        """Publica telemetría lista para visualizar o registrar por eventos."""
        sensors = {}
        for name, distance in distances.items():
            # LaserScan usa infinito cuando el sensor funciona, pero no tiene
            # un obstáculo dentro de su alcance. JSON no admite Infinity: se
            # conserva esa diferencia mediante has_reading e in_range.
            has_reading = distance is not None
            in_range = has_reading and math.isfinite(distance)
            sensors[name] = {
                'min_distance_m': distance if in_range else None,
                'has_reading': has_reading,
                'in_range': in_range,
                'state': self.sensor_state(name, distance),
            }
        payload = {
            'schema': 'assemblyscout.sensor_state.v1',
            'stamp_monotonic_s': round(now, 3),
            'source': 'laser_scan',
            'thresholds_m': {
                'front_stop': self.get_parameter('stop_distance').value,
                'front_caution': self.get_parameter('slow_distance').value,
                'detection': self.get_parameter('detection_distance').value,
                'side_stop': self.get_parameter('side_stop_distance').value,
            },
            'sensors': sensors,
        }
        self.status_publisher.publish(String(data=json.dumps(payload)))

    def publish_safe_command(self):
        now = time.monotonic()
        result = Twist()
        front = self.fresh_distance('front', now)
        left = self.fresh_distance('left', now)
        right = self.fresh_distance('right', now)
        self.publish_sensor_status(now, {
            'front': front,
            'left': left,
            'right': right,
        })

        command_timeout = self.get_parameter('command_timeout_sec').value
        if self.command_time is None or now - self.command_time > command_timeout:
            self.publisher.publish(result)
            return

        result = self.command
        stop = self.get_parameter('stop_distance').value
        slow = self.get_parameter('slow_distance').value
        status = 'libre'

        # Sin medición frontal vigente no se autoriza el avance: falla segura.
        if result.linear.x > 0.0:
            if front is None or front <= stop:
                result.linear.x = 0.0
                status = 'alto frontal'
            elif front < slow:
                result.linear.x *= (front - stop) / (slow - stop)
                status = 'avance reducido'

        self.publisher.publish(result)
        if status != self.last_status:
            self.get_logger().info(f'Seguridad: {status}')
            self.last_status = status


def main(args=None):
    rclpy.init(args=args)
    node = SafetyGate()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.publisher.publish(Twist())
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()
