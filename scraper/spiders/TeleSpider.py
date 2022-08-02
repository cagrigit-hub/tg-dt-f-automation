import scrapy
from ..items import TeleflexItem

class TeleFlex(scrapy.Spider):
    name = "teleflex"
    start_urls = ["https://www.coingecko.com/en/new-cryptocurrencies"]
    # custom_settings = {"DOWNLOAD_DELAY": 0.25}
    # get everypage, send it to get-telegram-address than fetch next page
    def parse(self, response):
        coin_pages = response.css(
            "td.coin-name > div.tw-flex > div.tw-flex-auto > div.tw-flex > a::attr(href)"
        ).extract()
        yield from response.follow_all(coin_pages, self.parse_telegram_address)

        # next_pages = response.css("li.page-item a::attr(href)").extract()
        # next_pages = [item for item in next_pages if item is not "#"]
        # yield from response.follow_all(next_pages, self.parse)

    # get telegram address
    def parse_telegram_address(self, response):
        telegram_items = TeleflexItem()
        telegram_i = response.css("div.tw-flex>a>i.fa-telegram")
        telegram_address = telegram_i.xpath("../@href").extract_first()
        telegram_items["telegram_address"] = telegram_address

        if telegram_address is not None:
            yield telegram_items
