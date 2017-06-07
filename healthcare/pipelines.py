# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
from mysql.connector import errorcode
from scrapy.exceptions import DropItem
from datetime import date
import logging

class CWMySQLPipeline(object):
    def __init__(self):
        config = {
          'user': 'root',
          'host': 'localhost',
          'database': 'scrapy',
          'raise_on_warnings': True,
        }
        try:
            self.logger = logging.getLogger(__file__)
            self.conn = mysql.connector.connect(**config)
            self.cursor = self.conn.cursor()
            self.current_date = date.today()
            self.add_item = """
            INSERT INTO cw (import_date, sku, name, price, saved, url)
            VALUES (%s, %s, %s, %s, %s, %s)"""
        except mysql.connector.Error as err:
            self.logger.error(err)


    def process_item(self, item, spider):
        item['import_date'] = self.current_date
        if item['price'] and item['price'].startswith('$'):
            item['price'] = float(item['price'][1:].replace(',',''))

        if item['saved'] and item['saved'].startswith('SAVE'):
            item['saved'] = float(item['saved'].split('$')[1].replace(',',''))
        else:
            item['saved'] = 0.0

        # if item['name']:
        #     item['name'] = item['name'].encode('utf-8')
        #
        # if item['url']:
        #     item['url'] = item['url'].encode('utf-8')

        try:
            self.cursor.execute(self.add_item, (self.current_date,
                                                item['sku'],
                                                item['name'].encode('utf-8'),
                                                item['price'],
                                                item['saved'],
                                                item['url'].encode('utf-8')
                                                ))
            self.conn.commit()
        except mysql.connector.Error as err:
            self.logger.error(err)

        return item
