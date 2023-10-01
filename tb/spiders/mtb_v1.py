import json
import logging
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
import scrapy
import os

from selenium import webdriver
from selenium.webdriver.common.by import By



class MtbSpider(scrapy.Spider):
    name = "mtb_v1"
    allowed_domains = ["taobao.com"]
    browser = None

    start_urls = ["https://www.baidu.com/","https://www.taobao.com"]
    # https://s.taobao.com/search?q=内衣&spm=a21bo.jianhua.201867-main.2.5af92a89Cqjr6w
    # start_urls = ["https://s.taobao.com/search?q=内衣&spm=a21bo.jianhua.201867-main.2.5af92a89Cqjr6w"]

    def __init__(self):
        print("初始化参数")
        # options = webdriver.FirefoxOptions()
        # self.browser = webdriver.Firefox(options=options)
        # self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {  get: () => undefined })")

        #
        # options = webdriver.ChromeOptions()
        # #options.add_argument("--headless")
        # options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_experimental_option("useAutomationExtension",False)
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # self.browser = webdriver.Chrome(options=options)
        # self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": """
        #           Object.defineProperty(navigator, 'webdriver', {
        #             get: () => undefined
        #           })
        #         """
        # })
        # self.browser.maximize_window()

    def start_requests(self):
        logging.info("请求开始")
        # cookies = self.selenium_chrome_login()
        # time.sleep(2)
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
            )


    def parse(self, response):
        # response = str(response).split(" ")[1].replace(">", "")
        # bro = self.login(response)  # 传入登陆网址进行模拟登录
        # print(response.text)
        # logging.warn("调试 调试")
        # print("-----------------")
        #b = response.text
        # print(b)
        # print("-----------------")
        # r = response.css("title")
        # print(r)

        pass

    def take_cookie(self):
        cookie_filename = "cookie.json"
        cookies = self.load_json_from_file(cookie_filename);
        if cookies == None :
            cookies = self.ask_for_newcookie()
            self.dump_cookie_to_file(cookie_filename, cookies)
        # logging.debug("cookie值为:%s",cookie_json)
        return cookies;

    def ask_for_newcookie(self):
        logging.info("登陆淘宝首页，获取cookie信息")
        self.browser.get("https://www.taobao.com")
        self.browser.find_element(By.LINK_TEXT,'亲，请登录').click()
        time.sleep(1)
        driver_wait = WebDriverWait(self.browser, 60, 0.5)
        user_name = driver_wait.until(EC.presence_of_element_located((By.ID, 'fm-login-id')))
        user_name.send_keys(self.settings["TAOBAO_USER_NAME"])
        password = driver_wait.until(EC.presence_of_element_located((By.ID, 'fm-login-password')))
        password.send_keys(self.settings["TAOBAO_PASSWORD"])
        # 检查是否出现了滑动验证码

        ##--测试可用
        try:
            slider = self.browser.find_element_by_xpath("//span[contains(@class, 'btn_slide')]")
            if slider.is_displayed():
                logging.info("滑动验证码处理")
                ActionChains(self.browser).click_and_hold(on_element=slider).perform()
                ActionChains(self.browser).move_by_offset(xoffset=258, yoffset=0).perform()
                ActionChains(self.browser).pause(0.5).release().perform()
        except:
            logging.info("没有出现滑动验证码")
            # 点击登录按钮
        button = driver_wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'password-login')))
        button.click()
        # --测试中
        # draggable = self.browser.find_element(By.ID, "nc_1_n1z")
        # logging.info("测试代码")
        # logging.info(draggable.text)
        # ActionChains(driver).click_and_hold(on_element = draggable).perform()
        # ActionChains(driver).move_to_element_with_offset(to_element=draggable,xoffset=8,yoffset=0)
        #
        # start = draggable.location
        # finish = driver.find_element(By.ID, "nc_1_n1z").location
        # ActionChains(driver) \
        #     .drag_and_drop_by_offset(draggable, finish['x'] - start['x'], finish['y'] - start['y']) \
        #     .perform()

        time.sleep(50)
        cookies = self.browser.get_cookies();
        return cookies

    def selenium_chrome_login(self):
        cookies = self.take_cookie()
        for cookie in cookies:
            logging.info("name=%s,value=%s",cookie["name"],cookie["value"])
        return cookies



    # 登录
    def login(self, url):
        bro = webdriver.Chrome()
        bro.maximize_window()
        time.sleep(1)

        bro.get(url)
        time.sleep(1)

        bro.find_element(by=By.ID, value="fm-login-id").click()
        time.sleep(3)

        # bro.find_element_by_name("fm-login-id").send_keys("淘宝账号")
        # time.sleep(1)
        # bro.find_element_by_name("fm-login-password").send_keys("淘宝密码")
        # time.sleep(1)
        #
        # # save_screenshot 就是将当前页面进行截图且保存
        # bro.save_screenshot('taobao.png')
        #
        # code_img_ele = bro.find_element_by_xpath("//*[@id='nc_1__scale_text']/span")
        # location = code_img_ele.location  # 验证码图片左上角的坐标 x,y
        # size = code_img_ele.size  # 验证码的标签对应的长和宽
        # # 左上角和右下角的坐标
        # rangle = (
        #     int(location['x']), int(location['y']), int(location['x'] + size['width']),
        #     int(location['y'] + size['height'])
        # )
        #
        # i = Image.open("./taobao.png")
        # # crop裁剪
        # frame = i.crop(rangle)
        #
        # # 动作链
        # action = ActionChains(bro)
        # # 长按且点击
        # action.click_and_hold(code_img_ele)
        #
        # # move_by_offset(x,y) x水平方向,y竖直方向
        # # perform()让动作链立即执行
        # action.move_by_offset(270, 0).perform()
        # time.sleep(0.5)
        #
        # # 释放动作链
        # action.release()
        # # 登录
        # bro.find_element_by_xpath("//*[@id='login-form']/div[4]/button").click()
        return bro

    def load_json_from_file(self,filename):
        try:
            if os.path.exists(filename):
                with open(filename, "r") as rd:
                    cookie_json = json.load(rd)
                    if len(cookie_json) == 0:
                        logging.warn("文件内容为空")
                        return None
                    return cookie_json
            else:
                logging.warn("文件不存在%s",filename)
                return None

        except Exception as e:
            logging.error("json加载失败(文件%s)",filename)
            logging.error(str(e))

        return None


    def dump_cookie_to_file(self,filename,cookies):
        try:
            with open(filename,"w") as wr:
               json.dumps(cookies,wr)
        except Exception as e:
            logging.error(str(e))