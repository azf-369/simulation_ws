#!/bin/bash

echo "=== 医院地图路径可视化脚本 ==="

# 设置环境 (需替换为本地路径)
source /home/azf/simulation_ws/install/setup.bash 

# 添加路径点
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 0.0, y: 0.5, z: 0.1}"
sleep 0.5

ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 2.5, y: 0.5, z: 0.1}"
sleep 0.5

ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 2.5, y: -4.5, z: 0.1}"
sleep 0.5

ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 4.5, y: -4.5, z: 0.1}"
sleep 0.5

ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 4.5, y: -0.5, z: 0.1}"
sleep 1

echo "显示路径..."
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'show_painted_path'}"