#!/bin/bash

echo "=== 医院地图纯蓝色路径可视化测试 ==="
echo "测试纯蓝色路径：简洁无花纹设计"
echo ""

# 设置环境
source /home/azf/slam_ws/install/setup.bash

echo "📍 添加测试路径点..."

# 添加路径点（创建一个L形路径展示效果）
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 0.0, y: 0.0, z: 0.1}" &
sleep 0.5

ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 6.0, y: 0.0, z: 0.1}" &
sleep 0.5

ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 6.0, y: 4.0, z: 0.1}" &
sleep 0.5

ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 10.0, y: 4.0, z: 0.1}" &
sleep 0.5

ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 10.0, y: 8.0, z: 0.1}" &
sleep 0.5

echo ""
echo "🎨 显示纯蓝色涂色地板路径..."
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'show_painted_path'}" &

sleep 2

echo ""
echo "🎨 显示纯蓝色地面贴花路径..."
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'show_floor_path'}" &

sleep 2

echo ""
echo "=== 纯蓝色路径可视化特征说明 ==="
echo "✓ 纯蓝色路径：rgb(0, 0.5, 1) 统一颜色"
echo "✓ 涂色地板路径：0.6m宽，极薄贴地（0.0001m）"
echo "✓ 地面贴花路径：0.4m宽，薄贴地（0.0005m）"
echo "✓ 无中央引导线：简洁设计"
echo "✓ 无边缘装饰线：纯色效果"
echo "✓ 无箭头标记：最简设计"
echo "✓ 高对比度：适合医院环境"
echo ""
echo "路径颜色对比测试完成！"
echo ""
echo "💡 管理命令："
echo "  隐藏路径: ros2 topic pub --once /path_command std_msgs/msg/String '{data: \"hide_path\"}'"
echo "  清除路径: ros2 topic pub --once /path_command std_msgs/msg/String '{data: \"clear_path\"}'"
