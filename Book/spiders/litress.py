import datetime
import json
import scrapy
from Book.items import BookItem


class LitressSpider(scrapy.Spider):
    name = 'litress'
    allowed_domains = ['litres.ru']

    urlPattern = 'https://api.litres.ru/foundation'
    urlBookPattern = 'https://www.litres.ru'
    imgPattern = 'https://cv7.litres.ru'

    # Обращение к api Литресса,
    # где genres/XXXXXX - код, который моджно найти в url жанра,
    # limit - колличество объектов, 
    # offset - колличество уже полученных
    # art_types=text_book - исключение аудиокниг и подкастов
    start_urls = ['https://api.litres.ru/foundation/api/genres/201591/arts/facets?art_types=text_book&genre=201591&limit=32&o=new&offset=0']
    
    #Не совсем уверен, как правильно сделать Rules для более простого обхода
    #rules = (
    #    Rule(LinkExtractor(restrict_xpaths=["//a[contains(., 'следующая >')]"]),"parse",follow=True),
    #    Rule(LinkExtractor(restrict_xpaths=['//li[@class="title"]/h2/a']),"parse_page"),
    #)


    def parse(self,response):
        j = json.loads(response.text)

        #yield {"page_num":response.url + f"  {datetime.datetime.now()}"} // Проверкаы
        if 'payload' in j:
            if 'data' in j['payload']:
                for book in j['payload']['data']:
                    yield scrapy.Request(self.urlBookPattern + book['url'],self.parse_page)

        if 'pagination' in j['payload']:
                if 'next_page' in j['payload']['pagination']:
                    yield scrapy.Request(self.urlPattern + j['payload']['pagination']['next_page'],self.parse)
                    


    def parse_page(self,response):

        item = BookItem()

        item['Name'] = response.xpath('//h1/text()').get()
        item['Author'] = response.xpath('//a[@class="biblio_book_author__link"]/span/text()').get()
        
        descDumb = ""
        for desc in response.xpath('//div[@itemprop="description"]/descendant::*/text()').getall():
            descDumb += desc

        item['Desc'] = descDumb
        item['Year'] = response.xpath('//dl[dt/text()="Дата написания:"]/dd/text()').get()
        
        item['Img'] = response.xpath('//source[@type="image/jpg"]/@srcset').get()
        item['ISBN'] = response.xpath('//dl[dt/text()="ISBN:"]/dd/text()').get()
        item['Page'] = response.xpath('//dl[dt/text()="Объем:"]/dd/text()').get()
        
        genre = []
        tags = []
        for gen in response.xpath('//a[@class="biblio_info__link"]'):
            if 'genre' in gen.xpath('@href').get():
                genre.append(f"{gen.xpath('span/text()').get()}{gen.xpath('text()').get()}")
            if 'tag' in gen.xpath('@href').get():
                tags.append(f"{gen.xpath('span/text()').get()}{gen.xpath('text()').get()}")
        item['Genre'] = genre
        item['Tag'] = tags

        yield item

# Вариант обхода по api
# Но там присутсвуют не все данные
# (Можно получить только название, авторов, картинку и ещё немного интересного)
'''
    def parse(self, response):
        
        item = BookItem()

        j = json.loads(response.text)

        if 'payload' in j:
            if 'data' in j['payload']:
                for book in j['payload']['data']:

                    item = BookItem()

                    item['Name'] = book['title']

                    autor = ""
                    for aut in book['persons']:
                        if aut['role'] == 'author':
                            autor +=aut['full_name']
                    item['Author'] = autor

                    item['Desc'] = "blank"
                    item['Year'] = "blank"
                    item['Img'] = self.imgPattern + book['cover_url']
                    item['ISBN'] = "blank"
                    item['Page'] = "blank"
                    item['Genre'] = "blank"
                    item['Tag'] = "blank"

                    yield item
        
            if 'pagination' in j['payload']:
                if 'next_page' in j['payload']['pagination']:
                    yield scrapy.Request(self.urlPattern + j['payload']['pagination']['next_page'],self.parse)
'''




    
