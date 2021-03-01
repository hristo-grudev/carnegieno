import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import CarnegienoItem
from itemloaders.processors import TakeFirst


class CarnegienoSpider(scrapy.Spider):
	name = 'carnegieno'
	start_urls = ['https://www.carnegie.no/news/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="card__link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="article__content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="article__date"]/text()[normalize-space()]').get()
		if date:
			date = re.findall(r'\d+\s[a-zA-Z]+\s\d{4}', date)[0]

		item = ItemLoader(item=CarnegienoItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
