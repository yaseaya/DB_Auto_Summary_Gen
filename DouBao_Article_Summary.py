# 导入必要的库
from selenium import webdriver  # 导入Selenium库以控制浏览器
from selenium.webdriver.common.by import By  # 导入用于定位元素的By类
from selenium.webdriver.common.action_chains import ActionChains  # 导入用于执行复杂用户操作的ActionChains类
from selenium.webdriver.chrome.service import Service  # 导入Chrome服务类
from selenium.webdriver.chrome.options import Options  # 导入Chrome选项类
import pyperclip  # 导入pyperclip库以处理剪贴板
import time  # 导入time库以处理时间延迟
import getpass  # 导入getpass库以获取当前用户名
import os

def main(file_path):  # 增加_main_函数，接收file_path作为参数
    print('########################## 【豆包总结 】脚本开始 ##########################')

    if not os.path.exists(file_path):
        print(f"{file_path} Not existed, please check the correct file")
        return
    else:
        print(f"{file_path} Existed, continue")

    # 获取当前用户名并设置Chrome用户数据目录路径
    username = getpass.getuser()  # 获取当前系统用户名
    user_profile_path = r'C:\Users\%s\AppData\Local\Google\Chrome\User Data' % username  # 设置Chrome用户数据目录路径
    print(user_profile_path)  # 打印用户数据目录路径

    # 配置Chrome选项
    options = Options()  # 创建Chrome选项对象
    options.add_argument(f"user-data-dir={user_profile_path}")  # 添加用户数据目录选项
    options.add_argument('--ignore-ssl-errors=yes')  # 忽略SSL错误
    options.add_argument('--ignore-certificate-errors')  # 忽略证书错误

    # 等待5秒
    time.sleep(3)  # 暂停5秒以确保设置生效

    # 使用配置的选项初始化WebDriver
    driver = webdriver.Chrome(options=options)  # 初始化Chrome浏览器驱动

    try:
        # 打开豆包AI的聊天页面
        driver.get('https://www.doubao.com/chat/')  # 访问豆包AI聊天页面

        # 等待页面加载
        time.sleep(2)  # 暂停2秒以等待页面加载完成

        # 点击"新对话"按钮
        element_to_click = driver.find_element(By.XPATH, "//*[text()='新对话']")  # 定位"新对话"按钮
        actions = ActionChains(driver)  # 创建动作链
        actions.move_to_element(element_to_click).click().perform()  # 移动到按钮并点击

        # 点击"阅读总结"按钮
        element_to_click = driver.find_element(By.XPATH, "//*[text()='阅读总结']")  # 定位"阅读总结"按钮
        actions = ActionChains(driver)  # 创建新的动作链
        actions.move_to_element(element_to_click).click().perform()  # 移动到按钮并点击

        # 等待操作完成
        time.sleep(2)  # 暂停2秒以等待操作完成

        # 上传文件
        driver.find_element(By.XPATH, "//input[@type='file']").send_keys(file_path)  # 定位文件上传输入框并上传文件

        # 在提示词输入框中输入文本
        iuput_field = driver.find_element(By.CSS_SELECTOR, "[data-testid='chat_input_input']")  # 定位输入框
        iuput_field.send_keys("详细整理这篇文档，输出格式清晰的总结")  # 输入提示词

        # 等待发送按钮变为可用状态
        element_to_click = driver.find_element(By.ID, "flow-end-msg-send")  # 定位发送按钮
        is_disabled = True  # 初始化按钮状态为禁用
        while is_disabled:  # 循环直到按钮可用
            try:
                time.sleep(1)  # 暂停1秒
                print("发送按钮 状态： " + str(element_to_click.is_enabled()))  # 打印按钮状态
                is_disabled = not element_to_click.is_enabled()  # 更新按钮状态
            except:
                print("except: 状态变化的时候，element 会变化报错")  # 捕获异常并打印错误信息
                break  # 跳出循环

        # 点击发送按钮
        element_to_click = driver.find_element(By.ID, "flow-end-msg-send")  # 重新定位发送按钮
        actions = ActionChains(driver)  # 创建新的动作链
        actions.move_to_element(element_to_click).click().perform()  # 移动到按钮并点击

        # 等待生成完成
        generating = True  # 初始化生成状态为进行中
        while generating:  # 循环直到生成完成
            try:
                element_to_click = driver.find_element(By.CSS_SELECTOR, "[data-testid='message_action_copy']")  # 定位复制按钮
                generating = False  # 更新生成状态为完成
            except:
                time.sleep(5)  # 暂停5秒以等待生成完成

        # 点击复制按钮
        actions = ActionChains(driver)  # 创建新的动作链
        actions.move_to_element(element_to_click).click().perform()  # 移动到复制按钮并点击

        # 获取剪贴板内容
        clipboard_content = pyperclip.paste()  # 从剪贴板获取内容

        # 打印剪贴板内容
        print(clipboard_content)  # 打印剪贴板内容

        ###########################################################
        # 在提示词输入框中输入文本
        time.sleep(5)  # 暂停5秒以等待用户查看结果
        iuput_field = driver.find_element(By.CSS_SELECTOR, "[data-testid='chat_input_input']")  # 定位输入框
        iuput_field.send_keys("再详细点")  # 输入新的提示词

        # 点击发送按钮
        time.sleep(2)  # 暂停2秒以等待输入完成
        element_to_click = driver.find_element(By.ID, "flow-end-msg-send")  # 重新定位发送按钮
        actions = ActionChains(driver)  # 创建新的动作链
        actions.move_to_element(element_to_click).click().perform()  # 移动到按钮并点击
        print("发送按钮 再次点击")  # 打印发送按钮点击信息

        # 等待生成完成
        time.sleep(2)  # 暂停2秒以等待生成完成
        generating = True  # 初始化生成状态为进行中
        while generating:  # 循环直到生成完成
            try:
                regenerate_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='message_action_regenerate']")  # 定位重新生成按钮
                generating = False  # 更新生成状态为完成
            except:
                print("except: 状态变化的时候，element 会变化报错")  # 捕获异常并打印错误信息
                time.sleep(5)  # 暂停5秒以等待生成完成

        copy_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='message_action_copy']")  # 定位复制按钮

        # 等待5秒
        # 点击复制按钮
        actions = ActionChains(driver)  # 创建新的动作链
        actions.move_to_element(copy_button).click().perform()  # 移动到复制按钮并点击

        # 获取剪贴板内容
        clipboard_content = pyperclip.paste()  # 从剪贴板获取内容

        # 打印剪贴板内容
        print(clipboard_content)  # 打印剪贴板内容

        # 等待10秒
        time.sleep(5)  # 暂停10秒以等待用户查看结果

        # 将内容写入文件
        with open("sample.txt", "w", encoding="utf-8") as file:  # 打开文件以写入
            file.write(clipboard_content)  # 将剪贴板内容写入文件

    finally:
        # 脚本结束
        driver.quit()  # 关闭浏览器驱动
        # 等待10秒
        print('########################## 【豆包总结 】脚本结束 ##########################')
        print('Waiting for messages. To exit press CTRL+C')
        time.sleep(15)  # 暂停10秒以释放资源

# 如果该文件作为主程序运行，则调用main函数
# if __name__ == "__main__":
#     file_name = "20240517_AA.txt"  # 当前要处理的文件名
#     file_path = r'D:\My.Dev\Job_MessageQuene\SampleTxt\%s' % file_name  # 设置文件的完整路径
#     main(file_path)  # 调用main函数
