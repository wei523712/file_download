# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from download.items import DownloadItem

class WenjianSpider(scrapy.Spider):
    name = 'wenjian'
    allowed_domains = ['matplotlib.org']
    start_urls = ['https://matplotlib.org/examples/index.html']

    def parse(self, response):
        #le = LinkExtractor(restrict_css='div.toctree-wrapper.compound',deny='/index.html$')
        le = LinkExtractor(restrict_xpaths='//li[@class="toctree-l2"]/a')
        links = le.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,callback=self.parse_down)

    def parse_down(self,response):
        item = DownloadItem()
        href = response.xpath('//a[@class="reference external"]/@href').extract_first()
        item['file_urls'] = [response.urljoin(href)]

        yield item
