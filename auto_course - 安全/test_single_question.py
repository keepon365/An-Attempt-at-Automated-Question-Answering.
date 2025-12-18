# test_single_question.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_loader import Config
from browser_controller import BrowserController
from screen_operator import ScreenOperator
from ai_communicator import AICommunicator
import time
import logging

logging.basicConfig(level=logging.INFO)


def test_single_question_cycle():
    """测试单道题的完整处理周期"""
    config = Config()
    # 重要：这里不新建浏览器，而是使用已有浏览器对象（需调整）
    # 为了测试，我们可以先简单初始化，但后续需手动附加到已打开浏览器
    browser = BrowserController(config)

    # 初始化操作器和AI
    # 注意：ScreenOperator可能需要driver对象，调整其__init__或传入driver
    operator = ScreenOperator(browser.driver)
    ai = AICommunicator(config)

    print("=== 单题全流程测试开始 ===")

    # 【第1步：手动前置操作】
    print("请手动操作浏览器，确保停留在一道待做的题目页面，然后按回车继续...")
    input()

    # 【第2步：定位题目并截图】
    print("正在定位题目区域...")
    try:
        question_element = browser.get_question_element()
        print(f"题目区域定位成功，开始截图...")
        screenshot_path = operator.capture_element(question_element)  # 需实现此方法
        print(f"截图已保存至: {screenshot_path}")
    except Exception as e:
        print(f"题目定位或截图失败: {e}")
        return

    # 【第3步：调用AI获取答案】
    print("正在调用AI识别答案...")
    try:
        # 先使用模拟答案进行安全测试，避免消耗API和误点击
        # simulated_answer = "B"  # 模拟AI返回
        # answer_text = simulated_answer

        # 真实调用AI（准备好后取消注释）
        answer_text = ai.get_answer_from_image(screenshot_path)
        print(f"AI返回的原始答案文本: {answer_text}")
    except Exception as e:
        print(f"AI调用失败: {e}")
        return

    # 【第4步：解析并点击答案】
    print("正在解析并准备点击答案...")
    # 将AI返回的文本（如“B”、“C”）解析为点击索引（0, 1, 2, 3）
    # 你需要一个函数 answer_text_to_index 来处理各种情况
    try:
        answer_index = answer_text_to_index(answer_text)  # 需实现此函数
        print(f"解析出的答案索引: {answer_index} (对应选项{'ABCD'[answer_index]})")

        # 【安全模式】首次运行，先注释掉点击，仅打印
        print(f"[安全模式] 应点击的答案索引: {answer_index}")
        # browser.click_option(answer_index)  # 首次测试先注释这行！
    except Exception as e:
        print(f"答案解析失败: {e}")
        return

    # 【第5步：提交并验证】
    print("正在提交答案...")
    try:
        # 同样可以先注释，仅测试翻页
        print("[安全模式] 应点击‘下一题’按钮")
        # browser.click_next_question()  # 首次测试先注释！
        print("提交/翻页成功（模拟）。")
    except Exception as e:
        print(f"提交失败: {e}")
        return

    print("=== 单题流程测试完成（安全模式）===")
    print("请检查以上日志。若一切符合预期，可逐步取消注释进行真实点击测试。")


def answer_text_to_index(answer_text):
    """将AI返回的文本转换为选项索引 (A->0, B->1, ...)"""
    # 这是一个简单的实现示例，你可能需要根据AI返回的实际情况增强
    answer_text = answer_text.strip().upper()
    if answer_text in ["A", "B", "C", "D"]:
        return ord(answer_text) - ord('A')  # A->0, B->1
    # 处理其他情况，如"选项B"、"答案是C"
    for char in answer_text:
        if char in ["A", "B", "C", "D"]:
            return ord(char) - ord('A')
    raise ValueError(f"无法从文本 '{answer_text}' 中解析出答案选项")


if __name__ == "__main__":
    test_single_question_cycle()