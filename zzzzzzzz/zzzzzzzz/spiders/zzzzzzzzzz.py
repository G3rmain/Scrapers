import scrapy
import json
import time

from datetime import datetime
from datetime import timedelta

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from .filesystem import FileCsv


class XxxxxxxxSpider(CrawlSpider):
    name = 'xxxxxxx'
    file_obj = None
    terminals = {}

    def start_requests(self):
        self.file_obj = FileCsv()
        urls = ['https://xxxxxxxxxxxx.com']
        for url in urls:
            yield Request(url=url, callback=self.parse_origins)

    def parse_origins(self, response):
        source = Selector(response)
        origins = source.xpath('//option/@value').getall()
        terminals_dict = source.xpath('//option')
        for term in terminals_dict:
            self.terminals[term.xpath('.//@value').get()] = term.xpath('.//text()').get()
        for origin in origins:
            url = 'https://xxxxxxxxxxxx.com'
            yield Request(url=url, callback=self.parse_destinations)

    def parse_destinations(self, response):
        origin = response.url.split('?')[1].split('=')[1]
        destinations = Selector(response)
        destinations = destinations.xpath('//option/@value').getall()
        for destination in destinations:
            for n in range(1, 2):
                today = datetime.today()
                date = today + timedelta(days=n)
                date = date.date().strftime('%d/%m/%Y')
                url = 'https://xxxxxxxxxxxx.com'
                yield Request(url=url, callback=self.parse_item, meta={'origin': origin, 'destination': destination, 'date': date})

    def parse_item(self, response):
        data = json.loads(response.body, encoding='cp1252')

        if data:
            if "error" in data:
                print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
            else:
                results = data

            for result in results:
                today = datetime.now()

                origin = self.terminals[response.meta['origin']]
                destination = self.terminals[response.meta['destination']]
                base_price = result["Costomayor"]
                if result['ClaveServicio'] == '0':
                    continue
                promo_price = 0
                if base_price != result["Costodescuento"]:
                    promo_price = result["Costodescuento"]

                item = {
                    'date_process': today.date().strftime('%d/%m/%Y'),
                    'time_process': today.time().strftime('%H:%M:%S'),
                    'id_sitio': 'www.xxxxxxxxxxxxx.com.mx',
                    'departure_date': result['FechaSalidaBoleto'],
                    'departure_time': result["HoraSalida"],
                    'brand': result['DescripcionEmpresaCorrida'],
                    'origin': origin,
                    'destination': destination,
                    'base_price': base_price,
                    'promo_price': promo_price,
                    'service_type': result['ClaveServicio'],
                    'route_type': result["Viaje"]
                }
                self.file_obj.add_row(item)
