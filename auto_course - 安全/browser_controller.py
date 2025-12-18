from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import logging
import time
class BrowserController:
    def __init__(self, config):
        self.config = config
        self.driver = self._init_browser()
        self.wait = WebDriverWait(self.driver, 1000000)  # 全局等待15秒

    def _init_browser(self):
        """初始化浏览器实例"""
        browser_type = self.config.browser_type
        try:
            if browser_type == "chrome":
                options = webdriver.ChromeOptions()
                options.add_experimental_option("excludeSwitches", ["enable-logging"])
                # 注意：需要先注释掉或删除下面这行旧的自动管理驱动的代码
                # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
                # 替换为指定本地 msedgedriver.exe 的路径
                driver = webdriver.Chrome(options=options)  # Chrome 驱动也改用此方式
            elif browser_type == "firefox":
                # driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
                driver = webdriver.Firefox()  # 同理
            elif browser_type == "edge":  # ！！！新增的 Edge 分支！！！
                # 导入Edge专用的选项类
                from selenium.webdriver.edge.options import Options as EdgeOptions
                from selenium.webdriver.edge.service import Service as EdgeService
                # 指定你已下载的 msedgedriver.exe 的路径
                service = EdgeService(executable_path='./msedgedriver.exe')  # 假设驱动在项目根目录
                options = EdgeOptions()
                # 可以添加一些Edge的特定选项，例如：
                options.add_experimental_option("excludeSwitches", ["enable-logging"])
                driver = webdriver.Edge(service=service, options=options)
            else:
                logging.error(f"不支持的浏览器类型：{browser_type}")
                raise ValueError(f"不支持的浏览器类型：{browser_type}（仅支持chrome/firefox/edge）")  # 更新错误提示
            driver.maximize_window()
            logging.info(f"成功初始化{browser_type}浏览器")
            return driver
        except Exception as e:
            logging.error(f"浏览器初始化失败：{str(e)}")
            raise

    def login(self, url=""):
        """登录智慧树"""
        try:
            self.driver.get(url)
            # 输入用户名
            username_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "lUsername"))
            )
            username_input.clear()
            username_input.send_keys(self.config.username)
            # 输入密码
            password_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "lPassword"))
            )
            password_input.clear()
            password_input.send_keys(self.config.password)
            # 点击登录按钮
            login_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "f_sign_up"))
            )
            login_btn.click()
            # 验证登录成功（等待跳转至首页）
            self.wait.until(
                EC.title_contains("智慧树网")
            )
            logging.info("登录成功")
            time.sleep(2)  # 等待页面加载完成
        except TimeoutException:
            logging.error("登录超时，可能是用户名密码错误或网络问题")
            raise
        except Exception as e:
            logging.error(f"登录失败：{str(e)}")
            raise

    def navigate_to_course(self):
        """导航到目标课程（需用户手动选择或扩展为自动选择指定课程）"""
        # 这里默认导航到"我的课程"页面，如需自动选择课程，可扩展课程名称配置
        try:
            my_course_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '我的课程')]"))
            )
            my_course_btn.click()
            logging.info("已导航到我的课程页面")
            # 提示用户选择课程（可扩展为自动选择指定课程）
            print("请在浏览器中选择需要答题的课程，然后按Enter继续...")
            input()
        except Exception as e:
            logging.error(f"导航到课程失败：{str(e)}")
            raise

    def expand_course_hierarchy(self):
        """展开课程章节层级"""
        try:
            # 定位所有章节展开按钮（根据智慧树实际HTML调整选择器）
            expand_buttons = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "jxtree-switch"))
            )
            for btn in expand_buttons:
                try:
                    if btn.get_attribute("title") == "展开":
                        btn.click()
                        time.sleep(0.5)
                except ElementClickInterceptedException:
                    continue
            logging.info("课程章节层级已展开")
        except Exception as e:
            logging.warning(f"展开章节层级失败（可能已展开）：{str(e)}")

    def click_next_question(self):
        """点击下一题按钮"""
        try:
            next_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".next-topic.next-t.ZHIHUISHU_QZMD"))
            )
            next_btn.click()
            time.sleep(1)
            logging.info("已点击下一题")
        except Exception as e:
            logging.error(f"点击下一题失败：{str(e)}")
            raise

    def click_next_section(self):
        """点击下一节/下一章按钮"""
        try:
            next_section_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".reviewDone.ZHIHUISHU_QZMD"))
            )
            next_section_btn.click()
            time.sleep(2)
            logging.info("已进入下一节")
        except Exception as e:
            logging.error(f"进入下一节失败：{str(e)}")
            raise

    def get_current_proficiency(self):
        """提取当前熟练度百分比"""
        try:
            # 智慧树熟练度通常在class为"progress-num"的元素中
            proficiency_element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".charts-label-rate"))
            )
            proficiency_text = proficiency_element.text.strip().replace("%", "")
            return int(proficiency_text) if proficiency_text.isdigit() else 0
        except Exception as e:
            logging.warning(f"获取熟练度失败：{str(e)}")
            return 0

    def get_question_element(self):
        """获取当前题目区域的HTML元素（用于截图）"""
        try:
            # 智慧树题目区域常见选择器（根据实际页面调整）
            return self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "questionContent"))
            )
        except Exception as e:
            logging.error(f"定位题目区域失败：{str(e)}")
            raise

    def click_option(self, option_index):
        """
        点击指定选项 (A=0, B=1, C=2, D=3)
        option_index: 选项的索引，0代表A，1代表B，以此类推
        """
        try:
            # 找到所有选项图标（返回一个列表）
            option_icons = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".iconfont.checkIcon.fl"))
            )
            # 确保索引有效
            if option_index < len(option_icons):
                option_icons[option_index].click()
                logging.info(f"已点击第 {option_index + 1} 个选项")
            else:
                logging.error(f"选项索引 {option_index} 超出范围")
        except Exception as e:
            logging.error(f"点击选项失败：{str(e)}")
            raise

    def quit(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            logging.info("浏览器已关闭")