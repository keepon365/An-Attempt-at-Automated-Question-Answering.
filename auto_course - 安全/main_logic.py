import logging
import json
import os
import time
from browser_controller import BrowserController
from screen_operator import ScreenOperator
from ai_communicator import AICommunicator

class MainLogic:
    def __init__(self, config):
        self.config = config
        self.browser = BrowserController(config)
        self.screen = ScreenOperator(self.browser)
        self.ai = AICommunicator(config)
        self.failures_file = "failures.json"
        # 初始化失败记录文件
        if not os.path.exists(self.failures_file):
            with open(self.failures_file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _parse_answer_to_index(self, answer_text):
        """
        将AI返回的答案文本解析为点击索引 (A->0, B->1, C->2, D->3)

        参数:
            answer_text: AI返回的原始文本，例如 “B”、“答案是C”、“我认为选A”

        返回:
            int: 选项索引 (0, 1, 2, 3)

        抛出:
            ValueError: 当无法从文本中解析出有效选项时
        """
        import re
        import logging

        if not answer_text:
            raise ValueError("AI返回的答案文本为空")

        # 统一转为大写，方便处理
        answer_text_upper = answer_text.strip().upper()
        logging.debug(f"开始解析答案文本: '{answer_text}' -> '{answer_text_upper}'")

        # 方案1: 直接匹配单个字母 A, B, C, D
        if answer_text_upper in ['A', 'B', 'C', 'D']:
            index = ord(answer_text_upper) - ord('A')
            logging.info(f"解析方案1-直接匹配: '{answer_text_upper}' -> 索引 {index}")
            return index

        # 方案2: 使用正则表达式查找文本中的第一个选项字母
        # 匹配模式示例: “A”, “选项B”, “答案是C”, “选D”, “(A)”, “[B]”
        pattern = r'[ABCD]'
        match = re.search(pattern, answer_text_upper)
        if match:
            matched_char = match.group()
            index = ord(matched_char) - ord('A')
            logging.info(f"解析方案2-正则匹配: 从 '{answer_text_upper}' 中提取到 '{matched_char}' -> 索引 {index}")
            return index

        # 方案3: 处理一些常见的中文表述
        answer_map = {
            "第一个选项": 0, "选项一": 0, "选项1": 0,
            "第二个选项": 1, "选项二": 1, "选项2": 1,
            "第三个选项": 2, "选项三": 2, "选项3": 2,
            "第四个选项": 3, "选项四": 3, "选项4": 3,
        }
        for key, idx in answer_map.items():
            if key in answer_text_upper:
                logging.info(f"解析方案3-中文映射: '{key}' -> 索引 {idx}")
                return idx

        # 所有方案都失败
        error_msg = f"无法从AI返回的文本中解析出有效选项: '{answer_text}'"
        logging.error(error_msg)
        raise ValueError(error_msg)

    def process_one_question(self):
        """处理一道题目：截图->问AI->点击答案->提交"""
        try:
            # 1. 截图题目
            screenshot_path = self.screen.capture_question()
            # 2. 调用AI获取答案
            answer = self.ai.get_answer_from_image(screenshot_path)
            # 3. 点击答案选项
            self.screen.locate_and_click_option(answer)
            # 4. 点击下一题
            self.browser.click_next_question()
            logging.info("单题处理完成")
            return True
        except Exception as e:
            logging.error(f"单题处理失败：{str(e)}")
            return False

    def process_one_course_section(self):
        """处理一个课程章节（循环答题直到达到目标熟练度）"""
        current_section = self._get_current_section_title()
        logging.info(f"开始处理章节：{current_section}")
        retry_count = 0
        while retry_count < self.config.max_retries:
            # 获取当前熟练度
            current_proficiency = self.browser.get_current_proficiency()
            logging.info(f"当前熟练度：{current_proficiency}%，目标：{self.config.target_proficiency}%")
            if current_proficiency >= self.config.target_proficiency:
                logging.info(f"章节{current_section}熟练度达标，进入下一节")
                return True
            # 循环处理本节题目（默认最多10道题）
            for _ in range(10):
                success = self.process_one_question()
                if not success:
                    break
            # 重试计数+1
            retry_count += 1
            logging.warning(f"章节{current_section}第{retry_count}次尝试未达标")
        # 多次重试未达标，记录失败
        self._record_failure(current_section)
        logging.error(f"章节{current_section}经{self.config.max_retries}次尝试仍未达标，已跳过")
        return False

    def _get_current_section_title(self):
        """获取当前章节标题（简化实现）"""
        try:
            title_element = self.browser.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "curr-chapter"))
            )
            return title_element.text.strip()
        except:
            return f"未知章节_{int(time.time())}"

    def _record_failure(self, section_title):
        """记录未达标的章节"""
        try:
            with open(self.failures_file, "r", encoding="utf-8") as f:
                failures = json.load(f)
            failures.append({
                "section": section_title,
                "timestamp": int(time.time()),
                "reason": f"经{self.config.max_retries}次尝试未达到目标熟练度{self.config.target_proficiency}%"
            })
            with open(self.failures_file, "w", encoding="utf-8") as f:
                json.dump(failures, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"记录失败章节失败：{str(e)}")
