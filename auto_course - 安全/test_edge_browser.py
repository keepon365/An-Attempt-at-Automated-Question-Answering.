# test_edge_browser.py
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 指定 msedgedriver.exe 的路径（如果已放在项目根目录，直接写名字即可）
driver_path = './msedgedriver.exe'
service = Service(executable_path=driver_path)


# 启动浏览器
driver = webdriver.Edge(service=service, options=options)

print("Edge浏览器已启动。请手动登录智慧树，并进入一个作业页面。")
print("然后，你需要按F12打开开发者工具，侦察页面元素。")
input("完成后，请回到此命令行窗口按回车键，浏览器将关闭...")

driver.quit()