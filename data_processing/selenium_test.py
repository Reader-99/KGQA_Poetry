# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/1/25 25:25
 @Author: Glimmering
 @Function: 使用selenium自动化测试框架抓取动态加载的信息
"""

import random
import re
import time

import cv2
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 模拟键盘操作
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium.webdriver import ActionChains
import os
import json
from PIL import Image
# from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

Root = r"D:\6.3 PythonCodes_PyCharm\PythonCodes_ExtraClass\PythonSpider\data"  # 存取文件根目录


# 1、加载指定页面并进行关闭
def loading_page():
    path = Root + r'\test.png'
    # 打开指定（chrome）浏览器
    browser = webdriver.Chrome()
    # 指定加载页面
    browser.get("http://www.baidu.com/")
    # 通过name属性选择文本框元素，并设置内容
    browser.find_element(By.NAME, 'wd').send_keys("selenium")
    # 通过通过ID属性获取“百度一下”按钮，并执行点击操作
    browser.find_element(By.ID, "su").click()
    # 提取页面
    print(browser.page_source.encode('utf-8'))
    # 提取cookie
    print(browser.get_cookies())
    # 获取当前页面截屏
    print(browser.get_screenshot_as_file(path))
    # 提取当前请求地址
    print(browser.current_url)

    # 设置五秒后执行下一步
    time.sleep(10)
    # 关闭浏览器
    browser.quit()


# 2、settings
def loading_and_settings():
    # 启动并打开指定页面
    options = webdriver.ChromeOptions()

    # 不加载图片
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # options.add_experimental_option("prefs", prefs)

    # 无头模式 在后台运行
    # options.add_argument("-headless")

    # 通过设置user-agent
    headers = 'user-agent=%s' % UserAgent().random
    options.add_argument(headers)
    # user_ag = 'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22;CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'

    # 隐藏"Chrome正在受到自动软件的控制"
    # options.add_experimental_option('useAutomationExtension', False)  # 去掉开发者警告
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 拓展使用
    # extension_path = r'E:\BaiduNetdiskDownload\Chrome插件\iguge_2011\igg_2.0.11.crx'
    # options.add_extension(extension_path)

    # 设置代理
    # options.add_argument("--proxy-server=http://58.20.184.187:9091")

    # 初始化配置
    log_url = "https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx"
    browser = webdriver.Chrome(options)
    browser.maximize_window()
    browser.get(log_url)
    wait = WebDriverWait(browser, 5)  # 等待加载页面 5 秒

    # 将浏览器最大化显示

    # 设置宽高
    # browser.set_window_size(480, 800)

    # 通过js新打开一个窗口
    # browser.execute_script('window.open("http://httpbin.org/ip");')
    # time.sleep(10)

    return browser, wait


# 3、提取单节点、多节点
def find_element():
    browser, wait = loading_and_settings()
    # 通过name属性选择文本框元素，并设置内容
    s = browser.find_element(by=By.NAME, value='wd')
    s.send_keys('衣服')
    s.send_keys(Keys.ENTER)  # 回车 确定的意思
    # s.clear()   # 清除输入

    # 各类节点的查找
    """
    # ID选择器定位
    input_text = browser.find_element(By.ID, "kw")
    input_text.send_keys("selenium")

    # CSS 选择器定位
    s = browser.find_element(By.CSS_SELECTOR, 'input.s_ipt')
    s.send_keys('衣服')

    # xpath 选择器定位
    s = browser.find_element(By.XPATH, '//input[@id="kw"]')
    s.send_keys('衣服')
    """

    # 切换 iframe
    """
    browser.get('https://www.douban.com/')
    login_iframe = browser.find_element(By.XPATH,'//div[@class="login"]/iframe')
    browser.switch_to.frame(login_iframe)
    browser.find_element(By.CLASS_NAME,'account-tab-account').click()  # 点击
    browser.find_element(By.ID,'username').send_keys('123123123')"""

    time.sleep(10)
    browser.quit()


# 4、动作链 拖拽
def drag_drop():
    browser = webdriver.Chrome()
    url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
    browser.get(url)
    log = browser.find_element(By.XPATH, '//div[@id="iframewrapper"]/iframe')
    browser.switch_to.frame(log)
    source = browser.find_element(By.ID, "draggable")  # 使用 ID 更好定位
    target = browser.find_element(By.ID, "droppable")
    actions = ActionChains(browser)
    actions.drag_and_drop(source, target)
    actions.perform()

    time.sleep(20)


# 5、页面滚动
def page_scroll():
    # 浏览器滚动到底部 10000位置
    """
    document.documentElement.scrollTop = 10000
    # 滚动到顶部
    document.documentElement.scrollTop = 0

    # 移动到页面最底部
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    # 移动到指定的坐标(相对当前的坐标移动)
    driver.execute_script("window.scrollBy(0, 700)")
    # 结合上面的scrollBy语句，相当于移动到700+800=1600像素位置
    driver.execute_script("window.scrollBy(0, 800)")

    # 移动到窗口绝对位置坐标，如下移动到纵坐标1600像素位置
    driver.execute_script("window.scrollTo(0, 1600)")
    # 结合上面的scrollTo语句，仍然移动到纵坐标1200像素位置
    driver.execute_script("window.scrollTo(0, 1200)")"""
    browser = webdriver.Chrome()
    # url = "https://blog.csdn.net/m0_52336378/article/details/131470901?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522170493521316800182172110%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=170493521316800182172110&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-2-131470901-null-null.142^v99^control&utm_term=selenium%E5%AE%9E%E6%88%98&spm=1018.2226.3001.4187"
    url = "'https://36kr.com/'"
    browser.get(url)
    # scrollTo  不叠加 200 200    scrollBy 叠加  200 300  500操作
    # 慢慢的下拉
    for i in range(1, 100):
        time.sleep(random.randint(100, 300) / 1000)
        browser.execute_script('window.scrollTo(0,{})'.format(i * 100))  # scrollTo 不叠加 700 1400 2100


# 6、获取属性名
def get_attribute():
    # browser = webdriver.Chrome()
    # url = 'https://pic.netbian.com/4kmeinv/index.html'
    # browser.get(url)
    # wait = WebDriverWait(browser, 10)
    # src = browser.find_elements(By.XPATH, '//ul[@class="clearfix"]/li/a/img')
    # for i in src:
    #     url = i.get_attribute('src')
    #     print(url)

    # 访问加载等待，并执行相应的检查
    """
    browser = webdriver.Chrome()
    browser.get('https://www.baidu.com/')
    wait = WebDriverWait(browser, 10)
    input = wait.until(EC.presence_of_element_located((By.ID, 'kw')))
    button = wait.until(EC.element_to_be_clickable((By.ID, 'su')))
    print(input, button)"""

    # 选项卡管理
    browser = webdriver.Chrome()
    browser.get('https://www.baidu.com')
    browser.execute_script('window.open()')
    print(browser.window_handles)
    browser.switch_to.window(browser.window_handles[1])

    browser.get('https://www.baidu.com')
    time.sleep(3)
    browser.switch_to.window(browser.window_handles[0])
    browser.get('https://pic.netbian.com')


# 7、获取登录界面的 cookies
def get_cookies():
    browser, wait = loading_and_settings()

    # 获取 cookies 保存至本地
    time.sleep(20)  # 进行扫码
    dictCookies = browser.get_cookies()  # 获取list的cookies
    jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存

    path = Root + r"\poems_cookies.txt"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(jsonCookies)
    print('cookies保存成功！')


# 8、使用 cookies 登录
def use_cookies():
    browser, wait = loading_and_settings()

    # 获取 cookies 保存至本地
    time.sleep(5)  # 等待加载
    """
    从本地读取cookies并刷新页面,成为已登录状态
    """
    path = Root + r"\poems_cookies.txt"
    with open(path, 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())

    # 往browser里添加cookies
    for cookie in listCookies:
        cookie_dict = {
            'domain': '.gushiwen.cn',
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            "expires": '',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        }
        browser.add_cookie(cookie_dict)
    browser.refresh()  # 刷新网页,cookies才成功

    time.sleep(30)


# 9、基于 selenium 使用 账号密码验证码登录
def log_website():
    try:
        # 第一步：浏览器驱动初始化
        browser, wait = loading_and_settings()

        # 第二步：登录界面截图，裁剪截图，识别验证码
        path = Root + r'\log_screen.png'
        browser.get_screenshot_as_file(path)  # 保存页面截图

        image = cv2.imread(path)  # 裁剪图片，获得验证码部分
        # print(img.shape)
        cropped = image[305:350, 760:855]  # 裁剪坐标为[y0:y1, x0:x1]
        path = Root + r'\log_cut.png'
        cv2.imwrite(path, cropped)

        # 将图片转换成灰度图片测试
        image = Image.open(path)
        image = image.convert('L')
        # image.show()

        # 将图片实现二值化处理
        t = 155
        table = []
        for i in range(256):
            if i < t:
                table.append(0)
            else:
                table.append(1)
        image = image.point(table, '1')

        path = Root + r"\log_Grayscale.png"        # 存储 经灰度和二值化 处理后的图片
        image.save(path)

        image = Image.open(path)  # Image 读取识别
        code_recognition = pytesseract.image_to_string(image, lang='eng')  # 英文识别
        # text = pytesseract.image_to_string(image, lang='chi_sim')

        if 'O' in code_recognition:  # 处理 0 与 O 的问题
            code_recognition = re.sub('O', '0', code_recognition).upper()

        # 输入所识别的文字
        print('本次验证码为：',  code_recognition)
        # 定位验证码的位置
        """
        # By.ID = 'imgCode'
        location = browser.find_element(by=By.ID, value='imgCode').location
        size = browser.find_element(by=By.ID, value='imgCode').size
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
    
        # 裁剪保存
        img = Image.open(path).crop((left, top, right, bottom))
        img.save('E:/Desktop/screen1.png')
    
        driver.quit()"""

        # 第三步：输入账号
        email = browser.find_element(by=By.ID, value='email')
        email.send_keys('1831197494@qq.com')
        # email.send_keys(Keys.ENTER)  # 回车 确定的意思
        time.sleep(10)

        # 第四步：输入密码
        password = browser.find_element(by=By.ID, value='pwd')
        password.send_keys('123qwerty')
        time.sleep(10)

        # 第五步：填入验证码
        code = browser.find_element(by=By.ID, value='code')
        code.send_keys(code_recognition)
        time.sleep(10)

        # 第四步：点击登录
        # time.sleep(5)
        # browser.find_element(by=By.ID, value='denglu').click()

        time.sleep(100)
        browser.close()
        return True

    except Exception as e:
        print("本次失败：", e)
        return False


# 主函数
def main():
    # loading_page()
    # find_element()
    # drag_drop()
    # page_scroll()
    # get_attribute()
    # get_cookies()
    # use_cookies()
    log_website()
    # while True:
    #     flag = log_website()
    #     if flag:
    #         break
    #     else:
    #         continue


if __name__ == '__main__':
    main()
