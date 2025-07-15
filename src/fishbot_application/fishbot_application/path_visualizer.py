#!/usr/bin/env python3
"""
路径可视化节点
用于在Gazebo中动态添加、移除和管理路径可视化标记
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from std_msgs.msg import String, Bool
from gazebo_msgs.srv import SpawnEntity, DeleteEntity
from ament_index_python.packages import get_package_share_directory
import os
import math

class PathVisualizerNode(Node):
    def __init__(self):
        super().__init__('path_visualizer')
        
        # 服务客户端
        self.spawn_client = self.create_client(SpawnEntity, '/spawn_entity')
        self.delete_client = self.create_client(DeleteEntity, '/delete_entity')
        
        # 订阅者和发布者
        self.create_subscription(String, '/path_command', self.command_callback, 10)
        self.create_subscription(Point, '/add_path_point', self.add_path_point_callback, 10)
        
        # 状态发布者
        self.status_publisher = self.create_publisher(String, '/path_status', 10)
        
        # 路径点存储
        self.path_points = []
        self.path_entities = []
        
        self.get_logger().info('路径可视化节点已启动')
        self.get_logger().info('可用命令:')
        self.get_logger().info('  - "show_path" / "show_floor_path": 显示地面路径')
        self.get_logger().info('  - "show_painted_path": 显示涂色地板路径')
        self.get_logger().info('  - "hide_path": 隐藏路径')
        self.get_logger().info('  - "clear_path": 清除所有路径')
        self.get_logger().info('  - "demo_path": 创建示例路径')
        
    def command_callback(self, msg):
        """处理路径命令"""
        command = msg.data.lower()
        
        if command == "show_path" or command == "show_floor_path":
            self.show_floor_path()
        elif command == "show_painted_path":
            self.show_painted_floor_path()
        elif command == "hide_path":
            self.hide_current_path()
        elif command == "clear_path":
            self.clear_all_paths()
        elif command == "demo_path":
            self.create_demo_path()
        else:
            self.get_logger().warn(f'未知命令: {command}')
    
    def add_path_point_callback(self, msg):
        """添加路径点"""
        point = [msg.x, msg.y, msg.z]
        self.path_points.append(point)
        self.get_logger().info(f'添加路径点: ({msg.x:.2f}, {msg.y:.2f}, {msg.z:.2f})')
        self.get_logger().info(f'当前共有 {len(self.path_points)} 个路径点')
    
    def create_demo_path(self):
        """创建示例路径"""
        self.clear_all_paths()
        
        # 添加示例路径点
        demo_points = [
            [0, -5, 0.1],    # 起始点
            [0, -2, 0.1],    # 中间点1
            [2, 0, 0.1],     # 转弯点
            [2, 2, 0.1],     # 中间点2
            [0, 4, 0.1]      # 终点
        ]
        
        self.path_points = demo_points
        self.show_painted_floor_path()
        self.get_logger().info('已创建示例路径')
    
    def hide_current_path(self):
        """隐藏当前路径"""
        if not self.path_entities:
            return
            
        for entity_name in self.path_entities:
            self.delete_entity(entity_name)
        
        self.path_entities.clear()
        
        # 等待删除操作完成
        import time
        time.sleep(0.5)
        
        self.get_logger().info('路径已隐藏')
        self.publish_status("路径已隐藏")
    
    def clear_all_paths(self):
        """清除所有路径"""
        self.hide_current_path()
        self.path_points.clear()
        self.get_logger().info('所有路径已清除')
        self.publish_status("所有路径已清除")
    
    def spawn_entity(self, entity_name, sdf_content, position):
        """生成实体"""
        if not self.spawn_client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('spawn_entity 服务不可用')
            return
        
        request = SpawnEntity.Request()
        request.name = entity_name
        request.xml = sdf_content
        request.robot_namespace = ""
        request.initial_pose.position.x = float(position[0])
        request.initial_pose.position.y = float(position[1])
        request.initial_pose.position.z = float(position[2])
        
        future = self.spawn_client.call_async(request)
        future.add_done_callback(lambda f: self.spawn_callback(f, entity_name))
    
    def spawn_callback(self, future, entity_name):
        """生成回调"""
        try:
            response = future.result()
            if response.success:
                self.path_entities.append(entity_name)
                self.get_logger().debug(f'成功生成实体: {entity_name}')
            else:
                self.get_logger().error(f'生成实体失败: {entity_name} - {response.status_message}')
        except Exception as e:
            self.get_logger().error(f'生成实体异常: {entity_name} - {str(e)}')
    
    def delete_entity(self, entity_name):
        """删除实体"""
        if not self.delete_client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('delete_entity 服务不可用')
            return
        
        request = DeleteEntity.Request()
        request.name = entity_name
        
        future = self.delete_client.call_async(request)
        future.add_done_callback(lambda f: self.delete_callback(f, entity_name))
    
    def delete_callback(self, future, entity_name):
        """删除回调"""
        try:
            response = future.result()
            if response.success:
                self.get_logger().debug(f'成功删除实体: {entity_name}')
            else:
                self.get_logger().error(f'删除实体失败: {entity_name} - {response.status_message}')
        except Exception as e:
            self.get_logger().error(f'删除实体异常: {entity_name} - {str(e)}')
    
    def publish_status(self, status):
        """发布状态消息"""
        msg = String()
        msg.data = status
        self.status_publisher.publish(msg)
    
    def show_painted_floor_path(self):
        """显示涂色地板路径（仅显示连接线，无节点圆圈）"""
        if not self.path_points:
            self.get_logger().warn('没有路径点可显示')
            return
        
        if len(self.path_points) < 2:
            self.get_logger().warn('至少需要2个路径点才能显示路径')
            return
        
        # 先隐藏现有路径
        self.hide_current_path()
        
        # 创建连续的地面涂色路径
        for i in range(len(self.path_points) - 1):
            self.spawn_painted_floor_segment(i, self.path_points[i], self.path_points[i + 1])
        
        self.get_logger().info('涂色地板路径已显示（仅连接线）')
        self.publish_status("涂色地板路径已显示")
    
    def spawn_painted_floor_segment(self, index, point1, point2):
        """生成涂色地板路径段"""
        entity_name = f"painted_floor_segment_{index}"
        
        # 计算基础长度和角度
        base_length = math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2) * 1.78
        angle = math.atan2(point2[1] - point1[1], point2[0] - point1[0])
        
        # 使用更大的重叠，确保路径段完全覆盖从点1到点2
        overlap_extension = base_length * 0.2  # 增加20%的重叠
        extended_length = base_length + overlap_extension
        
        # 使用原始的中心点，不进行偏移
        center_x = (point1[0] + point2[0]) / 2
        center_y = (point1[1] + point2[1]) / 2
        center_z = 0.0001  # 极薄贴在地面
        
        # 创建纯蓝色路径效果
        sdf_content = f"""
        <sdf version="1.6">
          <model name="{entity_name}">
            <static>true</static>
            <pose>{center_x} {center_y} {center_z} 0 0 {angle}</pose>
            <link name="link">
              <!-- 纯蓝色涂色路径 -->
              <visual name="base_paint">
                <geometry>
                  <box>
                    <size>{extended_length} 0.6 0.0001</size>
                  </box>
                </geometry>
                <material>
                  <ambient>0 0.5 1 1.0</ambient>
                  <diffuse>0 0.5 1 1.0</diffuse>
                  <specular>0.1 0.1 0.1 1</specular>
                  <emissive>0 0.1 0.2 0</emissive>
                </material>
              </visual>
            </link>
          </model>
        </sdf>
        """
        
        self.spawn_entity(entity_name, sdf_content, [center_x, center_y, center_z])
    
    
def main(args=None):
    rclpy.init(args=args)
    node = PathVisualizerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
