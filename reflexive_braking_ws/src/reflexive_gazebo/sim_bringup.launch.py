from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # Launches the safety arbitration supervisor
        Node(
            package='reflexive_core',
            executable='safety_supervisor_node',
            name='safety_supervisor',
            output='screen',
            parameters=[{
                'ttc_threshold_sec': 1.2,
                'min_stopping_distance_m': 0.8,
            }],
            remappings=[
                ('/cmd_vel_teleop', '/input/cmd_vel'),
                ('/cmd_vel', '/output/cmd_vel'),
            ]
        )
    ])