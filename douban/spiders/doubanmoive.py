# -*- coding: utf-8 -*-
import scrapy
from douban import items

class DoubanmoiveSpider(scrapy.Spider):
    name = 'doubanmoive'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250?start=0&filter=']
    offset = 0

    def parse(self, response):
        movies = response.xpath("//div[@class=\"info\"]")  # 挖掘所有info,div
        for movie in movies:
            doubanitem = items.DoubanItem()
            doubanitem["title"] = movie.xpath(".//span[@class=\"title\"][1]/text()").extract()[0]
            doubanitem["info"] = movie.xpath(".//div[@class=\"bd\"]/p/text()").extract()[0]
            doubanitem["star"] = movie.xpath(".//div[@class=\"star\"]/span[@class=\"rating_num\"]/text()").extract()[0]
            quote = movie.xpath(".//p[@class=\"quote\"]/span/text()").extract()
            if len(quote) != 0:
                doubanitem['quote'] = quote[0]
            else:
                doubanitem['quote'] = None
            yield doubanitem
        if self.offset < 255:
            self.offset +=25
        yield scrapy.Request("https://movie.douban.com/top250?start=" + str(self.offset) + "&filter=")
