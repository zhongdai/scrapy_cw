# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from os import path
from healthcare.items import CWItem

class CwSpider(scrapy.Spider):
    name = "cw"
    allowed_domains = ["www.chemistwarehouse.com.au"]
    start_urls = ['http://www.chemistwarehouse.com.au/Shop-Online/81/Vitamins',
                  'http://www.chemistwarehouse.com.au/Shop-Online/542/Fragrances',
                  'http://www.chemistwarehouse.com.au/Shop-Online/257/Beauty',
                  'http://www.chemistwarehouse.com.au/Shop-Online/258/Medicines',
                  'http://www.chemistwarehouse.com.au/Shop-Online/256/Health',
                  'http://www.chemistwarehouse.com.au/Shop-Online/159/OralHygieneAndDentalCare',
                  'http://www.chemistwarehouse.com.au/Shop-Online/20/BabyCare',
                  'http://www.chemistwarehouse.com.au/Shop-Online/129/HairCare']

    def parse(self, response):
        category = path.basename(response.url)
        products = response.xpath('//div[@class="product-list-container"]//td')
        for prod in products:
            p = CWItem()
            p['sku'] = prod.xpath('input/@value').extract_first()
            p['name'] = prod.xpath('a//div[@class="product-image"]/img/@alt').extract_first()
            p['url'] = prod.xpath('a/@href').extract_first()
            p['saved'] = prod.xpath('a//span[@class="Save"]/text()').extract_first()
            p['price'] = prod.xpath('a//span[@class="Price"]/text()').extract_first()

            if p['saved']:
                p['saved'] = p['saved'].strip()

            if p['price']:
                p['price'] = p['price'].strip()

            if p['url']:
                p['url'] = response.urljoin(p['url'])

            yield p

        page_urls = response.xpath('//div[@class="pager-results"][1]/a/@href').extract()
        for url in page_urls:
            yield Request(url = response.urljoin(url),
                          callback = self.parse)
