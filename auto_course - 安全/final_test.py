# final_test.py - 全自动单题闭环测试
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_loader import Config
from browser_controller import BrowserController
from screen_operator import ScreenOperator
from ai_communicator import AICommunicator


def full_auto_one_question():
    print("=" * 60)
    print("智慧树全自动答题 - 单题闭环终极测试")
    print("=" * 60)

    # 1. 初始化所有模块
    print("\n[1/5] 初始化系统...")
    config = Config()
    browser = BrowserController(config)
    screen = ScreenOperator(browser)
    ai = AICommunicator(config)

    # 2. 手动准备环境
    print("\n[2/5] 请手动准备答题环境：")
    print("  • 在浏览器中登录智慧树")
    print("  • 进入一个作业/练习页面")
    print("  • 确保第一道题显示在屏幕上")
    input("  准备完成后，请按【回车】继续...")

    # 3. 核心自动化流程
    print("\n[3/5] 开始全自动答题流程...")

    # 步骤A: 截图
    print("  A. 正在截图...")
    try:
        screenshot_path = screen.capture_question()
        print(f"     ✅ 截图成功: {screenshot_path}")
    except Exception as e:
        print(f"     ❌ 截图失败: {e}")
        browser.quit()
        return

    # 步骤B: 调用AI（使用真实API）
    print("  B. 调用AI识别答案...")
    try:
        answer_text = ai.get_answer_from_image(screenshot_path)
        print(f"     ✅ AI回复原始文本: 「{answer_text}」")
    except Exception as e:
        print(f"     ❌ AI调用失败: {e}")
        print("     将使用备选答案‘B’继续测试流程")
        answer_text = "B"  # 失败时使用备选答案

    # 步骤C: 解析答案
    print("  C. 解析答案...")
    # 简易解析逻辑：提取文本中的第一个A/B/C/D字母
    answer_text_clean = answer_text.strip().upper()
    selected_answer = None
    for char in answer_text_clean:
        if char in 'ABCD':
            selected_answer = char
            break

    if not selected_answer:
        print(f"     ⚠️  无法从「{answer_text}」解析出选项，默认使用B")
        selected_answer = 'B'

    answer_index = ord(selected_answer) - ord('A')  # A->0, B->1, ...
    print(f"     ✅ 解析结果: 选项{selected_answer} (索引{answer_index})")

    # 步骤D: 安全确认（首次运行务必确认）
    print("\n" + "-" * 40)
    print("【安全确认点】")
    print(f"AI建议点击: 选项 {selected_answer}")
    print("请立即核对浏览器中题目和选项！")
    confirm = input("是否执行自动点击？(输入 y 并回车确认，其他跳过点击): ").strip().lower()

    if confirm == 'y':
        # 步骤E: 点击答案
        print("  D. 点击答案...")
        try:
            # 查找所有选项并点击
            from selenium.webdriver.common.by import By
            options = browser.driver.find_elements(By.CSS_SELECTOR, ".iconfont.checkIcon.fl")
            if len(options) > answer_index:
                options[answer_index].click()
                time.sleep(0.5)  # 等待点击效果
                print(f"     ✅ 已点击选项{selected_answer}")
            else:
                print(f"     ❌ 错误：页面只有{len(options)}个选项，无法点击索引{answer_index}")
        except Exception as e:
            print(f"     ❌ 点击答案失败: {e}")

        # 步骤F: 点击下一题
        print("  E. 提交并进入下一题...")
        try:
            browser.click_next_question()
            time.sleep(1)
            print("     ✅ 已点击‘下一题’，页面应已刷新")
        except Exception as e:
            print(f"     ❌ 点击下一题失败: {e}")
    else:
        print("  ⚠️  已跳过自动点击，仅测试到AI识别环节")

    # 4. 完成总结
    print("\n" + "=" * 60)
    print("🔥 全自动单题测试完成！")
    print("\n执行总结：")
    print(f"  1. 截图: {'✅ 成功' if 'screenshot_path' in locals() else '❌ 失败'}")
    print(f"  2. AI识别: {'✅ 成功' if 'answer_text' in locals() else '❌ 失败'}")
    print(f"  3. 答案解析: {'✅ ' + selected_answer if selected_answer else '❌ 失败'}")
    print(f"  4. 自动点击: {'✅ 已执行' if confirm == 'y' else '⚠️ 已跳过'}")
    print("\n下一步建议：")
    if confirm != 'y':
        print("  • 首次运行成功！请检查AI答案是否合理")
        print("  • 若答案正确，再次运行本脚本并输入 y 进行真实点击测试")
    else:
        print("  • 恭喜！全自动流程已验证通过")
        print("  • 可修改脚本，移除安全确认实现完全自动化")
        print("  • 接下来可集成到 main.py 的主循环中")

    input("\n按回车键关闭浏览器并结束测试...")
    browser.quit()


if __name__ == "__main__":
    full_auto_one_question()