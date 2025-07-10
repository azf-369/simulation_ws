#!/bin/bash
# 简单的涂色地板路径测试脚本

echo "🎨 测试涂色地板路径功能"
echo "=================================================="

# 切换到工作空间目录
cd /home/azf/slam_ws

# 设置环境
source install/setup.bash

echo "📍 添加测试路径点..."

# 添加路径点
echo "  点 1: (5.0, 5.0, 0.1)"
ros2 run fishbot_application path_controller add_point 5.0 5.0 0.1
sleep 0.5

echo "  点 2: (8.0, 5.0, 0.1)"
ros2 run fishbot_application path_controller add_point 8.0 5.0 0.1
sleep 0.5

echo "  点 3: (8.0, 8.0, 0.1)"
ros2 run fishbot_application path_controller add_point 8.0 8.0 0.1
sleep 0.5

echo "  点 4: (5.0, 8.0, 0.1)"
ros2 run fishbot_application path_controller add_point 5.0 8.0 0.1
sleep 0.5

echo ""
echo "🎨 显示简化涂色地板路径..."
ros2 run fishbot_application path_controller show_painted_path

echo ""
echo "✅ 简化路径显示成功！"
echo ""
echo "请在Gazebo中查看效果："
echo "- 蓝色涂色带：路径连接线"
echo "- 白色中央引导线"
echo "- 无中间节点圆圈（简化设计）"

echo ""
echo "🎮 其他测试命令："
echo "  显示地面路径（含箭头）: ros2 run fishbot_application path_controller show_path"
echo "  隐藏路径: ros2 run fishbot_application path_controller hide_path"
echo "  清除路径: ros2 run fishbot_application path_controller clear_path"
