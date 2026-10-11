# Importa ROS 2 y los mensajes del control y de velocidad
import math
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


class PS4Teleop(Node):
    def __init__(self):
        # Asigna el nombre del nodo
        super().__init__('ps4_teleop')

        # Define los ejes utilizados y los límites configurables
        self.declare_parameter('axis_forward', 5)
        self.declare_parameter('axis_reverse', 4)
        self.declare_parameter('axis_angular', 2)
        self.declare_parameter('max_linear', 1.5)
        self.declare_parameter('max_angular', 1.5)
        self.declare_parameter('timeout_sec', 0.5)

        # Guarda la última lectura y su momento de recepción
        self.last_axes = None
        self.last_received = None
        self.last_log = 0.0

        # Publica las velocidades para la tortuga
        self.publisher_ = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10
        )

        # Recibe las entradas del control PS4
        self.subscription_ = self.create_subscription(
            Joy, '/joy', self.joy_callback, 10
        )

        # Actualiza las órdenes veinte veces por segundo
        self.timer_ = self.create_timer(0.05, self.publish_velocity)
        self.get_logger().info(
            'R2 avanza, L2 retrocede y el stick derecho controla el giro'
        )

    def joy_callback(self, msg):
        # Descarta mensajes con valores no válidos
        if not msg.axes or not all(math.isfinite(v) for v in msg.axes):
            self.last_axes = None
            self.last_received = None
            return

        # Guarda los ejes recibidos y el momento de llegada
        self.last_axes = list(msg.axes)
        self.last_received = time.monotonic()

    def publish_velocity(self):
        # Inicia la orden con velocidades cero
        command = Twist()
        now = time.monotonic()
        forward = 0.0
        reverse = 0.0

        # Obtiene los parámetros actuales
        axis_forward = self.get_parameter('axis_forward').value
        axis_reverse = self.get_parameter('axis_reverse').value
        axis_angular = self.get_parameter('axis_angular').value
        max_linear = self.get_parameter('max_linear').value
        max_angular = self.get_parameter('max_angular').value
        timeout = self.get_parameter('timeout_sec').value

        # Comprueba los límites y los índices configurados
        config_ok = all(
            math.isfinite(v) and v > 0.0
            for v in (max_linear, max_angular, timeout)
        )
        axes_ok = (
            self.last_axes is not None
            and all(
                0 <= i < len(self.last_axes)
                for i in (axis_forward, axis_reverse, axis_angular)
            )
        )
        fresh = (
            self.last_received is not None
            and now - self.last_received <= timeout
        )

        if config_ok and axes_ok and fresh:
            # Convierte los gatillos negativos en presiones de cero a uno
            forward = max(0.0, min(1.0, -self.last_axes[axis_forward]))
            reverse = max(0.0, min(1.0, -self.last_axes[axis_reverse]))

            # Obtiene el giro del stick derecho
            angular = max(-1.0, min(1.0, self.last_axes[axis_angular]))

            # Resta la presión de L2 a la de R2 para avanzar o retroceder
            command.linear.x = (forward - reverse) * max_linear

            # Permite girar tanto en movimiento como en el lugar
            command.angular.z = angular * max_angular

        # Publica cero cuando no hay datos recientes válidos
        self.publisher_.publish(command)

        # Muestra las presiones y velocidades dos veces por segundo
        if now - self.last_log >= 0.5:
            self.get_logger().info(
                f'R2 = {forward:.2f}, L2 = {reverse:.2f} | '
                f'Lineal = {command.linear.x:.2f} | '
                f'Angular = {command.angular.z:.2f}'
            )
            self.last_log = now


def main(args=None):
    # Inicia ROS 2 y crea el nodo
    rclpy.init(args=args)
    node = PS4Teleop()

    try:
        # Mantiene el nodo activo
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Permite detener el programa con Ctrl+C
        pass
    finally:
        # Intenta enviar una orden de parada antes de cerrar
        if rclpy.ok():
            node.publisher_.publish(Twist())
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


# Ejecuta main cuando inicia el archivo directamente
if __name__ == '__main__':
    main()
