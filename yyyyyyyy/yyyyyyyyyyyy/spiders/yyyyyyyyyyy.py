import scrapy
import json
import time
import os

from datetime import datetime
from datetime import timedelta

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.selector import Selector
from .filesystem import FileCsv


class YyyyyyyyyyyyyySpider(CrawlSpider):
    name = 'xxxxxxxxxxx'
    file_obj = None
    stations = []

    def start_requests(self):
        self.file_obj = FileCsv()
        urls = ['https://Yyyyyyyyyy.com']
        for url in urls:
            yield Request(
                url=url,
                callback=self.parse_origins,)

    def parse_origins(self, response):
        source = json.loads(response.body)
        stations = source['data']['stations']
        for origin in stations:
            url = 'https://Yyyyyyyyyy.com'
            yield Request(
                url=url,
                callback=self.parse_destinations,
                meta={'origin': origin})

    def parse_destinations(self, response):
        source = json.loads(response.body)
        origin = response.meta['origin']
        destinations = source['data']['stations']
        today = datetime.today()
        for destination in destinations:
            for n in range(1, int(os.environ.get('DAYS_SCRAPING', 10))):
                date = today + timedelta(days=n)
                date = date.date().strftime('%d-%m-%Y')
                url = 'https://Yyyyyyyyyy.com'
                yield Request(
                    url=url,
                    callback=self.parse_items,
                    headers={
                        'Accept': 'application/json, text/plain, */*',
                        'Accept-Language': 'es',
                        'Origin': 'https://Yyyyyyyyyy.com',
                        'Referer': 'https://Yyyyyyyyyy.com',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                        'x-api-key': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
                        },
                    meta={
                        'origin': origin,
                        'destination': destination
                        })

    def parse_items(self, response):
        data = json.loads(response.body)
        categories = {
            'luxury': 'Lujo',
            'economy plus': 'Económico',
            'economy': 'Económico'
        }

        if data:
            if "error" in data:
                print('Error in parse_items')
            else:
                results = data['data']['outbound_routes']

            for result in results:
                today = datetime.now()
                origin = result['origin_name']
                destination = result['destination_name']
                base_price = "{:.2f}".format(result["original_price"])
                promo_price = "0.00"
                if base_price != "{:.2f}".format(result["price"]):
                    promo_price = "{:.2f}".format(result["price"])
                if result['local']:
                    route_type = 'Local'
                else:
                    route_type = 'De paso'

                item = {
                    'date_process': today.date().strftime('%d/%m/%Y'),
                    'time_process': today.time().strftime('%H:%M:%S'),
                    'id_sitio': 'www.xxxxxxxxxxx.com.mx',
                    'departure_date': result['departure_date'],
                    'departure_time': result["departure_time"],
                    'brand': result['cabin_type_ws'],
                    'origin': origin,
                    'destination': destination,
                    'base_price': base_price,
                    'promo_price': promo_price,
                    'service_type': categories[result['cabin_type']],
                    'route_type': route_type
                }
                self.file_obj.add_row(item)

