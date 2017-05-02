# -*- coding: utf-8 -*-
import scrapy


class AmcalSpider(scrapy.Spider):
    name = "amcal"
    allowed_domains = ["amcal.com.au"]
    start_urls = ['http://amcal.com.au/']

    def parse(self, response):
        pass
