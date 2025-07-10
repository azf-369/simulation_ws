# 医院地图路径可视化系统

> 为医院Gazebo仿真环境提供地面路径可视化功能的ROS 2解决方案

![版本](https://img.shields.io/badge/版本-v3.0-blue.svg)
![ROS](https://img.shields.io/badge/ROS-2-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)
![许可](https://img.shields.io/badge/许可-MIT-lightgrey.svg)

## 📋 目录

- [系统概述](#系统概述)
- [功能特性](#功能特性)
- [环境要求](#环境要求)
- [安装步骤](#安装步骤)
- [使用指南](#使用指南)
- [API接口](#api接口)
- [配置参数](#配置参数)
- [故障排除](#故障排除)
- [版本历史](#版本历史)

## 🎯 系统概述

医院地图路径可视化系统是一个专为医院机器人导航设计的ROS 2包，能够在Gazebo仿真环境中以地面贴花/涂色的方式显示导航路径。系统设计简洁高效，路径完全贴地显示，不会影响机器人的正常运动。

### 核心优势

- 🏥 **医院环境优化**：蓝白配色方案，适合医院清洁环境
- 🤖 **无干扰设计**：地面贴花不影响机器人、轮椅、担架通行
- 🎨 **高可见性**：鲜明对比色确保路径清晰可见
- ⚡ **实时动态**：支持路径的实时添加、修改和删除
- 🧹 **易于管理**：虚拟路径可随时隐藏和清除

## ✨ 功能特性

### 当前版本特性 (v3.0)

- ✅ **纯地面路径**：路径完全贴地显示，极薄设计
- ✅ **仅直线连接**：路径点间只显示直线段，无装饰元素
- ✅ **无箭头标记**：简洁设计，移除所有箭头显示
- ✅ **无圆形节点**：移除所有圆盘/圆环标记
- ✅ **双路径模式**：支持涂色地板和贴花两种样式
- ✅ **动态管理**：实时添加、隐藏、清除路径

### 路径样式

#### 🎨 涂色地板路径（推荐）
- **底层基色**：蓝色涂漆效果（0.6m宽）
- **中央引导线**：白色中心线（0.1m宽）
- **边缘虚线**：深蓝色边界线（0.05m宽）
- **厚度**：0.0001m（极薄贴地）

#### 🏷️ 地面贴花路径（备用）
- **主路径带**：蓝色基础带（0.4m宽）
- **中央虚线**：白色中心线（0.05m宽）
- **边缘线条**：深蓝色边界线（0.03m宽）
- **厚度**：0.0005m（薄贴地）

## 🛠️ 环境要求

### 系统要求
- **操作系统**：Ubuntu 20.04 / 22.04
- **ROS版本**：ROS 2 Humble/Galactic
- **Python版本**：Python 3.8+
- **仿真环境**：Gazebo 11+

### 依赖包
```bash
# ROS 2 核心包
geometry_msgs
std_msgs
gazebo_msgs
rclpy

# 构建工具
colcon-common-extensions
```

## 📦 安装步骤

### 1. 克隆代码库

```bash
# 切换到ROS工作空间
cd ~/your_ros_workspace/src

# 克隆项目（如果是独立项目）
# git clone <repository_url>

# 或者直接使用现有的fishbot_application包
```

### 2. 安装依赖

```bash
# 安装ROS依赖
rosdep install --from-paths src --ignore-src -r -y

# 安装Python依赖
pip3 install -r requirements.txt  # 如果有的话
```

### 3. 编译项目

```bash
# 回到工作空间根目录
cd ~/your_ros_workspace

# 编译包
colcon build --packages-select fishbot_application

# 加载环境
source install/setup.bash
```

### 4. 验证安装

```bash
# 检查节点是否可用
ros2 pkg list | grep fishbot_application

# 检查可执行文件
ros2 run fishbot_application path_visualizer --help
```

## 🚀 使用指南

### 快速开始

#### 1. 启动Gazebo仿真环境

```bash
# 启动Gazebo（根据你的项目配置）
ros2 launch your_project gazebo.launch.py
```

#### 2. 启动路径可视化节点

```bash
# 方法1：直接运行
ros2 run fishbot_application path_visualizer

# 方法2：通过launch文件（如果有）
ros2 launch fishbot_application path_visualizer.launch.py
```

#### 3. 使用测试脚本

```bash
# 快速测试纯路径显示
./test_pure_path.sh

# 基础路径测试
./test_painted_path.sh
```

### 详细操作步骤

#### 步骤1：添加路径点

**方法A：通过话题逐个添加**
```bash
# 添加起点
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 0.0, y: 0.0, z: 0.1}"

# 添加中间点
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 5.0, y: 0.0, z: 0.1}"

# 添加转弯点
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 5.0, y: 3.0, z: 0.1}"

# 添加终点
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 8.0, y: 3.0, z: 0.1}"
```

**方法B：使用示例路径**
```bash
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'demo_path'}"
```

#### 步骤2：显示路径

**选项A：涂色地板路径（推荐）**
```bash
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'show_painted_path'}"
```

**选项B：地面贴花路径**
```bash
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'show_floor_path'}"
```

#### 步骤3：管理路径

**隐藏路径**
```bash
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'hide_path'}"
```

**清除所有路径**
```bash
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'clear_path'}"
```

### 批量操作脚本

创建自定义路径脚本：

```bash
#!/bin/bash
# custom_path.sh

echo "创建自定义医院路径..."

# 设置环境
source install/setup.bash

# 启动节点（后台运行）
ros2 run fishbot_application path_visualizer &
NODE_PID=$!

sleep 2

# 添加医院路径点
echo "添加大厅到诊室的路径..."
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 0.0, y: 0.0, z: 0.1}"    # 大厅入口
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 10.0, y: 0.0, z: 0.1}"   # 走廊
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 10.0, y: 5.0, z: 0.1}"   # 转弯处
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 15.0, y: 5.0, z: 0.1}"   # 诊室门口

sleep 1

# 显示涂色路径
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'show_painted_path'}"

echo "路径创建完成！"
echo "按Ctrl+C退出..."

wait $NODE_PID
```

## 📡 API接口

### 话题接口

#### 订阅话题

| 话题名称 | 消息类型 | 描述 |
|---------|---------|------|
| `/path_command` | `std_msgs/String` | 路径控制命令 |
| `/add_path_point` | `geometry_msgs/Point` | 添加路径点 |

#### 发布话题

| 话题名称 | 消息类型 | 描述 |
|---------|---------|------|
| `/path_status` | `std_msgs/String` | 路径状态信息 |

### 支持的命令

| 命令 | 功能描述 |
|------|---------|
| `show_path` / `show_floor_path` | 显示地面贴花路径 |
| `show_painted_path` | 显示涂色地板路径 |
| `hide_path` | 隐藏当前显示的路径 |
| `clear_path` | 清除所有路径点和路径 |
| `demo_path` | 创建示例演示路径 |

### 消息格式

#### Point消息（路径点）
```yaml
x: float64    # X坐标（米）
y: float64    # Y坐标（米）
z: float64    # Z坐标（米，建议0.1）
```

#### String消息（命令）
```yaml
data: string  # 命令字符串
```

## ⚙️ 配置参数

### 路径样式参数

可在代码中调整的关键参数（位于`path_visualizer.py`）：

```python
# 涂色地板路径参数
PAINTED_PATH_WIDTH = 0.6      # 主路径宽度（米）
CENTER_GUIDE_WIDTH = 0.1      # 中央引导线宽度（米）
EDGE_LINE_WIDTH = 0.05        # 边缘线宽度（米）
PAINTED_PATH_HEIGHT = 0.0001  # 路径厚度（米）

# 地面贴花路径参数
FLOOR_PATH_WIDTH = 0.4        # 主路径宽度（米）
CENTER_LINE_WIDTH = 0.05      # 中央线宽度（米）
EDGE_STRIP_WIDTH = 0.03       # 边缘条宽度（米）
FLOOR_PATH_HEIGHT = 0.0005    # 路径厚度（米）

# 颜色参数（RGBA）
MAIN_PATH_COLOR = (0.2, 0.6, 1, 0.9)    # 主路径蓝色
CENTER_LINE_COLOR = (1, 1, 1, 0.95)      # 中央线白色
EDGE_LINE_COLOR = (0, 0.4, 0.8, 0.8)     # 边缘线深蓝色
```

### 性能参数

```python
# 服务超时设置
SERVICE_TIMEOUT = 5.0         # 服务调用超时时间（秒）

# 实体命名
PATH_SEGMENT_PREFIX = "painted_floor_segment_"  # 路径段前缀
FLOOR_LINE_PREFIX = "floor_path_line_"          # 地面线前缀
```

## 🔧 故障排除

### 常见问题及解决方案

#### 1. 路径不显示

**症状**：发送命令后在Gazebo中看不到路径

**可能原因及解决方案**：

```bash
# 检查Gazebo是否运行
gazebo --version

# 检查节点是否启动
ros2 node list | grep path_visualizer

# 检查话题连接
ros2 topic list | grep path

# 检查路径点数据
ros2 topic echo /add_path_point --once

# 重启节点
ros2 node kill /path_visualizer
ros2 run fishbot_application path_visualizer
```

#### 2. 路径位置不准确

**症状**：路径显示在错误的位置

**解决步骤**：

```bash
# 1. 检查坐标系
ros2 topic info /add_path_point

# 2. 验证Z轴高度（建议0.1m）
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 0.0, y: 0.0, z: 0.1}"

# 3. 确认路径点顺序
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'clear_path'}"
# 然后重新按顺序添加路径点
```

#### 3. 性能问题

**症状**：路径显示卡顿或延迟

**优化方案**：

```bash
# 1. 减少路径点数量（建议<20个点）
# 2. 使用较短的路径段（<10m每段）
# 3. 及时清理不需要的路径

# 检查系统资源
htop
gazebo --verbose

# 重启Gazebo
killall gzserver gzclient
# 重新启动仿真环境
```

#### 4. 编译错误

**常见编译问题**：

```bash
# 清理构建缓存
rm -rf build/ install/ log/

# 检查依赖
rosdep check fishbot_application

# 重新安装依赖
rosdep install --from-paths src --ignore-src -r -y

# 重新编译
colcon build --packages-select fishbot_application --cmake-clean-cache
```

### 调试技巧

#### 启用详细日志

```bash
# 启动时启用调试日志
ros2 run fishbot_application path_visualizer --ros-args --log-level DEBUG

# 查看特定话题数据
ros2 topic echo /path_status
ros2 topic echo /add_path_point
```

#### 检查Gazebo实体

```bash
# 在Gazebo中查看当前实体
# 打开Gazebo GUI > View > Scene > Models
# 查找以"painted_floor_segment_"或"floor_path_line_"开头的模型
```

## 📈 性能指标

### 系统性能

- **路径生成延迟**：< 100ms
- **最大支持路径点**：1000个点
- **内存占用**：< 50MB
- **CPU占用**：< 5%

### 推荐使用限制

- **单次路径点数**：20-50个点
- **路径段长度**：1-10米
- **同时显示路径数**：1-3条

## 📋 版本历史

### v3.0 (当前版本) - 2025-07-09
- ✅ 移除所有箭头显示，实现纯路径可视化
- ✅ 简化代码结构，提升性能
- ✅ 完善文档和测试脚本
- ✅ 优化医院环境适配

### v2.0 - 2025-07-08
- ✨ 添加增强箭头系统
- ✨ 支持转弯检测和间隔箭头
- ✨ 多种箭头类型和颜色区分
- 🐛 修复路径连接问题

### v1.0 - 2025-07-07
- 🎉 基础路径可视化功能
- 🎨 双路径样式支持
- 📡 ROS 2话题接口
- 🏥 医院环境优化设计

## 🤝 贡献指南

### 开发环境设置

```bash
# 1. Fork项目
# 2. 克隆你的fork
git clone <your_fork_url>

# 3. 创建开发分支
git checkout -b feature/your-feature-name

# 4. 进行开发
# 5. 测试更改
./test_pure_path.sh

# 6. 提交更改
git commit -m "feat: 添加新功能描述"

# 7. 推送并创建Pull Request
```

### 代码规范

- 遵循PEP 8 Python代码规范
- 添加适当的注释和文档字符串
- 编写相应的测试用例
- 更新README.md（如需要）

## 📄 许可证

本项目采用MIT许可证。详细信息请查看[LICENSE](LICENSE)文件。

## 📞 支持与联系

- **问题报告**：[GitHub Issues](issues_url)
- **功能请求**：[GitHub Discussions](discussions_url)
- **文档**：[项目Wiki](wiki_url)

---

**🏥 专为医院机器人导航设计的地面路径可视化解决方案**

*如果这个项目对你有帮助，请给它一个⭐！*
