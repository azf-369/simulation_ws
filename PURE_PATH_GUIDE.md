# 医院地图纯路径可视化指南

## 功能概述

本系统为医院Gazebo仿真环境提供纯粹的地面路径可视化功能，路径以地面贴花/涂色方式显示，不影响机器人正常运动。

## 核心特性

- ✅ **纯地面路径**：路径完全贴地显示，不影响机器人运动
- ✅ **仅直线连接**：路径点间只显示直线段，无任何装饰
- ✅ **无箭头标记**：完全移除所有箭头显示
- ✅ **无圆形节点**：完全移除所有圆盘/圆环标记
- ✅ **简洁设计**：专注于基础路径指示功能
- ✅ **高可见性**：鲜明色彩确保医院环境中清晰可见

## 路径样式

### 涂色地板路径（推荐）
- **纯蓝色基色**：统一蓝色效果（0.6m宽）
- **厚度**：0.0001m（极薄贴地）
- **颜色**：rgb(0, 0.5, 1) 纯蓝色

### 地面贴花路径（备用）
- **纯蓝色路径带**：统一蓝色基础带（0.4m宽）
- **厚度**：0.0005m（薄贴地）
- **颜色**：rgb(0, 0.5, 1) 纯蓝色

## 使用方法

### 1. 启动路径可视化节点
```bash
ros2 run fishbot_application path_visualizer
```

### 2. 添加路径点
```bash
# 方法1：通过话题添加单个点
ros2 topic pub --once /add_path_point geometry_msgs/msg/Point "{x: 0.0, y: 0.0, z: 0.1}"

# 方法2：通过代码调用demo_path
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'demo_path'}"
```

### 3. 显示路径
```bash
# 显示涂色地板路径（推荐）
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'show_painted_path'}"

# 显示地面贴花路径（备用）
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'show_floor_path'}"
```

### 4. 路径管理
```bash
# 隐藏路径
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'hide_path'}"

# 清除路径
ros2 topic pub --once /path_command std_msgs/msg/String "{data: 'clear_path'}"
```

## 快速测试

```bash
# 启动节点并测试纯路径显示
./test_pure_path.sh
```

## 系统架构

```
PathVisualizerNode
├── 路径接收：/add_path_point (Point)
├── 命令接收：/path_command (String)
├── 核心功能：
│   ├── 地面路径渲染
│   ├── 涂色地板路径
│   └── Gazebo实体管理
└── 状态发布：/path_status (String)
```

## 支持的命令

- `show_path` / `show_floor_path`：显示地面贴花路径
- `show_painted_path`：显示涂色地板路径  
- `hide_path`：隐藏当前路径
- `clear_path`：清除所有路径点和路径
- `demo_path`：创建示例路径

## 医院环境优化

- **高对比度**：蓝白配色方案适合医院环境
- **无障碍设计**：地面贴花不影响轮椅、担架通行
- **简洁美观**：无多余装饰，专注路径指示
- **易于清理**：虚拟路径可随时隐藏/清除

## 技术参数

### 路径尺寸
- 涂色地板路径宽度：0.6m
- 地面贴花路径宽度：0.4m

### 高度设置
- 涂色地板路径：0.0001m（极薄贴地）
- 地面贴花路径：0.0005m（薄贴地）

### 颜色方案
- 主路径色：rgb(0, 0.5, 1) 纯蓝色

## 故障排除

### 路径不显示
1. 检查Gazebo是否运行
2. 确认节点已启动：`ros2 node list`
3. 验证路径点数据：`ros2 topic echo /add_path_point`

### 路径位置不准确
1. 确认路径点坐标系设置正确
2. 检查z轴高度设置（建议0.1m）
3. 验证路径点顺序

### 性能问题
1. 减少路径点数量
2. 使用较短的路径段
3. 及时清理不需要的路径

## 开发信息

- **编程语言**：Python 3
- **ROS版本**：ROS 2
- **依赖包**：geometry_msgs, std_msgs, gazebo_msgs
- **仿真环境**：Gazebo
- **设计原则**：简洁、高效、无干扰

## 版本历史

- v1.0：基础路径可视化功能
- v2.0：添加转弯箭头和间隔箭头
- v3.0：移除所有箭头，实现纯路径显示（当前版本）

---

*适用于医院机器人导航系统的地面路径可视化解决方案*
