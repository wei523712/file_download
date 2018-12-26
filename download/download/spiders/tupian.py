# -*- coding: utf-8 -*-
import scrapy


class TupianSpider(scrapy.Spider):
    name = 'tupian'
    allowed_domains = ['image.so.com']
    start_urls = ['http://image.so.com/']

    def parse(self, response):
        pass
