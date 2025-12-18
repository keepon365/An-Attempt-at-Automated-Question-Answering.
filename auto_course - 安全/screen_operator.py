import pyautogui
import os
import logging
from PIL import Image
import time

class ScreenOperator:
    def __init__(self, browser_controller):
        self.browser = browser_controller
        self.screenshot_dir = "screenshots"
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
        # 设置pyautogui失败安全（移动到屏幕角落时抛出异常）
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5  # 每次操作后暂停0.5秒

    def capture_question(self):
        """截取当前题目区域的截图（使用Selenium内置方法，最准确）"""
        import time
        import os
        import logging

        try:
            # 1. 通过浏览器控制器获取题目元素
            question_element = self.browser.get_question_element()

            # 2. 确保截图目录存在
            if not os.path.exists(self.screenshot_dir):
                os.makedirs(self.screenshot_dir)

            # 3. 生成唯一的文件名
            timestamp = int(time.time())
            screenshot_path = os.path.join(self.screenshot_dir, f"question_{timestamp}.png")

            # 4. 【核心改动】使用Selenium直接对元素截图，无需坐标计算
            question_element.screenshot(screenshot_path)

            logging.info(f"题目截图已保存：{screenshot_path}")
            print(f"[调试] 截图成功，路径：{screenshot_path}")  # 添加打印以便实时查看
            return screenshot_path

        except Exception as e:
            logging.error(f"截图失败：{str(e)}")
            # 打印更详细的错误信息，帮助调试
            print(f"[错误] 截图过程中发生异常：{e}")
            raise

    def locate_and_click_option(self, option_text):
        """根据选项文本定位并点击答案（支持A/B/C/D或文本选项）"""
        try:
            logging.info(f"正在查找选项：{option_text}")
            # 简化方案：如果是A/B/C/D，直接点击对应选项（智慧树选项通常有固定位置）
            if option_text.strip().upper() in ["A", "B", "C", "D"]:
                self._click_option_by_letter(option_text.upper())
                return
            # 进阶方案：通过图像识别查找选项文本（需提前准备选项模板图，此处简化）
            # 这里使用pyautogui的像素匹配（实际使用时建议结合OpenCV提升准确率）
            screen_width, screen_height = pyautogui.size()
            # 只在屏幕中间区域查找（避免干扰）
            search_region = (screen_width//4, screen_height//3, screen_width//2, screen_height//3)
            # 此处简化为模拟点击（实际需替换为图像识别逻辑）
            logging.warning("文本选项识别暂未实现，模拟点击第一个选项")
            pyautogui.click(search_region[0] + 50, search_region[1] + 50)
        except Exception as e:
            logging.error(f"点击选项失败：{str(e)}")
            raise

    def _click_option_by_letter(self, letter):
        """根据选项字母（A/B/C/D）点击对应位置"""
        try:
            # 获取题目区域坐标，计算选项位置（智慧树选项通常在题目下方，垂直排列）
            question_element = self.browser.get_question_element()
            location = question_element.location
            size = question_element.size
            browser_window = self.browser.driver.get_window_position()
            # 选项起始位置（在题目下方）
            option_y = browser_window["y"] + location["y"] + size["height"] + 30
            option_x = browser_window["x"] + location["x"] + 50
            # 选项间隔（每个选项约50像素）
            option_index = {"A": 0, "B": 1, "C": 2, "D": 3}[letter]
            target_y = option_y + option_index * 50
            # 点击选项（点击字母左侧的单选框位置）
            pyautogui.click(option_x, target_y)
            logging.info(f"已点击选项：{letter}（坐标：{option_x}, {target_y}）")
            # 点击提交按钮（智慧树部分题目需手动提交）
            self._click_submit_button()
        except Exception as e:
            logging.error(f"点击字母选项失败：{str(e)}")
            raise

    def _click_submit_button(self):
        """点击提交按钮"""
        try:
            # 智慧树提交按钮常见XPath
            submit_btn_xpath = "//button[contains(text(), '提交') or contains(text(), '确认')]"
            # 先尝试通过Selenium点击（更准确）
            try:
                submit_btn = self.browser.wait.until(
                    EC.element_to_be_clickable((By.XPATH, submit_btn_xpath))
                )
                submit_btn.click()
            except:
                # Selenium点击失败时，使用pyautogui点击屏幕下方中间位置
                screen_width, screen_height = pyautogui.size()
                pyautogui.click(screen_width//2, screen_height//2 + 200)
            logging.info("已提交答案")
            time.sleep(1)
        except Exception as e:
            logging.warning(f"提交按钮点击失败（可能无需手动提交）：{str(e)}")