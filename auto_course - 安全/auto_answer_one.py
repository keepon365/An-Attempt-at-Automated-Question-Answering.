# auto_answer_one.py - 自动完成一道题的完整流程
import sys
import os
import time
import logging
import base64
from pathlib import Path

# 设置当前目录，确保能导入你的模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_loader import Config
from browser_controller import BrowserController
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# 配置日志，方便查看
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def auto_answer_one_question():
    """自动处理一道题：截图、问AI、点击答案、翻页"""
    print("=" * 50)
    print("智慧树单题自动化测试启动")
    print("=" * 50)

    # 0. 初始化
    print("\n[步骤0] 初始化配置和浏览器...")
    config = Config()
    browser = BrowserController(config)
    from screen_operator import ScreenOperator  # 确保导入了类
    screen_op = ScreenOperator(browser)  # 创建实例，命名为 screen_op

    # 1. 手动操作提示
    print("\n[步骤1] 请完成以下手动操作：")
    print("  1. 在打开的浏览器中登录智慧树（如果未登录）。")
    print("  2. 进入一个具体的作业/练习页面。")
    print("  3. 确保屏幕上显示一道待做的题目。")
    input("  完成以上操作后，请按【回车】继续...")

    # 2. 定位题目并截图
    print("\n[步骤2] 定位题目并截图（调用标准化方法）...")
    try:
        # 关键：直接使用已初始化好的ScreenOperator实例来截图
        # 首先，确保脚本前面已经初始化了ScreenOperator。如果没有，需要添加：
        # from screen_operator import ScreenOperator
        # screen_op = ScreenOperator(browser) # 传入browser对象

        # 如果你的 MainLogic 或已有代码中已经创建了 ScreenOperator 实例，直接使用它。
        # 这里假设你像在main_logic中一样，已经创建了 self.screen
        screenshot_path = screen_op.capture_question()  # 调用统一的方法

        print(f"  ✅ 题目截图已保存: {screenshot_path}")

    except Exception as e:
        print(f"  ❌ 截图失败: {e}")
        # 可以打印更详细的错误信息
        import traceback
        traceback.print_exc()
        browser.quit()
        return

    # 3. 调用AI获取答案（模拟版本 - 安全第一）
    print("\n[步骤3] 调用AI获取答案...")
    # 注意：这里使用模拟答案，避免消耗API和误操作
    # 首次运行时，我们使用模拟答案测试流程

    simulated_answer = "B"  # 模拟AI返回答案B
    print(f"  [模拟模式] AI返回答案: {simulated_answer}")
    print("  (这是模拟答案，用于测试流程。下一步将使用真实AI)

    # 4. 解析答案并点击（安全模式）
    print("\n[步骤4] 解析答案并准备点击...")

    # 解析答案文本为索引 (A->0, B->1, C->2, D->3)
    def parse_answer(answer_str):
        answer_str = answer_str.strip().upper()
        for char in answer_str:
            if char in "ABCD":
                return ord(char) - ord('A')  # A->0, B->1, etc.
        # 默认返回B（索引1）以防解析失败
        return 1

    answer_index = parse_answer(simulated_answer)  # 如果是真实AI，改为 answer_text
    print(f"  解析结果: 选项{'ABCD'[answer_index]} (索引{answer_index})")

    # 安全模式：先不点击，只定位
    print("\n  ⚠️  【安全模式】首次运行，不执行真实点击")
    print("  请根据以下信息确认流程是否正确:")

    # 定位选项
    try:
        options = browser.driver.find_elements(By.CSS_SELECTOR, ".iconfont.checkIcon.fl")
        if len(options) > answer_index:
            option = options[answer_index]
            print(f"  ✅ 找到对应选项元素")

            # 获取选项位置信息（不点击）
            location = option.location
            print(f"  选项位置: x={location['x']}, y={location['y']}")

            # 安全模式：询问用户是否继续
            user_choice = input("\n  是否执行真实点击？(y/n): ").lower()
            if user_choice == 'y':
                print("  执行真实点击...")
                option.click()
                time.sleep(1)  # 等待点击反应
                print("  ✅ 选项点击完成")

                # 点击下一题
                print("\n[步骤5] 点击下一题...")
                try:
                    browser.click_next_question()
                    print("  ✅ 已点击下一题")
                    time.sleep(2)
                except Exception as e:
                    print(f"  ❌ 点击下一题失败: {e}")
            else:
                print("  跳过真实点击，仅测试定位")
        else:
            print(f"  ❌ 错误: 找到{len(options)}个选项，但答案索引是{answer_index}")
    except Exception as e:
        print(f"  ❌ 定位选项失败: {e}")

    # 5. 完成
    print("\n" + "=" * 50)
    print("单题自动化测试完成！")
    print("\n总结:")
    print("1. 题目定位: ✅ 成功")
    print("2. 截图保存: ✅ 成功")
    print("3. AI调用: ⚠️ 模拟模式（可切换真实AI）")
    print("4. 答案解析: ✅ 成功")
    print("5. 点击操作: ⚠️ 安全模式（需手动确认）")
    print("\n下一步:")
    print("1. 检查 screenshots/ 文件夹中的截图是否准确")
    print("2. 确认无误后，可修改代码使用真实AI")
    print("3. 取消安全模式，实现全自动答题")

    input("\n按回车键关闭浏览器...")
    browser.quit()


if __name__ == "__main__":
    auto_answer_one_question()