# 使用方法:

## step 1: start gazebo:

### 构建:
colcon build

### 设置环境
source /home/azf/simulation_ws/install/setup.bash (需替换为本地路径)

export SVGA_VGPU10=0  (可选,用于解决地图可视化异常的问题)

export GAZEBO_MODEL_PATH=/home/azf/simulation_ws/src/fishbot_description/world/aws-robomaker-hospital-world/fuel_models:/home/azf/simulation_ws/src/fishbot_description/world/aws-robomaker-hospital-world/models:$GAZEBO_MODEL_PATH  (添加地图模型路径,需替换为本地路径)

### 启动仿真
ros2 launch fishbot_description gazebo_sim.launch.py

## step 2: start path_visualizer node:
source install/setup.bash

ros2 run fishbot_application path_visualizer

## step 3: 运行 ./show_path.sh 路径可视化:
./show_path.sh


## step 4: 使用path_controller清除路径:
python3 ./src/fishbot_application/fishbot_application/path_controller.py clear_path



## 停止仿真: pkill -f gazebo && pkill -f path_visualizer
