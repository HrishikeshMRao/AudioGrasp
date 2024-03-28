import os

import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

import launch
from launch import LaunchDescription, conditions
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='ur_robotiq_description' #<--- CHANGE ME
    default_model_path = "/home/fiend/voice_grab/ros2_ws/src/ur_robotiq/ur_robotiq_description/urdf/ur3e_robotiq_2f_85_urdf.xacro"

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'arm'],
                        output='screen')
    
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        arguments=[default_model_path],
    )
    
    Rviz = Node(
       package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
    )

    DeclareLaunchArgument(name='use_sim_time', 
                        default_value='True',
                        description='Flag to enable use_sim_time')
    

    # Launch them all!
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        joint_state_publisher_node,
        Rviz,
    ])