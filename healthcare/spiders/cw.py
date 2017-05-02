# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from os import path

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
            sku = prod.xpath('input/@value').extract_first()
            name = prod.xpath('a//div[@class="product-image"]/img/@alt').extract_first()
            url = prod.xpath('a/@href').extract_first()
            save = prod.xpath('a//span[@class="Save"]/text()').extract_first()
            price = prod.xpath('a//span[@class="Price"]/text()').extract_first()

            if save:
                save = save.strip()

            if price:
                price = price.strip()

            yield {
                'category': category,
                'sku': sku,
                'name': name,
                'price': price,
                'save': save,
                'url': response.urljoin(url)
            }

        page_urls = response.xpath('//div[@class="pager-results"][1]/a/@href').extract()
        for url in page_urls:
            yield Request(url = response.urljoin(url),
                          callback = self.parse)
