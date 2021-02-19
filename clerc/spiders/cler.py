import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from clerc.items import Article


class ClerSpider(scrapy.Spider):
    name = 'cler'
    start_urls = ['https://www.cler.ch/de/bank-cler/medien']

    def parse(self, response):
        links = response.xpath('//table[@class="m-table-press-release"]//a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//div[@class="heading"]//span/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="date"]/p/text()').get()
        if date:
            date = date.strip()

        content = response.xpath("//div[@id='content']//text()").getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[3:]).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
