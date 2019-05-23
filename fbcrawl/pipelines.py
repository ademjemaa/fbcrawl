# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

"""
import mysql.connector
from mysql.connector import errorcode



class LinkPipeline(object):

    def _init_(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'facebook123',
            database = 'link'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""#DROP TABLE IF EXISTS link_tb""")
        #self.curr.execute("""create table link_tb(
                        """profile text,
                        post_url text,
                        action text,
                        url text,
                        date text
                        )""")
    """
    def process_item(self,item, spider):
        self.store_db(item)
        return(item)

    def store_db(self, item):
        self.curr.execute("""#insert into link_tb values (%s,%s,%s,%s,%s)""", (
            """item['profile'][0],
            item['post_url'][0],
            item['action'][0],
            item['url'][0],
            item['date'][0]
        ))
        self.conn.commit()
