# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for href in response.xpath('//article[@class="product_pod"]//@href'):
            yield response.follow(href, self.parse_book)

        # follow pagination links
        for href in response.xpath('//li/a[text()="next"]'):
            yield response.follow(href, self.parse)

    def parse_book(self, response):
        def product_info(data):
            return '//th[text()="' + data + '"]/following-sibling::td/text()'

        yield {
            'name': response.xpath('//h1/text()').extract_first(),
            'price': response.xpath(
                '//p[@class="price_color"]/text()').extract_first(),
            'star': (response.xpath(
                '//*[contains(@class, "star-rating")]/@class'
            ).extract_first().replace('star-rating', '').strip()),
            'description': response.xpath(
                '//*[@id="content_inner"]/article/p//text()').extract_first(),

            'UPC': response.xpath(product_info('UPC')).extract_first(),
            'Product Type': response.xpath(
                product_info('Product Type')).extract_first(),
            'Price (excl. tax)': response.xpath(
                product_info('Price (excl. tax)')).extract_first(),
            'Price (incl. tax)': response.xpath(
                product_info('Price (incl. tax)')).extract_first(),
            'Tax': response.xpath(product_info('Tax')).extract_first(),
            'Availability': response.xpath(
                product_info('Availability')).extract_first(),
            'Number of reviews': response.xpath(
                product_info('Number of reviews')).extract_first(),

        }
