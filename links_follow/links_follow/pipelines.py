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
            link text,
            link_type text,
            current_page text,
            page_title text)""")

    def process_item(self, item, spider):
        self.store_db(item)
        print( "Pipeline: Text: " + item["link_text"] + "    Link: " + item["link_href"])
        return item

    def store_db(self, item):
        self.curs.execute("""INSERT INTO links_tb VALUES (?,?,?,?,?)""",(
            item["link_text"],
            item["link_href"],
            item["link_type"],
            item["current_page"],
            item["page_title"]
        ))
        self.conn.commit()
