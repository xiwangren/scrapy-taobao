# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import openpyxl as openpyxl
from itemadapter import ItemAdapter
from .my_pysql import PyMySql


class TbPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = '淘宝评论'
        self.ws.append(('店铺','产品链接','店铺链接'))
    def process_item(self, item, spider):
        self.ws.append((item['shop_name'],item['product_url'],item['shop_url']))
        return item
    def close_spider(self,spider):
        self.wb.save("淘宝评论.xlsx")


class MysqlPipeline:
    db = PyMySql()
    def __init__(self):
        print("Mysql init ........")
        self._data = []

    def process_item(self,item,spider):
        self._data.append((item['product_url'],item['shop_name'],item['shop_url']))
        #self.db.insert("INSERT into cpy_products(product_url,shop_name,shop_url) values(%s,%s,%s)", (item['product_url'],item['shop_name'],item['shop_url']))
        if(len(self._data) > 20):
            self.db.insert_batch("INSERT into cpy_products(product_url,shop_name,shop_url) values(%s,%s,%s)", self._data)
            self._data.clear();


    def close_spider(self,spider):
        print("Mysql close_spider ........")
        if(len(self._data)>0):
            self.db.insert_batch("INSERT into cpy_products(product_url,shop_name,shop_url) values(%s,%s,%s)", self._data)
        self.db.close()