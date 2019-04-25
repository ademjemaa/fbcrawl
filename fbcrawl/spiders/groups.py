import scrapy
import logging

from scrapy.loader import ItemLoader
from fbcrawl.spiders.fbcrawl import FacebookSpider
from fbcrawl.items import FbcrawlItem

class GroupPosts(FacebookSpider):

    name = "group"
    custom_settings = {
        'FEED_EXPORT_FIELDS': ['source','shared_from','date','text', \
                               'reactions','likes','ahah','love','wow', \
                               'sigh','grrr','comments','url'],
        'CONCURRENT_REQUESTS':1,
        'DUPEFILTER_CLASS' : 'scrapy.dupefilters.BaseDupeFilter',

    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

    def parse_page(self, response):
        '''
        Parse the given page selecting the posts.
        Then ask recursively for another page.
        '''
        #select all posts
        for post in response.xpath("//div[contains(@id,'m_group_stories')]//div[contains(@data-ft,'top_level_post_id')]"):            
            new = ItemLoader(item=FbcrawlItem(),selector=post)
            self.logger.info('Parsing post n = {}'.format(abs(self.count)))
            new.add_xpath('comments', "./div[2]/div[2]/a[1]/text()")        
            new.add_xpath('url', ".//a[contains(@href,'footer')]/@href")

            #returns full post-link in a list
            post = post.xpath(".//a[contains(@href,'footer')]/@href").extract() 
            temp_post = response.urljoin(post[0])
            self.count -= 1
            yield scrapy.Request(temp_post, self.parse_post, priority = self.count, meta={'item':new})       

        #load following page
        #tries to click on "more"
        new_page = response.xpath("//div[contains(@id,'m_group_stories')]/div[2]/a/@href").extract()      
        if not new_page: 
            self.logger.info('Crawling has finished with no errors!')
        else:
            self.logger.info('new page')
            self.k -= 1
            new_page = response.urljoin(new_page[0])
            yield scrapy.Request(new_page, callback=self.parse_page)
                
    def parse_post(self,response):
        new = ItemLoader(item=FbcrawlItem(),response=response,parent=response.meta['item'])
        new.add_xpath('source', "substring-before(.//div[1]/div/div/div/table//strong[1]/a[1]/@href,'?')")
        new.add_xpath('shared_from','//div[contains(@data-ft,"top_level_post_id") and contains(@data-ft,\'"isShare":1\')]/div/div[3]//strong/a/text()')
        new.add_xpath('date','//div/div/abbr/text()')
        new.add_xpath('text','//div[@data-ft]//p//text() | //div[@data-ft]/div[@class]/div[@class]/text()')
        new.add_xpath('reactions',"//a[contains(@href,'reaction/profile')]/div/div/text()")  
        
        reactions = response.xpath("//div[contains(@id,'sentence')]/a[contains(@href,'reaction/profile')]/@href")
        reactions = response.urljoin(reactions[0].extract())
        yield scrapy.Request(reactions, callback=self.parse_reactions, meta={'item':new})
        
    def parse_reactions(self,response):
        new = ItemLoader(item=FbcrawlItem(),response=response, parent=response.meta['item'])
        new.context['lang'] = self.lang           
        new.add_xpath('likes',"//a[contains(@href,'reaction_type=1')]/span/text()")
        new.add_xpath('ahah',"//a[contains(@href,'reaction_type=4')]/span/text()")
        new.add_xpath('love',"//a[contains(@href,'reaction_type=2')]/span/text()")
        new.add_xpath('wow',"//a[contains(@href,'reaction_type=3')]/span/text()")
        new.add_xpath('sigh',"//a[contains(@href,'reaction_type=7')]/span/text()")
        new.add_xpath('grrr',"//a[contains(@href,'reaction_type=8')]/span/text()")        
        yield new.load_item()    


        
