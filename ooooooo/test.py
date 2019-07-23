__author__ = 'Germain'


from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from .filesystem import FileCsv


class Pregunta(Item):
    pregunta = Field()
    id = Field()
