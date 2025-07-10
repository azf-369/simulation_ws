import launch
import launch_ros
import os
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # 设置 turtlebot3 waffle 模型路径
    turtlebot3_model = 'waffle'
    turtlebot3_pkg = get_package_share_directory('turtlebot3_description')
    default_model_path = os.path.join(
        turtlebot3_pkg, 'urdf', f'turtlebot3_{turtlebot3_model}.urdf'
    )
    default_world_path = '/home/azf/slam_ws/src/fishbot_description/world/aws-robomaker-hospital-world/worlds/hospital.world'

    # 设置机器人描述参数
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name='model', default_value=str(default_model_path),
        description='URDF 的绝对路径')

    # 直接读取urdf文件内容
    with open(default_model_path, 'r') as infp:
        robot_description_content = infp.read()
    robot_description = launch_ros.parameter_descriptions.ParameterValue(
        robot_description_content,
        value_type=str
    )

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    launch_gazebo = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory(
            'gazebo_ros'), '/launch', '/gazebo.launch.py']),
        launch_arguments=[('world', default_world_path), ('verbose', 'true')]
    )

    spawn_entity_node = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', '/robot_description',
                   '-entity', 'turtlebot3', 
                   '-x', '1.0', '-y', '3.0', '-z', '0.0']
    )

    return launch.LaunchDescription([
        action_declare_arg_mode_path,
        robot_state_publisher_node,
        launch_gazebo,
        spawn_entity_node,
    ])