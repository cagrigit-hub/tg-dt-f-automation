from scraper.spiders.TeleSpider import TeleFlex
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(TeleFlex)
process.start()
