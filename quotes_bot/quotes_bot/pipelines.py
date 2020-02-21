# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class QuotesBotPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("scraped_data.db")
        self.curs = self.conn.cursor()

    def create_table(self):
        self.curs.execute("""DROP TABLE IF EXISTS scraped_tb""")
        self.curs.execute("""CREATE TABLE scraped_tb(
            text text,
            author text,
            tag text)""")

    def process_item(self, item, spider):
        self.store_db(item)
        print( "Pipeline:" + item["text"][0])
        return item

    def store_db(self, item):
        self.curs.execute("""INSERT INTO scraped_tb VALUES (?,?,?)""",(
            item["text"][0],
            item["author"][0],
            item["tag"][0],
        ))
        self.conn.commit()