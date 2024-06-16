Make sure to remove the suffix and replace _mimic with a null string. In gazebo_ros2_control. 
Also change the accuracy to 1e-2 instead of 1e-4 under moveit_task_constructor_core in source and build it againt by selecting only that package with:
  colcon build --executor sequential --packages-select gazebo_ros2_control
  colcon build --executor sequential --packages-select moveit_task_constructor_core

Make the necessary changes required machine specific.
