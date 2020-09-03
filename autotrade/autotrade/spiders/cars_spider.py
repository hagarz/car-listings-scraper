import scrapy
import pandas as pd
from openpyxl.workbook import Workbook
import json


class Cars4Spider(scrapy.Spider):
    name = "cars_spider"
    start_urls = ['https://www.autotrader.co.uk/car-search?sort=price-asc&postcode=CF241NZ&radius=1500&include-delivery-option=on&page=1']

    def parse(self, response):

        set_selector = './/li[@class="search-page__result"]'

        for car in response.xpath(set_selector):
            attribute_selector = './/ul[@class="listing-key-specs "]//li/ text()'
            price_selector = './/*[@class="vehicle-price"]/ text()'
            car_type_selector = './/a[@class="js-click-handler listing-fpa-link tracking-standard-link"]/ text()'

            yield{
                'type': list(filter(None, map(lambda s: s.strip(), car.xpath(car_type_selector).extract()))),
                'attributes': car.xpath(attribute_selector).extract(),
                'price': car.xpath(price_selector).extract(),
            }

        next_page_selector = './/a[@class="paginationMini--right__active"]/@data-paginate'
        page_num = response.xpath(next_page_selector).extract_first()
        if int(page_num) >= 100:  # limit number of pages for testing
            next_page = None
        else:
            next_page = f'https://www.autotrader.co.uk/car-search?sort=price-asc&postcode=CF241NZ&radius=1500&include-delivery-option=on&page={page_num}'

        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)



def data_to_json(attr_dict):
    filename = 'cars_4.json'
    try:
        with open(filename) as json_file:
            json_data = json.load(json_file)
            json_data['attrs'].append(attr_dict['attrs'][0])
        with open(filename, 'w') as json_file:
            json.dump(json_data, json_file)
    except FileNotFoundError:  # create file
        with open(filename, 'w') as json_file:
            json.dump(attr_dict, json_file)





# to run
# scrapy runspider scraper.py
# or, to export results to JSON:
# scrapy crawl cars_spider -o cars_s.json