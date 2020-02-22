# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class LinksFollowPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("links_scraped.db")
        self.curs = self.conn.cursor()

    def create_table(self):
        self.curs.execute("""DROP TABLE IF EXISTS links_tb""")
        self.curs.execute("""CREATE TABLE links_tb(
            text text,
            link text)""")

    def process_item(self, item, spider):
        self.store_db(item)
        print( "Pipeline: Text: " + item["link_text"][0] + "    Link: " + item["link_href"][0])
        return item

    def store_db(self, item):
        self.curs.execute("""INSERT INTO links_tb VALUES (?,?)""",(
            item["link_text"][0],
            item["link_href"][0]
        ))
        self.conn.commit()
