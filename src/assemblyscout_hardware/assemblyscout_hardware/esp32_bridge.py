"""Puente ROS 2 para la base física controlada por ESP32.

En ``dry_run`` registra el protocolo que se enviará, permitiendo validar el
flujo PS4 -> safety_gate -> puente físico sin una Raspberry conectada.
"""

import json
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import Range
from std_msgs.msg import String

from .protocol import command_line, parse_state


class Esp32Bridge(Node):
    """Entrega órdenes de velocidad al ESP32 y publica telemetría física."""

    def __init__(self):
        super().__init__('esp32_bridge')
        self.declare_parameter('transport', 'dry_run')
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('command_topic', '/assemblyscout/cmd_vel')
        self.declare_parameter('max_linear_mps', 0.15)
        self.declare_parameter('max_angular_radps', 0.70)
        self.declare_parameter('command_timeout_sec', 0.50)

        self.transport_name = self.get_parameter('transport').value
        self.serial = None
        self.sequence = 0
        self.last_command = Twist()
        self.last_command_time = None
        self.last_wire_line = None

        self.status_publisher = self.create_publisher(
            String, '/physical/bridge/status', 10)
        self.state_publisher = self.create_publisher(
            String, '/physical/esp32_state', 10)
        self.range_publishers = {
            name: self.create_publisher(Range, f'/physical/range/{name}', 10)
            for name in ('front', 'left', 'right')
        }
        self.create_subscription(
            Twist,
            self.get_parameter('command_topic').value,
            self.command_callback,
            10,
        )
        self.create_timer(0.05, self.exchange)
        self.open_transport()

    def open_transport(self):
        """Abre serial solo en la Raspberry; dry_run no depende de hardware."""
        if self.transport_name == 'dry_run':
            self.publish_status('Modo local: se valida el protocolo sin ESP32.')
            return
        if self.transport_name != 'serial':
            raise ValueError('transport debe ser dry_run o serial')
        try:
            import serial  # pyserial se instala únicamente en la Raspberry.
            self.serial = serial.Serial(
                self.get_parameter('serial_port').value,
                self.get_parameter('baudrate').value,
                timeout=0.0,
            )
            self.publish_status('Puerto serial ESP32 conectado.')
        except Exception as error:  # Se reporta como estado ROS, no se mueve nada.
            self.publish_status(f'No se abrió el ESP32: {error}')
            self.get_logger().error(f'No se abrió el ESP32: {error}')

    def command_callback(self, message):
        self.last_command = message
        self.last_command_time = time.monotonic()

    def clamp_command(self):
        """Limita el primer movimiento físico a una velocidad conservadora."""
        result = Twist()
        now = time.monotonic()
        timeout = self.get_parameter('command_timeout_sec').value
        if self.last_command_time is None or now - self.last_command_time > timeout:
            return result
        linear_limit = self.get_parameter('max_linear_mps').value
        angular_limit = self.get_parameter('max_angular_radps').value
        result.linear.x = max(-linear_limit, min(linear_limit, self.last_command.linear.x))
        result.angular.z = max(-angular_limit, min(angular_limit, self.last_command.angular.z))
        return result

    def exchange(self):
        command = self.clamp_command()
        self.sequence += 1
        wire_line = command_line(command.linear.x, command.angular.z, self.sequence)
        self.last_wire_line = wire_line
        if self.serial is not None:
            self.serial.write(wire_line.encode('utf-8'))
            self.read_serial()
        elif self.transport_name == 'dry_run' and self.sequence % 20 == 0:
            self.get_logger().info(f'ESP32 simulado recibe: {wire_line.strip()}')

    def read_serial(self):
        """Procesa todas las líneas completas disponibles del ESP32."""
        while self.serial is not None and self.serial.in_waiting:
            raw = self.serial.readline().decode('utf-8', errors='replace').strip()
            if not raw:
                continue
            try:
                self.publish_state(parse_state(raw))
            except (ValueError, json.JSONDecodeError) as error:
                self.get_logger().warning(f'Telemetría ESP32 ignorada: {error}')

    def publish_state(self, state):
        self.state_publisher.publish(String(data=json.dumps(state, sort_keys=True)))
        for name in ('front', 'left', 'right'):
            if name + '_m' not in state:
                continue
            message = Range()
            message.header.stamp = self.get_clock().now().to_msg()
            message.header.frame_id = f'physical_{name}_range'
            message.radiation_type = Range.INFRARED
            message.field_of_view = 0.47
            message.min_range = 0.03
            message.max_range = 2.00
            message.range = state[name + '_m'] if state[name + '_m'] is not None else float('inf')
            self.range_publishers[name].publish(message)

    def publish_status(self, text):
        self.status_publisher.publish(String(data=text))

    def destroy_node(self):
        if self.serial is not None:
            self.serial.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = Esp32Bridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
