from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    package = FindPackageShare('rfid_simulator_test')
    use_sim_time = LaunchConfiguration('use_sim_time')
    robot_description = ParameterValue(Command([
        'xacro ', PathJoinSubstitution([
            package, 'urdf', 'robot_with_laser_and_antenna.urdf.xacro'
        ])
    ]), value_type=str)
    arguments = [
        DeclareLaunchArgument('paused', default_value='false'),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('gui', default_value='true'),
        DeclareLaunchArgument('headless', default_value='false'),
        DeclareLaunchArgument('debug', default_value='false'),
        DeclareLaunchArgument('verbose', default_value='false'),
        DeclareLaunchArgument('world', default_value=PathJoinSubstitution([
            FindPackageShare('aws_robomaker_small_warehouse_world'),
            'worlds', 'no_roof_small_warehouse.world'
        ])),
    ]
    return LaunchDescription(arguments + [
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(PathJoinSubstitution([
                FindPackageShare('gazebo_ros'), 'launch', 'gazebo.launch.py'
            ])),
            launch_arguments={
                'world': LaunchConfiguration('world'),
                'gdb': LaunchConfiguration('debug'),
                'gui': PythonExpression([
                    "'", LaunchConfiguration('gui'), "'.lower() == 'true' and '",
                    LaunchConfiguration('headless'), "'.lower() != 'true'"
                ]),
                'pause': LaunchConfiguration('paused'),
                'verbose': LaunchConfiguration('verbose'),
            }.items(),
        ),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             name='robot_state_publisher', parameters=[{
                 'robot_description': robot_description, 'use_sim_time': use_sim_time
             }]),
        Node(package='joint_state_publisher', executable='joint_state_publisher',
             name='joint_state_publisher', parameters=[{'use_sim_time': use_sim_time}]),
        Node(package='gazebo_ros', executable='spawn_entity.py', name='spawn_urdf',
             arguments=['-topic', 'robot_description', '-entity', 'pioneer3at_robot']),
    ])
