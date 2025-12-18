# ai_communicator.py
import os
import base64
import logging
from openai import OpenAI  # 注意：需要安装 openai 库


class AICommunicator:
    def __init__(self, config):
        self.config = config
        # 初始化OpenAI客户端，并指向阿里云百炼的兼容端点
        self.client = OpenAI(
            api_key=self.config.ai_api_key,  # 从你的config中读取密钥
            base_url=
        )
        self.model =   # 或你开通的其他模型，如 `qwen3-vl-flash`
        logging.info(f"AI通信器初始化完成，使用模型: {self.model}")

    def get_answer_from_image(self, image_path):
        """调用阿里云视觉模型分析题目图片并返回答案"""
        try:
            # 1. 将本地图片转换为Base64编码
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            # 2. 构建与官方示例完全一致的消息请求
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    # 使用构建好的Data URL
                                    "url": image_data_url
                                },
                            },
                            {
                                "type": "text",
                                "text": "请分析这张图片中的题目（可能是数学公式或文本），并直接给出你认为正确的单个选项答案（例如：'A'， 'B'， 'C' 或 'D'）。如果题目是问答题，请给出最简洁的答案。不要解释原因，只输出答案。"
                            },
                        ],
                    }
                ],
                # 可以添加流式输出或思考过程（可选），首次测试建议保持简单
                # stream=True,
                # extra_body={'enable_thinking': True}
            )

            # 3. 提取AI返回的答案文本
            answer_text = completion.choices[0].message.content
            logging.info(f"AI返回原始答案: {answer_text}")
            return answer_text.strip()

        except Exception as e:
            logging.error(f"AI调用失败: {e}")
            raise