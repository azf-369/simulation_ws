# Gazebo 路径可视化系统使用说明

## 概述
这个系统允许你在Gazebo仿真环境中添加和管理可视化路径标记，帮助规划机器人导航路径。

## 系统组成

### 1. 地面路径模型（推荐使用）

#### 贴花路径模式
- 绿色地面圆盘：起始点
- 黄色地面圆盘：中间路径点
- 红色地面圆盘：目标点
- 蓝色地面带：路径连接线
- 黄色地面箭头：方向指示

#### 涂色地板路径模式（最佳效果）
- 绿色圆环标记：起始点
- 橙色圆环标记：中间路径点
- 红色圆环标记：目标点
- 蓝色涂色带：路径连接线（带白色中央引导线）
- **优势**：更像真实的地面涂色，视觉效果最佳，完全不影响机器人运动

### 2. 动态路径管理节点
- `path_visualizer`: 主要的路径可视化管理节点
- `path_controller`: 命令行控制工具

## 快速开始（推荐）

### 一键测试涂色地板路径
```bash
# 终端1：启动Gazebo和路径可视化节点
cd /home/azf/slam_ws
source install/setup.bash
ros2 launch fishbot_description hospital_with_path.launch.py

# 终端2：运行快速测试脚本
cd /home/azf/slam_ws
./test_painted_path.sh
```

### 手动测试步骤
```bash
# 1. 添加路径点
ros2 run fishbot_application path_controller add_point 5 5 0.1
ros2 run fishbot_application path_controller add_point 8 5 0.1
ros2 run fishbot_application path_controller add_point 8 8 0.1

# 2. 显示涂色地板路径
ros2 run fishbot_application path_controller show_painted_path
```

## 使用方法

### 方法1：使用静态地面路径启动
```bash
# 启动医院世界（包含静态地面路径标记）
cd /home/azf/slam_ws
source install/setup.bash
ros2 launch fishbot_description gazebo_sim.launch.py
```

### 方法2：使用涂色地板路径启动（强烈推荐）
```bash
# 启动带有动态路径管理的医院世界
cd /home/azf/slam_ws
source install/setup.bash
ros2 launch fishbot_description hospital_with_path.launch.py

# 在新终端中显示涂色地板路径
ros2 run fishbot_application path_controller show_painted_path
```

### 动态路径控制命令

#### 基本命令（推荐使用涂色地板路径）
```bash
# 在新终端中执行以下命令

# 1. 创建示例路径
ros2 run fishbot_application path_controller demo_path

# 2. 显示涂色地板路径（推荐）
ros2 run fishbot_application path_controller show_painted_path

# 3. 显示地面贴花路径
ros2 run fishbot_application path_controller show_path

# 4. 隐藏当前路径
ros2 run fishbot_application path_controller hide_path

# 5. 清除所有路径
ros2 run fishbot_application path_controller clear_path
```

#### 添加自定义路径点
```bash
# 添加路径点 (x, y, z坐标)
ros2 run fishbot_application path_controller add_point 0 -5 0.1   # 起始点
ros2 run fishbot_application path_controller add_point 2 -2 0.1   # 中间点
ros2 run fishbot_application path_controller add_point 2 2 0.1    # 转弯点
ros2 run fishbot_application path_controller add_point 0 4 0.1    # 终点
```

#### 使用ROS话题直接控制
```bash
# 发送地面路径命令
ros2 topic pub /path_command std_msgs/String "data: 'show_floor_path'" --once

# 发送3D路径命令
ros2 topic pub /path_command std_msgs/String "data: 'show_3d_path'" --once

# 发送示例路径命令
ros2 topic pub /path_command std_msgs/String "data: 'demo_path'" --once

# 添加路径点
ros2 topic pub /add_path_point geometry_msgs/Point "x: 1.0
y: 2.0  
z: 0.1" --once

# 监听状态
ros2 topic echo /path_status
```

## 路径显示模式说明

### 涂色地板路径模式（强烈推荐）
- **绿色圆环标记**: 路径起始点
- **橙色圆环标记**: 路径中间点
- **红色圆环标记**: 路径目标点
- **蓝色涂色带**: 路径连接线（带白色中央引导线）
- **厚度**: 仅0.1mm，完全贴在地面
- **效果**: 最像真实的地面涂漆标记
- **优势**: 视觉效果最佳，完全不影响机器人运动

### 地面贴花路径模式
- **绿色地面圆盘**: 路径起始点
- **黄色地面圆盘**: 路径中间点
- **红色地面圆盘**: 路径目标点
- **蓝色地面带**: 路径连接线
- **黄色地面箭头**: 方向指示
- **厚度**: 仅1mm，不影响机器人运动

## 坐标系统
医院世界的坐标系统：
- X轴：左右方向（正值向右）
- Y轴：前后方向（正值向前）
- Z轴：上下方向（正值向上）
- 机器人默认生成位置：(1.0, 3.0, 0.0)

## 示例场景

### 场景1：从入口到护士站（地面路径）
```bash
ros2 run fishbot_application path_controller add_point 0 -5 0.1    # 医院入口
ros2 run fishbot_application path_controller add_point 0 -2 0.1    # 大厅中央
ros2 run fishbot_application path_controller add_point 0 1.5 0.1   # 护士站
ros2 run fishbot_application path_controller show_floor_path       # 显示地面路径
```

### 场景2：病房巡查路线（地面路径）
```bash
ros2 run fishbot_application path_controller add_point -8 -10 0.1   # 左侧病房区
ros2 run fishbot_application path_controller add_point -8 -5 0.1    # 走廊
ros2 run fishbot_application path_controller add_point 8 -5 0.1     # 右侧病房区
ros2 run fishbot_application path_controller add_point 8 -10 0.1    # 返回点
ros2 run fishbot_application path_controller show_floor_path        # 显示地面路径
```

### 场景3：快速演示
```bash
ros2 run fishbot_application path_controller demo_path              # 创建示例路径
ros2 run fishbot_application path_controller show_floor_path        # 显示为地面路径
```

## 故障排除

### 1. 如果快速测试脚本失败
```bash
# 检查节点是否运行
ros2 node list | grep path

# 如果没有看到 /path_visualizer 节点，请确保：
# 1. Gazebo已启动
# 2. hospital_with_path.launch.py 已运行
ros2 launch fishbot_description hospital_with_path.launch.py

# 手动测试单个命令
cd /home/azf/slam_ws
source install/setup.bash
ros2 run fishbot_application path_controller add_point 5 5 0.1
ros2 run fishbot_application path_controller show_painted_path
```

### 2. 如果看不到路径标记
```bash
# 检查节点是否运行
ros2 node list | grep path

# 检查话题是否正常
ros2 topic list | grep path

# 重新显示涂色地板路径
ros2 run fishbot_application path_controller show_painted_path
```

### 3. 如果路径位置不合适
```bash
# 清除当前路径
ros2 run fishbot_application path_controller clear_path

# 重新添加正确的路径点
ros2 run fishbot_application path_controller add_point x y z
```

### 4. 如果Gazebo中看不到模型
- 确保Gazebo完全加载完成
- 检查控制台是否有错误信息
- 尝试重启Gazebo

### 5. 常见错误和解决方案

#### "source: not found" 错误
```bash
# 使用 bash 脚本而不是 python 脚本
./test_painted_path.sh  # 而不是 python3 quick_test_painted_path.py
```

#### 节点无法连接
```bash
# 确保先启动 Gazebo 和 path_visualizer 节点
ros2 launch fishbot_description hospital_with_path.launch.py
# 等待完全启动后，再运行测试
```

#### 路径显示位置错误
```bash
# 医院地图的坐标范围大约是 -15 到 15
# 建议使用以下坐标范围：
# X: -10 到 10
# Y: -10 到 10  
# Z: 0.1 (地面高度)
```

## 扩展功能

### 自定义路径样式
你可以修改 `path_visualizer.py` 中的材质参数来改变路径的外观：
- `ambient`: 环境光颜色
- `diffuse`: 漫反射颜色  
- `emissive`: 发光颜色
- 几何形状：`cylinder`、`box`、`sphere`

### 保存和加载路径
你可以扩展系统来保存路径到文件并在下次启动时加载。

## 下一步操作建议

1. **测试地面路径**：使用动态路径管理测试地面路径显示
   ```bash
   cd /home/azf/slam_ws
   colcon build
   source install/setup.bash
   ros2 launch fishbot_description hospital_with_path.launch.py
   # 新终端
   ros2 run fishbot_application path_controller demo_path
   ros2 run fishbot_application path_controller show_floor_path
   ```

2. **测试3D路径**：比较3D路径和地面路径的效果
3. **自定义路径**：根据你的需求添加自定义路径点
4. **集成导航**：将路径点作为导航目标点使用
5. **路径规划**：结合ROS2 Navigation Stack进行路径规划

## 推荐使用流程

### 最简单的使用方法
1. **启动系统**：
   ```bash
   cd /home/azf/slam_ws
   source install/setup.bash
   ros2 launch fishbot_description hospital_with_path.launch.py
   ```

2. **快速测试**（新终端）：
   ```bash
   cd /home/azf/slam_ws
   ./test_painted_path.sh
   ```

### 手动控制流程
1. **启动系统**：
   ```bash
   ros2 launch fishbot_description hospital_with_path.launch.py
   ```

2. **创建路径**：
   ```bash
   ros2 run fishbot_application path_controller demo_path
   ```

3. **显示涂色地板路径**：
   ```bash
   ros2 run fishbot_application path_controller show_painted_path
   ```

4. **机器人导航**：机器人可以正常在涂色地板路径上运动，路径不会影响机器人

记得在每次修改后重新编译工作空间：
```bash
cd /home/azf/slam_ws
colcon build
source install/setup.bash
```
