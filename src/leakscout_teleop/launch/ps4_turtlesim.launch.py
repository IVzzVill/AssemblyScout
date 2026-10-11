# Importa las herramientas para iniciar varios nodos
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # Define los tres procesos del sistema de teleoperación
    return LaunchDescription([
        # Lee los ejes y botones del control y los publica en /joy
        Node(
            package='joy',
            executable='game_controller_node',
            name='ps4_driver',
            parameters=[{
                'deadzone': 0.05,
                'autorepeat_rate': 20.0,
            }],
            output='screen'
        ),

        # Abre el simulador de la tortuga
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            output='screen'
        ),

        # Convierte los gatillos y el stick derecho en velocidades
        Node(
            package='leakscout_teleop',
            executable='ps4_teleop',
            parameters=[{
                'axis_forward': 5,
                'axis_reverse': 4,
                'axis_angular': 2,
                'max_linear': 1.5,
                'max_angular': 1.5,
                'timeout_sec': 0.5,
            }],
            output='screen'
        ),
    ])
