import scrapy
from Book.items import BookItem

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['www.labirint.ru']
    start_urls = ['https://www.labirint.ru/books/']

    urlPattern = "https://www.labirint.ru/books/"


    def parse(self, response):

        q = response.xpath('//div[@data-title="Все в жанре «Книги»"]')

        for book in q.xpath('div[@class ="genres-carousel__item"]'):
            yield scrapy.Request(f"{self.urlPattern}{book.xpath('div/@data-product-id').get()}",self.parse_page)
            

        next = response.xpath('//div[@class="pagination-next"]/a/@href').get()
        if next:
            yield scrapy.Request(self.urlPattern + next,self.parse)
                    

    def parse_page(self,response):
        
        item = BookItem()
        
        item['Name'] = response.xpath('//h1/text()').get()
        item['Author'] = response.xpath('//div[@class="authors"]/a/text()').get()
        item['Desc'] = "".join(response.xpath('//div[@id="product-about"]/p/text()').getall())
        item['Year'] = response.xpath('//div[@class="publisher"]/text()').getall()[-1]
        item['Img'] = response.xpath('//div[@id="product-image"]/img/@src').get()
        item['ISBN'] = response.xpath('//div[@class="isbn"]/text()').get().split(': ')[-1]

        #Есть не всегда
        page = response.xpath('//div[@class="pages2"]/text()').get()
        if page:
            item['Page'] = page.split(" ")[1]
        genre = response.xpath('//div[@class="genre"]/a/text()').get()
        if genre:
            item['Genre'] = genre
        
        tags = response.xpath('//div[@id="thermometer-books"]/span/a/span/text()').getall()
        tags.pop(0)
        item['Tag'] = tags

        yield item
