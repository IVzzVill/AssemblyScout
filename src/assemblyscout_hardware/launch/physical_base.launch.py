"""Inicio del puente físico en Raspberry Pi o en modo local de prueba."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('transport', default_value='dry_run'),
        DeclareLaunchArgument('serial_port', default_value='/dev/ttyUSB0'),
        DeclareLaunchArgument('max_linear_mps', default_value='0.15'),
        DeclareLaunchArgument('max_angular_radps', default_value='0.70'),
        Node(
            package='assemblyscout_hardware',
            executable='esp32_bridge',
            parameters=[{
                'transport': LaunchConfiguration('transport'),
                'serial_port': LaunchConfiguration('serial_port'),
                'max_linear_mps': LaunchConfiguration('max_linear_mps'),
                'max_angular_radps': LaunchConfiguration('max_angular_radps'),
            }],
            output='screen',
        ),
    ])
