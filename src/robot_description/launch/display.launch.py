from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # Lee la descripción del robot
    paquete = Path(get_package_share_directory('robot_description'))
    modelo = (paquete / 'urdf' / 'robot.urdf').read_text()

    return LaunchDescription([
        # Publica las transformaciones de los enlaces
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': modelo}],
            output='screen',
        ),

        # Permite modificar el ángulo de las ruedas
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen',
        ),

        # Abre la configuración guardada de RViz
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', str(paquete / 'rviz' / 'display.rviz')],
            output='screen',
        ),
    ])
