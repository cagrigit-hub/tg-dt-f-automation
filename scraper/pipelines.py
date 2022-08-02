# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
import requests
from collections import defaultdict


class ScraperPipeline:
    def __init__(self) -> None:
        self.telegram_addr = {"telegram_address": []}

    def process_item(self, item, spider):
        self.telegram_addr["telegram_address"].append(item["telegram_address"])
        return item["telegram_address"][13:]

    def close_spider(self, spider):

        requests.post(
            "https://tg-dataflex-automation-tlyflhffza-ey.a.run.app/telegram",
            data=json.dumps(self.telegram_addr),
        )
        self.telegram_addr = {"telegram_address": []}
