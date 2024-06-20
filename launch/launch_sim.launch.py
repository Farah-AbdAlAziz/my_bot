import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Set the package name and ensure it's correct
    package_name = 'my_bot' # Make sure this matches your package name

    # Construct the full path to rsp.launch.py
    rsp_path = os.path.join(get_package_share_directory(package_name), 'launch', 'rsp.launch.py')
    assert os.path.exists(rsp_path), f"{rsp_path} does not exist"

    # Construct the full path to gazebo.launch.py
    gazebo_path = os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
    assert os.path.exists(gazebo_path), f"{gazebo_path} does not exist"

    # Include the robot_state_publisher launch file
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([rsp_path]), 
                launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([gazebo_path])
             )

    # Run the spawner node
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')

    # Launch them all
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
    ])