from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    talker_node = Node(
        package = "my_package",
        executable = "talk"
    )

    talker_node_2 = Node(
        package = "my_package",
        executable = "talk2"
    )

    ld.add_action(talker_node)
    ld.add_action(talker_node_2)

    return ld