from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SunmoonSpiderSpider(CrawlSpider):
    name = "sunmoon_spider"
    allowed_domains = ["lily.sunmoon.ac.kr"]
    start_urls = ["https://lily.sunmoon.ac.kr/"]
    rules = (
        Rule(
            LinkExtractor(allow=r"Items/"), callback="parse_item", follow=True
        ),
    )

    def parse_item(self) -> None:
        pass
