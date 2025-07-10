# 🚀 快速入门指南

> 5分钟快速上手医院地图路径可视化系统

## 📋 前置条件

确保你已经有：
- ✅ Ubuntu 20.04/22.04
- ✅ ROS 2 Humble/Galactic
- ✅ Gazebo 11+
- ✅ 工作的ROS工作空间

## ⚡ 3步快速开始

### 步骤1：编译和运行

```bash
# 编译
cd /path/to/your/slam_ws
colcon build --packages-select fishbot_application
source install/setup.bash

# 启动路径可视化节点
ros2 run fishbot_application path_visualizer
```

### 步骤2：使用测试脚本

在新终端中：
```bash
cd /path/to/your/slam_ws
./test_pure_path.sh
```

### 步骤3：查看结果

在Gazebo中你将看到：
- 🔵 蓝色涂色地板路径
- ⚪ 白色中央引导线
- 🔷 深蓝色边缘线

## 🎯 常用操作

### 手动添加路径

```bash
# 添加路径点
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 0.0, y: 0.0, z: 0.1}"
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 5.0, y: 0.0, z: 0.1}"

# 显示路径
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'show_painted_path'}"

# 清除路径
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'clear_path'}"
```

### 创建自定义路径脚本

```bash
#!/bin/bash
# my_hospital_path.sh

source install/setup.bash

# 启动节点
ros2 run fishbot_application path_visualizer &
sleep 2

# 大厅到手术室的路径
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 0.0, y: 0.0, z: 0.1}"
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 8.0, y: 0.0, z: 0.1}"
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 8.0, y: 5.0, z: 0.1}"
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 12.0, y: 5.0, z: 0.1}"

# 显示路径
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'show_painted_path'}"

echo "医院路径已创建！"
```

## 🔧 快速故障排除

| 问题 | 解决方案 |
|-----|----------|
| 路径不显示 | 检查Gazebo是否运行，节点是否启动 |
| 位置不对 | 确认z轴设为0.1，检查坐标系 |
| 编译失败 | `rm -rf build install log && colcon build` |

## 📚 更多信息

- 📖 完整文档：[README.md](README.md)
- 🎯 详细指南：[PURE_PATH_GUIDE.md](PURE_PATH_GUIDE.md)
- 🧪 测试脚本：`test_pure_path.sh`

---

**享受你的医院路径可视化之旅！** 🏥✨
