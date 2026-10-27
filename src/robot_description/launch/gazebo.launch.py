from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package = Path(get_package_share_directory('robot_description'))
    ros_gz_sim = Path(get_package_share_directory('ros_gz_sim'))
    model = (package / 'urdf' / 'robot.urdf').read_text()
    use_joystick = LaunchConfiguration('use_joystick')
    use_rviz = LaunchConfiguration('use_rviz')
    arrange_windows = LaunchConfiguration('arrange_windows')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(ros_gz_sim / 'launch' / 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': model,
            'use_sim_time': True,
        }],
        output='screen',
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'assemblyscout',
            '-topic', 'robot_description',
            '-z', '0.0135',
        ],
        output='screen',
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
        ],
        output='screen',
    )

    joystick = Node(
        package='joy',
        executable='game_controller_node',
        name='ps4_driver',
        parameters=[{
            'deadzone': 0.05,
            'autorepeat_rate': 20.0,
        }],
        condition=IfCondition(use_joystick),
        output='screen',
    )

    teleop = Node(
        package='assemblyscout_teleop',
        executable='ps4_teleop',
        parameters=[{
            'axis_forward': 5,
            'axis_reverse': 4,
            'axis_angular': 2,
            'max_linear': 0.40,
            'max_angular': 2.00,
            'timeout_sec': 0.5,
            'cmd_vel_topic': '/cmd_vel',
        }],
        condition=IfCondition(use_joystick),
        output='screen',
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=[
            '-d', str(package / 'rviz' / 'display.rviz'),
            '-f', 'odom',
        ],
        parameters=[{'use_sim_time': True}],
        condition=IfCondition(use_rviz),
        output='screen',
    )

    window_arranger = TimerAction(
        period=3.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'bash',
                    str(package / 'scripts' / 'arrange_windows.sh'),
                ],
                output='screen',
            ),
        ],
        condition=IfCondition(arrange_windows),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_joystick',
            default_value='true',
            description='Inicia el mando PS4 y la teleoperación',
        ),
        DeclareLaunchArgument(
            'use_rviz',
            default_value='true',
            description='Inicia RViz junto con Gazebo',
        ),
        DeclareLaunchArgument(
            'arrange_windows',
            default_value='true',
            description='Acomoda Gazebo y RViz en mitades de la pantalla',
        ),
        gazebo,
        robot_state_publisher,
        spawn_robot,
        bridge,
        joystick,
        teleop,
        rviz,
        window_arranger,
    ])
