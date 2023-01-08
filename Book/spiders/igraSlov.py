import datetime
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from Book.items import BookItem




class IgraslovSpider(CrawlSpider):
    name = 'igraSlov'
    allowed_domains = ['igraslov.store']
    #start_urls = ['https://igraslov.store/shop/?products-per-page=all']
    start_urls = ['https://igraslov.store/shop/']


    rules = (
        Rule(LinkExtractor(restrict_xpaths=['//li[@class="title"]/h2/a']),"parse_page"),
    )



    def parse(self, response):
        yield {"page_num":response.url + f"  {datetime.datetime.now()}"}
        
    def parse_page(self,response):

        
        item = BookItem()

        item['Name'] = response.xpath('//h2/text()').get()
        item['Author'] = response.xpath('//tr[contains(@class, "%d0%b0%d0%b2%d1%82%d0%be%d1%80")]/td/p/text()').get()
        item['Desc'] = response.xpath('//div[@class="woocommerce-product-details__short-description"]/p/text()').getall()
        item['Year'] = response.xpath('//tr[contains(@class, "%d0%b3%d0%be%d0%b4-%d0%b8%d0%b7%d0%b4%d0%b0%d0%bd%d0%b8%d1%8f")]/td/p/text()').get()
        item['Img'] = response.xpath('//img[@class="wp-post-image"]/@src').get()
        item['ISBN'] = response.xpath('//tr[contains(@class, "isbnissn")]/td/p/text()').get()
        item['Page'] = response.xpath('//tr[contains(@class, "%d0%ba%d0%be%d0%bb-%d0%b2%d0%be-%d1%81%d1%82%d1%80%d0%b0%d0%bd%d0%b8%d1%86")]/td/p/text()').get()
        item['Genre'] = "black"
        item['Tag'] = response.xpath('//a[@rel="tag"]/text()').get()

        yield item
        
        
