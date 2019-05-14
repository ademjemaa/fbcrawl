# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Join, MapCompose
from datetime import datetime, timedelta

    
def comments_strip(string,loader_context):
    lang = loader_context['lang']    
    if lang == 'en':
        new_string = string[0].rstrip(' Comments')
        while new_string.rfind(',') != -1:
            new_string = new_string[0:new_string.rfind(',')] + new_string[new_string.rfind(',')+1:]
        return new_string
    else:
        return string

def reactions_strip(string,loader_context):
    lang = loader_context['lang']
    if lang == 'en':
        newstring = string[0]
        #19,298,873 instead of "User1, User2 and 4k others"  
        if len(newstring.split()) == 1:
            while newstring.rfind(',') != -1:
                newstring = newstring[0:newstring.rfind(',')] + newstring[newstring.rfind(',')+1:]
            return newstring
        else:
            return newstring
    else:
        return string

def url_strip(url):
    fullurl = url[0]
    #catchin '&id=' is enough to identify the post
    i = fullurl.find('&id=')
    if i != -1:
        return fullurl[:i+4] + fullurl[i+4:].split('&')[0]
    else:  #catch photos   
        i = fullurl.find('/photos/')
        if i != -1:
            return fullurl[:i+8] + fullurl[i+8:].split('/?')[0]
        else: #catch albums
            i = fullurl.find('/albums/')
            if i != -1:
                return fullurl[:i+8] + fullurl[i+8:].split('/?')[0]
            else:
                return fullurl
    

class FbcrawlItem(scrapy.Item):
    source = scrapy.Field()   
    date = scrapy.Field(      # when was the post published
        input_processor=TakeFirst()
    )       
    text = scrapy.Field(
        output_processor=Join(separator=u'')
    )                       # full text of the post as sometimes text not all in the same <>
    comments = scrapy.Field(
        output_processor=comments_strip
    )                                       
    reactions = scrapy.Field(
        output_processor=reactions_strip
    )                  # num of reactions
    likes = scrapy.Field(
        output_processor=reactions_strip
    )                      
    ahah = scrapy.Field()                      
    love = scrapy.Field()                      
    wow = scrapy.Field()                      
    sigh = scrapy.Field()                      
    grrr = scrapy.Field()                      
    share = scrapy.Field()                      # num of shares
    url = scrapy.Field(
        output_processor=url_strip
    )
    shared_from = scrapy.Field()

class CommentsItem(scrapy.Item):
    source = scrapy.Field()   
    reply_to=scrapy.Field()
    date = scrapy.Field()      # when was the post published
           
    text = scrapy.Field(
        output_processor=Join(separator=u'')
    )                       # full text of the post as comments are sometimes not all in the same <>
    reactions = scrapy.Field(
        output_processor=reactions_strip
    )                  # num of reactions
    likes = scrapy.Field(
        output_processor=reactions_strip
    )                      
    ahah = scrapy.Field()                      
    love = scrapy.Field()                      
    wow = scrapy.Field()                      
    sigh = scrapy.Field()                      
    grrr = scrapy.Field()                      
    share = scrapy.Field()                      # num of shares
    url = scrapy.Field()
    shared_from = scrapy.Field()
    
class ReactionsItem(scrapy.Item):
    type = scrapy.Field()
    profile = scrapy.Field()

class ProfileItem(scrapy.Item):
    name = scrapy.Field()
    birth = scrapy.Field()
    url = scrapy.Field()
    location = scrapy.Field()
    friends = scrapy.Field()

class MembersItem(scrapy.Item):
    profile = scrapy.Field()

class LinkItem(scrapy.Item):
    profile = scrapy.Field()
    post_url = scrapy.Field()
    action = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    
    
    
