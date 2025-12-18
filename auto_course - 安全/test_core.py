import time
from config_loader import Config
from browser_controller import BrowserController

print("=== 核心功能分步测试 ===\n")

# 1. 初始化配置和浏览器
print("步骤1: 正在初始化浏览器...")
config = Config()
browser = BrowserController(config)

# 2. 手动操作提示
print("步骤2: 请现在手动完成以下操作：")
print("  1. 在刚打开的浏览器中登录智慧树。")
print("  2. 进入一个具体的课程。")
print("  3. 进入一个作业页面，确保有一道题显示在屏幕上。")
input("完成以上所有手动操作后，请回到此窗口按【回车键】继续...\n")

# 3. 测试1：检查题目区域是否能找到
print("步骤3: 测试题目区域定位...")
try:
    question_element = browser.get_question_element()
    print("   ✅ 成功！题目区域已定位。")
    print(f"     元素信息: {question_element.tag_name} (class: {question_element.get_attribute('class')})")
except Exception as e:
    print(f"   ❌ 失败！错误信息: {e}")
    print("   **请检查 browser_controller.py 中 ‘get_question_element‘ 方法里的 class 名 ‘questionContent‘ 是否正确。**")
    browser.quit()
    exit()

# 4. 测试2：检查“下一题”按钮是否能找到
print("\n步骤4: 测试‘下一题’按钮定位...")
try:
    # 这里直接使用你修改过的选择器，但先不点击
    from selenium.webdriver.common.by import By # 确保导入了By
    next_btn = browser.wait.until(
        lambda d: d.find_element(By.CSS_SELECTOR, ".next-topic.next-t.ZHIHUISHU_QZMD")
    )
    print("   ✅ 成功！‘下一题’按钮已定位。")
except Exception as e:
    print(f"   ❌ 失败！错误信息: {e}")
    print("   **请检查 browser_controller.py 中 ‘click_next_question‘ 方法里的CSS选择器字符串是否正确。**")
    browser.quit()
    exit()

# 5. 测试3：检查“选项”图标（用于点击答案）是否能找到
print("\n步骤5: 测试选项按钮定位...")
try:
    # 修复：导入By，并使用正确的调用方式
    from selenium.webdriver.common.by import By
    # 查找所有选项图标
    options = browser.driver.find_elements(By.CSS_SELECTOR, ".iconfont.checkIcon.fl")
    print(f"   ✅ 成功！找到 {len(options)} 个选项图标。")
    if len(options) >= 4:
        print("   (这很可能对应A、B、C、D四个选项)")
except Exception as e:
    print(f"   ❌ 失败！错误信息: {e}")
    print("   **请检查选项图标的class是否仍是 ‘.iconfont.checkIcon.fl‘。**")

# 6. 测试4：检查“熟练度”文本是否能找到
print("\n步骤6: 测试熟练度文本定位...")
try:
    # 同样修复导入和调用方式
    prof_element = browser.driver.find_element(By.CSS_SELECTOR, ".charts-label-rate")
    prof_text = prof_element.text
    print(f"   ✅ 成功！找到熟练度文本: ‘{prof_text}‘")
except Exception as e:
    print(f"   ⚠️  警告：未找到熟练度元素。错误: {e}")
    print("   (这可能是因为当前页面不显示熟练度，可以暂时忽略)")

# 7. 最终总结
print("\n" + "="*40)
print("分步测试完成！")
print("✅ 如果步骤3、4、5都成功，说明你的所有核心定位器在当前页面都是有效的！")
print("⚠️  如果任何一步失败，请根据提示修改对应文件中的选择器。")
print("\n下一步行动建议：")
print("1. 保持此浏览器窗口打开，不要关闭。")
print("2. 我们将基于此，编写一个真正自动截图、问AI、答题的脚本。")
input("\n按回车键结束测试并关闭浏览器...")
browser.quit()