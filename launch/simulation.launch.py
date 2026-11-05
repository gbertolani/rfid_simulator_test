import os
import shlex

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    package = get_package_share_directory('rfid_simulator_test')
    actions = [IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(package, 'launch', 'pioneer3atRFID.launch.py')
    ))]
    entities = [('tag1', ['2.90', '0.57', '2.05']), ('tag2', ['2.90', '-1.24', '2.05']), ('tag3', ['2.90', '-3.03', '2.05']), ('tag4', ['2.90', '-4.82', '2.05']), ('tag5', ['2.90', '-6.75', '2.05']), ('tag6', ['2.90', '-8.66', '2.05']), ('tag7', ['-4.85', '-7.70', '1.85']), ('tag8', ['-4.85', '-3.03', '1.85']), ('tag9', ['-4.85', '1.44', '1.85']), ('tag10', ['-4.85', '5.95', '1.85']), ('antenna_fixed', ['3.5', '-4.0', '2.0'])]
    for entity, xyz in entities:
        is_antenna = entity == 'antenna_fixed'
        xacro_file = ('antenna/antenna.urdf.xacro' if is_antenna else 'tag/tag.urdf.xacro')
        xacro_cmd = ['xacro', os.path.join(package, 'urdf', xacro_file)]
        if is_antenna:
            xacro_cmd.append('name_idx:=_fixed')
        spawn_cmd = [
            'ros2', 'run', 'gazebo_ros', 'spawn_entity.py', '-stdin', '-entity', entity,
            '-x', xyz[0], '-y', xyz[1], '-z', xyz[2],
        ]
        actions.append(ExecuteProcess(
            cmd=[shlex.join(xacro_cmd) + ' | ' + shlex.join(spawn_cmd)],
            shell=True, name='spawn_gazebo_' + entity, output='screen',
        ))
        actions.append(Node(
            package='tf2_ros', executable='static_transform_publisher',
            name=entity + '_to_map',
            arguments=[*xyz, '0', '0', '0', '1', 'map', entity],
        ))
    return LaunchDescription(actions)
