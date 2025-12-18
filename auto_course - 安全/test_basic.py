from config_loader import Config
from browser_controller import BrowserController
import time

config = Config()
bc = BrowserController(config)


# 如果不想自动登录，可以注释掉上一行，手动登录

# 2. 手动操作：请在此处手动登录并导航到具体的作业页面
print("请手动登录智慧树，并打开一个包含题目的作业页面，然后回到这里...")
input("完成后按回车键继续...")

# 3. 测试获取当前URL和标题（验证浏览器对象可用）
print(f"当前页面标题: {bc.driver.title}")
print(f"当前页面URL: {bc.driver.current_url}")
print("基础测试通过！浏览器控制对象工作正常。")
input("按回车键关闭浏览器...")

bc.quit()