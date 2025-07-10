#!/usr/bin/env python3
"""
快速测试涂色地板路径功能
"""

import subprocess
import time
import os

def quick_test():
    """快速测试涂色地板路径功能"""
    print("🎨 测试涂色地板路径功能")
    print("=" * 50)
    
    # 切换到工作空间
    os.chdir('/home/azf/slam_ws')
    
    # 环境设置 - 使用bash shell并正确设置环境
    env = os.environ.copy()
    
    print("📍 添加测试路径点...")
    points = [
        (5.0, 5.0, 0.1),
        (8.0, 5.0, 0.1),
        (8.0, 8.0, 0.1),
        (5.0, 8.0, 0.1),
    ]
    
    for i, (x, y, z) in enumerate(points):
        cmd = f"bash -c 'source install/setup.bash && ros2 run fishbot_application path_controller add_point {x} {y} {z}'"
        print(f"  点 {i+1}: ({x}, {y}, {z})")
        subprocess.run(cmd, shell=True, env=env, capture_output=True, timeout=5)
        time.sleep(0.5)
    
    print("\n🎨 显示涂色地板路径...")
    cmd = "bash -c 'source install/setup.bash && ros2 run fishbot_application path_controller show_painted_path'"
    result = subprocess.run(cmd, shell=True, env=env, capture_output=True, timeout=10)
    
    if result.returncode == 0:
        print("✅ 涂色地板路径显示成功！")
        print("\n请在Gazebo中查看效果：")
        print("- 绿色圆环：起始点")
        print("- 橙色圆环：中间点")  
        print("- 红色圆环：终点")
        print("- 蓝色涂色带：路径连接线")
        print("- 白色中央引导线")
        
        print("\n🎮 其他测试命令：")
        print("  显示地面贴花路径: ros2 run fishbot_application path_controller show_path")
        print("  显示3D路径: ros2 run fishbot_application path_controller show_3d_path")
        print("  隐藏路径: ros2 run fishbot_application path_controller hide_path")
        print("  清除路径: ros2 run fishbot_application path_controller clear_path")
    else:
        print("❌ 显示失败，请检查:")
        print("1. Gazebo是否已启动")
        print("2. path_visualizer节点是否运行")
        print("3. 运行: ros2 launch fishbot_description hospital_with_path.launch.py")
        if result.stderr:
            print(f"错误信息: {result.stderr.decode()}")

if __name__ == '__main__':
    quick_test()
