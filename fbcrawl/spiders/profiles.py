import scrapy
import time

from scrapy.loader import ItemLoader
from fbcrawl.spiders.fbcrawl import FacebookSpider
from fbcrawl.items import ProfileItem


class ProfileSpider(FacebookSpider):
    """
    parse FB profile, give a profile url
    """
    name = "profile"
    custom_settings = {
        'FEED_EXPORT_FIELDS' : ['name','birth','url','location','friends'],
        'DUPEFILTER_CLASS' : 'scrapy.dupefilters.BaseDupeFilter',
        'CONCURRENT_REQUESTS':1,
        'ITEM_PIPELINES':{
            'fbcrawl.pipelines.ProfilePipeline':300
            }

    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        

    def parse_page(self, response):
        """
        selects everything it needs from a profile
        provide profile url to parse
        """
        new = ItemLoader(item=ProfileItem(), response=response)
        new.context['lang'] = self.lang
        new.add_xpath('name',".//strong[contains(@class,'cd')]/text()")
        new.add_xpath('birth',".//div[contains(@id,'basic-info')]//div[contains(@title,'Birthday')]//td[2]//div/text()")
        new.add_xpath('url',".//div[contains(@title,'Facebook')]//td[2]/div/text()")
        new.add_xpath('location',".//div[contains(@title,'Current City')]//td[2]//a/text()")
        #item['friends'] = []
        friends = response.xpath("//div/div[2]/div/div/a[contains(@href,'friends')]/@href").extract()
        friends_list = response.urljoin(friends[0])
        #checks if friends are available to collect
        yield scrapy.Request(friends_list, self.parse_friends, meta={'item':new})

    def parse_friends(self, response):
        self.logger.info('collecting friends')
        new = ItemLoader(item=ProfileItem(),response=response,parent=response.meta['item'])
        #loads all the friends into the item field friends
        new.add_xpath('friends',".//td[contains(@style,'vertical-align')]/a/@href")
        new_page = response.xpath("//div[contains(@id,'m_more')]/a/@href").extract()
        if not new_page:
            self.logger.info('no additional friends')
            yield new.load_item()
        else :
            self.logger.info('more friends to load')
            time.sleep(1)
            new_list = response.urljoin(new_page[0])
            yield scrapy.Request(new_list, self.parse_friends, meta={'item':new})
        






