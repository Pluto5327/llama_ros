#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from llama_msgs.srv import GPT


class LlamaClientNode(Node):

    def __init__(self) -> None:
        super().__init__("llama_client_node")

        self.sub = self.create_subscription(
            String, "gpt_text", self.text_cb, 10)
        self.client = self.create_client(GPT, "gpt")

    def text_cb(self, msg: String) -> None:
        print(msg.data, end="", flush=True)

    def send_prompt(self, text: str) -> None:
        self.client.wait_for_service()
        req = GPT.Request()
        req.prompt = text
        future = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        print("\n")


def main():

    rclpy.init()

    node = LlamaClientNode()
    node.send_prompt("""Do you know the city of León from Spain?
Can you tell me a bit about its history?""")

    rclpy.shutdown()


if __name__ == "__main__":
    main()
