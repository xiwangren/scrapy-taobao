from __future__ import absolute_import
import json
import logging
import time
import os

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains

import scrapy
from scrapy.http import HtmlResponse

from selenium import webdriver
from selenium.webdriver.common.by import By

from ..items import ProductItem


class MtbSpider(scrapy.Spider):
    name = "mtb"
    allowed_domains = ["taobao.com"]
    browser = None


    #start_urls = ["https://www.baidu.com/","https://www.taobao.com"]
    # https://s.taobao.com/search?q=内衣&spm=a21bo.jianhua.201867-main.2.5af92a89Cqjr6w
    start_urls = ["https://s.taobao.com/search?q=染发&spm=a21bo.jianhua.201867-main.2.5af92a89Cqjr6w"]
    #start_urls = []
    def __init__(self):
        print("初始化参数")

    def start_requests(self):
        logging.info("请求开始")
        for url in self.start_urls:
            yield scrapy.Request(url,callback=self.parse)


    def parse(self, response: HtmlResponse):
        links = self.ask_for_search_list(response)
        # 测试2
        for link in links:
            proudct_item = ProductItem()
            a = link.xpath('@href')
            # .//开头 相对路径 //开头绝对路径
            b = link.xpath('.//a[contains(@class,"ShopInfo--shopName--")]/@href')
            c = link.xpath('.//a[contains(@class,"ShopInfo--shopName--")]/text()')
            #proudct_item['shop_name'] = c.get()
            #proudct_item['shop_url'] = response.urljoin(b.get())
            #proudct_item['product_url'] = response.urljoin(a.get())
            #yield proudct_item
            print("测试*************",c.get(),"*************测试!")

    def ask_for_product_detail(self,response: HtmlResponse):
        pass
    def ask_for_search_list(self,response):
        # 解析下面html
        # <a class="Card--doubleCardWrapper--L2XFE73" target="_blank"
        # href="https://click.simba.taobao.com/cc_im?p=%C4%DA%D2%C2&amp;s=178615695&amp;k=1017&amp;e=D%2F5Ghk%2F9yBiRqvkvOcnj%2B6me4qwZvjRfIIyYjmI3pxoFsch7vEZW2jq%2F7s0NxG69%2F71MJHsrPiI4gtjJjdIVynhjXWqyDGC2O1VQ2quwATAic5FLNobn8XZfxZlZA6BIqKmkEcQKiMAP5Fmkex3Q6r3y3GiYp22BgR46Nfb48DZJ%2FB6XOhtkWOd0JAJbKN7A1piwNl%2ByK9aNDQvTKVfw6YGDcLZRb4GSVxLNNdnJEo0BQPQ0TT5VQ23c6V5J9naMKfXvfBN3Mg%2F0w3w0qZ24M77YyhnAwK2tuualeAz6RFoKnha2GQ0ILs8wZIIBtH8eUwWTu7k7cswoMIDEtYPCe57BSLtK5JYT7rI6aRKX%2Fqe377aJn1TwlOT1Aos7QxCLMKOzdMpx2yX%2Fmc17HrcbucG18H2YutjLqA8GGuCV1ntuimCmCkfi%2F1SOGl7fYxtb%2BHbj6e8szazyq14TJIsMuuEyChN7%2BAy9hn01Y7VmahiGp%2FdtSl7OA9tRkP2LtbAwZh9WidZRv%2F2Vv5fypEFNPbNG8o8eEKndTLpFpTXzbz4QKocKFVh9PzzyxqKSkfp0BbdcEHseY8Sqb0b610DkCRl1YFAXILq5K4Uog8qbvB8oc2rvutbbO8muBEcie4XV34yS%2FEkjCgdTZMx%2F9acjzgh6OEfslh1XP73dfXcqyzvrueoYAU7GrdSPMpWs1WMDPUS8aLJVbiKz9u0DDjrntWlNMhcuY%2BAEPN6fg4v3JqPSXRuThK4TCvqCsMDCdz3dUk%2BIhrgaqYSEld73CwX6BAQitEsWgFJTz4520ln7lQ3EFEptt0UkKUjtivvScYzrWM5EBK%2FYcvP3sBQOemxEq0cw0jOiBG7VA9D%2F2y0LfGgfLp%2FdWeYcht6GO5If29LsEtUImjqeoYdJ%2Bo9HtaQRrsgHW%2BA9r710amXgITXutdfo5nuQmOlNTQD2NkyLCkM2e6TSTRfTbTOXjN5OwdX0kbIjufUaQDjfDldRi4Nn7Ia9BRVrBnb7dw%3D%3D">
        # <div class="Card--doubleCard--wznk5U4">
        # </div>
        # </a>
        # Card--doubleCardWrapper and ( href包括'detail.tmall.com'  or href包括'taobao.com')
        links = response.xpath(
            '//a[contains(@class,"Card--doubleCardWrapper") and (contains(@href,"detail.tmall.com") or contains(@href,"taobao.com"))]')
        # '//a[contains(@class,"Card--doubleCardWrapper") and (contains(@href,"detail.tmall.com") or contains(@href,"taobao.com"))]/@href')

        print("*******下一页*******")
        next = response.xpath("//div[@class='next-pagination-pages']/button[2]/span[@class='next-btn-helper']")
        print(next)
        return links


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