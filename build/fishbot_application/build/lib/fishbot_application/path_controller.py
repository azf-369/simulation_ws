#!/usr/bin/env python3
"""
路径控制脚本
提供简单的命令行界面来控制Gazebo中的路径可视化
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Point
import sys

class PathController(Node):
    def __init__(self):
        super().__init__('path_controller')
        
        # 发布者
        self.command_publisher = self.create_publisher(String, '/path_command', 10)
        self.point_publisher = self.create_publisher(Point, '/add_path_point', 10)
        
        # 订阅状态
        self.create_subscription(String, '/path_status', self.status_callback, 10)
        
        self.get_logger().info('路径控制器已启动')
    
    def status_callback(self, msg):
        """状态回调"""
        self.get_logger().info(f'状态更新: {msg.data}')
    
    def send_command(self, command):
        """发送命令"""
        msg = String()
        msg.data = command
        self.command_publisher.publish(msg)
        self.get_logger().info(f'发送命令: {command}')
    
    def add_point(self, x, y, z=0.1):
        """添加路径点"""
        msg = Point()
        msg.x = float(x)
        msg.y = float(y)
        msg.z = float(z)
        self.point_publisher.publish(msg)
        self.get_logger().info(f'添加路径点: ({x}, {y}, {z})')

def main():
    rclpy.init()
    controller = PathController()
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python3 path_controller.py show_path          # 显示地面贴花路径")
        print("  python3 path_controller.py show_painted_path  # 显示涂色地板路径（推荐）")
        print("  python3 path_controller.py show_floor_path    # 显示地面贴花路径")
        print("  python3 path_controller.py hide_path          # 隐藏路径")
        print("  python3 path_controller.py clear_path         # 清除路径")
        print("  python3 path_controller.py demo_path          # 创建示例路径")
        print("  python3 path_controller.py add_point x y [z]  # 添加路径点")
        return
    
    command = sys.argv[1]
    
    if command in ['show_path', 'show_floor_path', 'show_painted_path', 'hide_path', 'clear_path', 'demo_path']:
        controller.send_command(command)
    elif command == 'add_point' and len(sys.argv) >= 4:
        x = sys.argv[2]
        y = sys.argv[3]
        z = sys.argv[4] if len(sys.argv) > 4 else 0.1
        controller.add_point(x, y, z)
    else:
        print(f"未知命令: {command}")
        return
    
    # 等待一秒钟让消息发送
    rclpy.spin_once(controller, timeout_sec=1.0)
    
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
