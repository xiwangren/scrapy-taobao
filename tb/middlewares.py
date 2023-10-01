# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import time
import os
import json

from scrapy import signals
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class TbSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class CustDownloaderMiddleware:
    browser = None

    def __init__(self):
        print("初始化 .... 浏览器! 加载....cookie!")
        logging.getLogger('selenium').setLevel('ERROR')
        logging.getLogger('urllib3').setLevel('ERROR')
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--disable-gpu')  # 上面代码就是为了将Chrome不弹出界面
        options.add_argument('--start-maximized')  # 最大化
        options.add_argument('--incognito')  # 无痕隐身模式
        options.add_argument("disable-cache")  # 禁用缓存
        options.add_argument('disable-infobars')
        options.add_argument("--log-level=3")
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        self.browser = webdriver.Chrome(options=options)
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                  Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                  })
                """
        })
        self.browser.maximize_window()
        self.browser.get("https://www.taobao.com")
        cookies = self.take_cookie()
        for cookie in cookies:
            self.browser.add_cookie(cookie)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        self.browser.get(request.url)
        return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8')

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass
    def spider_closed(self,spider):
        print("关闭 关闭 关闭 关闭 关闭 关闭 关闭 关闭 关闭 关闭 关闭 ")
    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

    def take_cookie(self):
        cookie_filename = "/Volumes/bluepay/python/crapy-case/tb/cookie.json"
        cookies = self.load_cookies_from_file(cookie_filename);
        if cookies == None:
            cookies = self.ask_for_newcookie()
            self.dump_cookie_to_file(cookie_filename, cookies)
            cookies = self.load_cookies_from_file(cookie_filename)
        # logging.debug("cookie值为:%s", json.dumps(cookies))
        return cookies;

    def ask_for_newcookie(self):
        logging.info("登陆淘宝首页，重新获取cookie信息")
        self.browser.get("https://www.taobao.com")
        self.browser.find_element(By.LINK_TEXT, '亲，请登录').click()
        time.sleep(1)
        driver_wait = WebDriverWait(self.browser, 60, 0.5)
        user_name = driver_wait.until(EC.presence_of_element_located((By.ID, 'fm-login-id')))
        user_name.send_keys("tb384465205666")
        password = driver_wait.until(EC.presence_of_element_located((By.ID, 'fm-login-password')))
        password.send_keys("ningbo12#")
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

        time.sleep(1)
        cookies = self.browser.get_cookies()
        return cookies;

    def load_cookies_from_file(self, filename):
        try:
            if os.path.exists(filename):
                with open(filename, "r") as rd:
                    cookie = json.load(rd)
                    if not cookie or len(cookie) == 0:
                        logging.warn("文件内容为空")
                        return None
                    return cookie
            else:
                logging.warn("文件不存在%s", filename)
                return None

        except Exception as e:
            logging.error("json加载失败(文件%s)", filename)
            logging.error(str(e))

        return None

    def dump_cookie_to_file(self, filename, cookies):
        try:
            # new_dict = {}
            # for cookie in cookies:
            #     new_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            with open(filename, "w") as wr:
                # print("要写入的cookie：%s",json.dumps(new_dict))
                # wr.write(json.dumps(new_dict))
                json.dump(cookies,wr)

        except Exception as e:
            logging.error(str(e))


class TbDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        print("*********默认 TbDownloaderMiddleware*********")
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
