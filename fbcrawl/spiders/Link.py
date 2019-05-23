import scrapy
import logging
import time


from scrapy.loader import ItemLoader
from scrapy.http import FormRequest
from fbcrawl.items import LinkItem
from fbcrawl.spiders.fbcrawl import FacebookSpider


class LinkSpider(FacebookSpider):
    """
    Parse FB comments, given a post (needs credentials)
    """    
    name = "link"
    custom_settings = {
        'FEED_EXPORT_FIELDS': ['profile','post_url','action','url','date'],
        'DUPEFILTER_CLASS' : 'scrapy.dupefilters.BaseDupeFilter',
        'CONCURRENT_REQUESTS':1, 
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

    def parse_page(self, response):
        '''
        Parse the given page selecting the posts.
        Then ask recursively for another page.
        '''

        #select all posts
        for post in response.xpath("//div[contains(@data-ft,'top_level_post_id')]"):
            self.logger.info('Parsing post n = {}'.format(abs(self.count)+1))
            #returns full post-link in a list
            post = post.xpath(".//a[contains(@href,'footer')]/@href").extract()
            temp_post = response.urljoin(post[0])
            self.count -= 1
            link_url = post[0].split("&refid")[0]
            yield scrapy.Request(temp_post,
                                 callback=self.parse_post,
                                 priority = self.count,
                                 meta={'index':1,
                                       'link_url':link_url})
    
            #load following page, try to click on "more"
            #after few pages have been scraped, the "more" link might disappears 
            #if not present look for the highest year not parsed yet
            #click once on the year and go back to clicking "more"
            new_page = response.xpath("//div[2]/a[contains(@href,'timestart=') and not(contains(text(),'ent')) and not(contains(text(),number()))]/@href").extract()      
            if not new_page: 
                self.logger.info('[!] "more" link not found, will look for a "year" link')
                #self.k is the year link that we look for 
                if response.meta['flag'] == self.k and self.k >= self.year:                
                    xpath = "//div/a[contains(@href,'time') and contains(text(),'" + str(self.k) + "')]/@href"
                    new_page = response.xpath(xpath).extract()
                    if new_page:
                        new_page = response.urljoin(new_page[0])
                        self.k -= 1
                        self.logger.info('Found a link for year "{}", new_page = {}'.format(self.k,new_page))
                        yield scrapy.Request(new_page, 
                                             callback=self.parse_page, 
                                             priority = -10000, 
                                             meta={'flag':self.k})
                    else:
                        while not new_page: #sometimes the years are skipped this handles small year gaps
                            self.logger.info('Link not found for year {}, trying with previous year {}'.format(self.k,self.k-1))
                            self.k -= 1
                            if self.k < self.year:
                                raise CloseSpider(' Crawling finished')
                            xpath = "//div/a[contains(@href,'time') and contains(text(),'" + str(self.k) + "')]/@href"
                            new_page = response.xpath(xpath).extract()
                        self.logger.info('Found a link for year "{}", new_page = {}'.format(self.k,new_page))
                        new_page = response.urljoin(new_page[0])
                        self.k -= 1
                        yield scrapy.Request(new_page, 
                                             callback=self.parse_page,
                                             priority = -10000,
                                             meta={'flag':self.k}) 
                else:
                    self.logger.info('Crawling has finished with no errors!')
            else:
                new_page = response.urljoin(new_page[0])
                if 'flag' in response.meta:
                    self.logger.info('Page scraped, clicking on "more"! new_page ')
                    yield scrapy.Request(new_page, 
                                         callback=self.parse_page, 
                                         priority = -10000, 
                                         meta={'flag':response.meta['flag']})
                else:
                    self.logger.info('First page scraped, clicking on "more"! new_page = {}'.format(new_page))
                    yield scrapy.Request(new_page, 
                                         callback=self.parse_page, 
                                         priority = -10000, 
                                         meta={'flag':self.k})
    def parse_post(self,response):
        #selects all the reactions of the post of the previous spider
        reactions = response.xpath("//div[contains(@id,'sentence')]/a[contains(@href,'reaction/profile')]/@href")
        reactions = response.urljoin(reactions[0].extract())
        yield scrapy.Request(reactions, callback=self.parse_reactions, priority = 10000,
                             meta={'link_url':response.meta['link_url']})
        self.logger.info('reaction parsing done moving on to comment parsing')
        path = './/div[string-length(@class) = 2 and count(@id)=1 and contains("0123456789", substring(@id,1,1)) and .//div[contains(@id,"comment_replies")]]'  + '['+ str(response.meta['index']) + ']'
        for reply in response.xpath(path):
            source = reply.xpath("substring-before(.//h3/a/@href, concat(substring('&', 1 div contains(.//h3/a/@href, 'profile.php')), substring('?', 1 div not(contains(.//h3/a/@href, 'profile.php')))))").extract()
            answer = reply.xpath('.//a[contains(@href,"repl")]/@href').extract()
            ans = response.urljoin(answer[::-1][0])
            self.logger.info('{} nested comment @ page {}'.format(str(response.meta['index']),ans))
            yield scrapy.Request(ans,
                                 callback=self.parse_reply,
                                 meta={'url':response.url,
                                       'index':response.meta['index'],
                                       'link_url':response.meta['link_url'],
                                       'flag':'init'})
        #loads regular comments     
        if not response.xpath(path):
            path2 = './/div[string-length(@class) = 2 and count(@id)=1 and contains("0123456789", substring(@id,1,1)) and not(.//div[contains(@id,"comment_replies")])]'
            for i,reply in enumerate(response.xpath(path2)):
                self.logger.info('{} regular comment @ post {}'.format(i,response.meta['link_url']))
                new = ItemLoader(item=LinkItem(),selector=reply)
                new.context['lang'] = self.lang
                new.add_xpath('profile',"substring-before(.//h3/a/@href, concat(substring('&', 1 div contains(.//h3/a/@href, 'profile.php')), substring('?', 1 div not(contains(.//h3/a/@href, 'profile.php')))))")  
                new.add_xpath('action','.//div[h3]/div[1]//text()')
                new.add_xpath('date','.//abbr/text()')
                new.add_value('post_url',response.meta['link_url'])
                new.add_value('url',response.url)
                yield new.load_item()
            
        #previous comments
        if not response.xpath(path):
            for next_page in response.xpath('.//div[contains(@id,"see_next")]'):
                new_page = next_page.xpath('.//@href').extract()
                new_page = response.urljoin(new_page[0])
                self.logger.info('New page to be crawled {}'.format(new_page))
                yield scrapy.Request(new_page,
                                     callback=self.parse_page,
                                     meta={'index':1,
                                           'link_url':response.meta['link_url']})        
        
    def parse_reply(self,response):
        '''
        parse reply to comments, root comment is added if flag
        '''
        if response.meta['flag'] == 'init':
            #parse root comment
            for root in response.xpath('//div[contains(@id,"root")]/div/div/div[count(@id)!=1 and contains("0123456789", substring(@id,1,1))]'): 
                new = ItemLoader(item=LinkItem(),selector=root)
                new.context['lang'] = self.lang
                new.add_xpath('profile', "substring-before(.//h3/a/@href, concat(substring('&', 1 div contains(.//h3/a/@href, 'profile.php')), substring('?', 1 div not(contains(.//h3/a/@href, 'profile.php')))))")
                new.add_xpath('action','.//div[1]//text()')
                new.add_xpath('date','.//abbr/text()')
                new.add_value('post_url',response.meta['link_url'])
                new.add_value('url',response.url)
                yield new.load_item()
            #parse all replies in the page
            for reply in response.xpath('//div[contains(@id,"root")]/div/div/div[count(@id)=1 and contains("0123456789", substring(@id,1,1))]'): 
                new = ItemLoader(item=LinkItem(),selector=reply)
                new.context['lang'] = self.lang
                new.add_xpath('profile', "substring-before(.//h3/a/@href, concat(substring('&', 1 div contains(.//h3/a/@href, 'profile.php')), substring('?', 1 div not(contains(.//h3/a/@href, 'profile.php')))))")
                new.add_xpath('action','.//div[h3]/div[1]//text()')
                new.add_xpath('date','.//abbr/text()')
                new.add_value('post_url',response.meta['link_url'])
                new.add_value('url',response.url)   
                yield new.load_item()
                
            back = response.xpath('//div[contains(@id,"comment_replies_more_1")]/a/@href').extract()
            if back:
                self.logger.info('Back found, more nested comments')
                back_page = response.urljoin(back[0])
                yield scrapy.Request(back_page, 
                                     callback=self.parse_reply,
                                     priority=1000,
                                     meta={'link_url':response.meta['link_url'],
                                           'flag':'back',
                                           'url':response.meta['url'],
                                           'index':response.meta['index']})
            else:
                next_reply = response.meta['url']
                self.logger.info('Nested comments crawl finished, heading to proper page: {}'.format(response.meta['url']))
                yield scrapy.Request(next_reply,
                                     callback=self.parse_page,
                                     meta={'index':response.meta['index']+1,
                                           'link_url':response.meta['link_url']})
                
        elif response.meta['flag'] == 'back':
            #parse all comments
            for reply in response.xpath('//div[contains(@id,"root")]/div/div/div[count(@id)=1 and contains("0123456789", substring(@id,1,1))]'): 
                new = ItemLoader(item=LinkItem(),selector=reply)
                new.context['lang'] = self.lang            
                new.add_xpath('profile', "substring-before(.//h3/a/@href, concat(substring('&', 1 div contains(.//h3/a/@href, 'profile.php')), substring('?', 1 div not(contains(.//h3/a/@href, 'profile.php')))))")
                new.add_value('post_url',response.meta['link_url'])
                new.add_xpath('action','.//div[h3]/div[1]//text()')
                new.add_xpath('date','.//abbr/text()')
                new.add_value('url',response.url)   
                yield new.load_item()
            #keep going backwards
            back = response.xpath('//div[contains(@id,"comment_replies_more_1")]/a/@href').extract()
            self.logger.info('Back found, more nested comments')
            if back:
                back_page = response.urljoin(back[0])
                yield scrapy.Request(back_page, 
                                     callback=self.parse_reply,
                                     priority=1000,
                                     meta={'link_url':response.meta['link_url'],
                                           'flag':'back',
                                           'url':response.meta['url'],
                                           'index':response.meta['index']})
            else:
                next_reply = response.meta['url']
                self.logger.info('Nested comments crawl finished, heading to home page: {}'.format(response.meta['url']))
                yield scrapy.Request(next_reply,
                                     callback=self.parse_page,
                                     meta={'index':response.meta['index']+1})        
        
   
    def parse_reactions(self,response):
        #selects all reactions of a given post
        self.logger.info('parsing reactions of post : {}'.format(response.meta['link_url']))
        for i,reply in enumerate(response.xpath(".//li/table/tbody/tr/td/table")):
            new = ItemLoader(item=LinkItem(),selector=reply)
            new.context['lang'] = self.lang
            new.add_xpath('profile',".//div/h3/a/@href")
            new.add_xpath('action',".//td[2]/img/@alt")
            new.add_value('url',response.url)
            new.add_value('post_url',response.meta['link_url'])
            yield new.load_item()
        #finds new reactions to crawl
        new_page = response.xpath("//li/table/tbody/tr/td/div/a/@href").extract()
        time.sleep(1)
        self.logger.info('finding more reactions')
        if not new_page :
            self.logger.info('no more reactions to fetch')
        else :
            self.logger.info('more reactions found')
            new_page = response.urljoin(new_page[0])
            yield scrapy.Request(new_page, callback=self.parse_reactions, priority = 10000, meta={'link_url':response.meta['link_url']})

