# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql




class LinkPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = pymysql.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'facebook123',
            database = 'link'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS link_tb""")
        self.curr.execute("""create table link_tb(
                        profile text,
                        post_url text,
                        action text,
                        url text,
                        date text
                        )""")
    def process_item(self,item, spider):
        self.store_db(item)
        return(item)

    def store_db(self, item):
        self.curr.execute("""insert into link_tb values (%s, %s, %s, %s, %s)""", (
            item['profile'][0],
            item['post_url'][0],
            item['action'][0],
            item['url'][0],
            item['date'][0]
            
        ))
        self.conn.commit()

class FbcrawlPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = pymysql.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'facebook123',
            database = 'link'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS posts_tb""")
        self.curr.execute("""create table posts_tb(
                        source text,
                        date text,
                        text text,
                        reactions text,
                        likes text,
                        ahah text,
                        love text,
                        wow text,
                        sigh text,
                        grrr text,
                        comments text,
                        url text
                        )""")
    def process_item(self,item, spider):
        self.store_db(item)
        return(item)

    def store_db(self, item):
        self.curr.execute("""insert into posts_tb values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
            item['source'][0],
            item['date'][0],
            item['text'][0],
            item['reactions'][0],
            item['likes'][0],
            item['ahah'][0],
            item['love'][0],
            item['wow'][0],
            item['sigh'][0],
            item['grrr'][0],
            item['comments'][0],
            item['url'][0]
            
        ))
        self.conn.commit()

class CommentsPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = pymysql.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'facebook123',
            database = 'link'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS comments_tb""")
        self.curr.execute("""create table comments_tb(
                        source text,
                        reply_to text,
                        date text,
                        reactions text,
                        text text,
                        url text
                        )""")
    def process_item(self,item, spider):
        self.store_db(item)
        return(item)

    def store_db(self, item):
        self.curr.execute("""insert into comments_tb values (%s, %s, %s, %s, %s, %s)""", (
            item['source'][0],
            item['reply_to'][0],
            item['date'][0],
            item['reactions'][0],
            item['text'][0],
            item['url'][0]
            
        ))
        self.conn.commit()

class GroupPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = pymysql.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'facebook123',
            database = 'link'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS group_tb""")
        self.curr.execute("""create table group_tb(
                        source text,
                        date text,
                        text text,
                        reactions text,
                        likes text,
                        ahah text,
                        love text,
                        wow text,
                        sigh text,
                        grrr text,
                        comments text,
                        url text
                        )""")
    def process_item(self,item, spider):
        self.store_db(item)
        return(item)

    def store_db(self, item):
        self.curr.execute("""insert into group_tb values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
            item['source'][0],
            item['date'][0],
            item['text'][0],
            item['reactions'][0],
            item['likes'][0],
            item['ahah'][0],
            item['love'][0],
            item['wow'][0],
            item['sigh'][0],
            item['grrr'][0],
            item['comments'][0],
            item['url'][0]
            
        ))
        self.conn.commit()
        
class MembersPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = pymysql.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'facebook123',
            database = 'link'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS members_tb""")
        self.curr.execute("""create table members_tb(
                        profile text
                        )""")
    def process_item(self,item, spider):
        self.store_db(item)
        return(item)

    def store_db(self, item):
        self.curr.execute("""insert into members_tb values (%s)""", (
            item['profile'][0]

            
        ))
        self.conn.commit()
        
class ProfilePipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = pymysql.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'facebook123',
            database = 'link'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS profile_tb""")
        self.curr.execute("""create table profile_tb(
                        name text,
                        birth text,
                        url text,
                        location text,
                        friends text
                        )""")
    def process_item(self,item, spider):
        self.store_db(item)
        return(item)

    def store_db(self, item):
        self.curr.execute("""insert into profile_tb values (%s, %s, %s, %s, %s)""", (
            item['name'][0],
            item['birth'][0],
            item['url'][0],
            item['location'][0],
            item['friends'][0]

            
        ))
        self.conn.commit()
        
class ReactionsPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = pymysql.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'facebook123',
            database = 'link'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS reactions_tb""")
        self.curr.execute("""create table reactions_tb(
                        profile text,
                        type text
                        )""")
    def process_item(self,item, spider):
        self.store_db(item)
        return(item)

    def store_db(self, item):
        self.curr.execute("""insert into reactions_tb values (%s, %s)""", (
            item['profile'][0],
            item['type'][0]

            
        ))
        self.conn.commit()
        
