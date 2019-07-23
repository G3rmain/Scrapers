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


class AltaMarSpider(CrawlSpider):
    name = 'xxxxxx'
    file_obj = None
    terminals = {}

    def start_requests(self):
        self.file_obj = FileCsv()
        urls = ['https://xxxxxxxxxxxx.com']
        for url in urls:
            yield FormRequest(
                url=url,
                formdata={
                    'APPNAME': 'Navegante',
                    'PRGNAME': 'OrigenDestino',
                    'ARGUMENTS': 'a_origen,n_sesion'
                    },
                callback=self.parse_origins,
                method='POST')

    def parse_origins(self, response):
        source = json.loads(response.body, encoding='utf-8')
        origins = []
        for term in source:
            self.terminals[term['ClaveOficina']] = term['DescripcionOficina']
            origins.append(term['ClaveOficina'])
        for origin in origins:
            url = 'https://xxxxxxxxxxxx.com'
            yield FormRequest(
                url=url,
                formdata={
                    'APPNAME': 'Navegante',
                    'PRGNAME': 'OrigenDestino',
                    'ARGUMENTS': 'a_origen,n_sesion',
                    'a_origin': origin,
                    },
                callback=self.parse_destinations,
                method='POST',
                meta={'origin': origin})

    def parse_destinations(self, response):
        source = json.loads(response.body, encoding='utf-8')
        destinations = [destination['ClaveOficina'] for destination in source]
        today = datetime.today()
        for destination in destinations:
            for n in range(1, int(os.environ.get('DAYS_SCRAPING', 10))):
                date = today + timedelta(days=n)
                date = date.date().strftime('%d/%m/%Y')
                url = 'https://xxxxxxxxxxxx.com'
                yield FormRequest(
                    url=url,
                    formdata={
                        'APPNAME': 'Navegante',
                        'PRGNAME': 'RecuperaCorridasVR',
                        'ARGUMENTS': 'oficinao,oficinar,fechasal,adultos',
                        'oficinao': response.meta['origin'],
                        'oficinar': destination,
                        'fechasal': date,
                        'adultos': "1",
                        },
                    callback=self.parse_items,
                    method='POST',
                    meta={
                        'origin': response.meta['origin'],
                        'destination': destination
                        })

    def parse_items(self, response):
        body = response.text.translate({ord('('):None}).translate({ord(')'):None})
        data = json.loads(body, encoding='utf-8')
        if data:
            if "error" in data:
                print('Error in parse_items')
            else:
                results = data

            for result in results:
                if result['FechaSalidaBoleto'] == '0':
                    continue
                today = datetime.now()
                origin = self.terminals[response.meta['origin']]
                destination = self.terminals[response.meta['destination']]
                base_price = result["Tarifa"].translate({ord(' '):None})
                promo_price = "0.00"
                if base_price != result["PromoCorrida"]:
                    promo_price = result["PromoCorrida"]

                item = {
                    'date_process': today.date().strftime('%d/%m/%Y'),
                    'time_process': today.time().strftime('%H:%M:%S'),
                    'id_sitio': 'www.xxxxxx.com.mx',
                    'departure_date': result['FechaSalidaBoleto'],
                    'departure_time': result["HoraSalida"],
                    'brand': result['DescripcionEmpresaCorrida'],
                    'origin': origin,
                    'destination': destination,
                    'base_price': base_price,
                    'promo_price': promo_price,
                    'service_type': result['ClaveServicio'],
                    'route_type': result["TipoServicio"]
                }
                self.file_obj.add_row(item)

