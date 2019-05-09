import scrapy
import logging
import time


from scrapy.loader import ItemLoader
from fbcrawl.spiders.fbcrawl import FacebookSpider
from fbcrawl.items import ReactionsItem

class ReactionsSpider(FacebookSpider):
    """
    parse post reactions, given a post(needs credentials)
    """
    name = "reactions"
    custom_settings = {
        'FEED_EXPORT_FIELDS': ['profile','type'],
        'DUPEFILTER_CLASS' : 'scrapy.dupefilters.BaseDupeFilter',
        'CONCURRENT_REQUESTS':1,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

    def parse_page(self, response):
        reactions = response.xpath("//div[contains(@id,'sentence')]/a[contains(@href,'reaction/profile')]/@href")
        reactions = response.urljoin(reactions[0].extract())
        yield scrapy.Request(reactions, callback=self.parse_reactions)
        
    def parse_reactions(self,response):
        self.logger.info('crawling data')
        for i,reply in enumerate(response.xpath(".//li/table/tbody/tr/td/table")):
            self.logger.info('{} regular reaction @ page '.format(i+1))
            new = ItemLoader(item=ReactionsItem(),selector=reply)
            new.context['lang'] = self.lang
            new.add_xpath('profile',".//div/h3/a/@href")
            new.add_xpath('type',".//td[2]/img/@alt")        
            yield new.load_item()
            self.logger.info('item created ')
        new_page = response.xpath("//li/table/tbody/tr/td/div/a/@href").extract()
        time.sleep(1)
        self.logger.info('finding new page ')
        if not new_page :
            self.logger.info('no more reactions to fetch')
        else :
            self.logger.info('new page found')
            new_page = response.urljoin(new_page[0])
            yield scrapy.Request(new_page, callback=self.parse_reactions)



