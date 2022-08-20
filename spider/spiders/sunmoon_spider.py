from scrapy.http.response.html import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule

from spider.items import SunmoonItem
from spider.models import SunmoonBus
from spider.utils.spider_utils import SpiderUtils


class SunmoonSpider(CrawlSpider):
    name: str = "sunmoon_spider"
    allowed_domains: list[str] = ["sunmoon.ac.kr"]
    custom_settings: dict[str, dict[str, int]] = {
        "ITEM_PIPELINES": {
            "spider.pipelines.SpiderPipeline": 300,
        }
    }

    rules = (
        # NOTE: 学期中の時刻表
        Rule(
            LinkExtractor(restrict_text="학기 시간표"),
            callback="semester_item",
            follow=False,
        ),
        # NOTE: 休みの時刻表
        Rule(
            LinkExtractor(restrict_text="방학 시간표"),
            callback="holiday_item",
            follow=False,
        ),
    )

    def semester_item(self, response: HtmlResponse) -> ItemLoader:
        semester_item: ItemLoader = SpiderUtils.add_value_to_semester_item(
            semester_item=ItemLoader(item=SunmoonItem(), response=response),
            response=response,
        )

        return semester_item.load_item()

    def holiday_item(self, response: HtmlResponse) -> ItemLoader:
        holiday_item: ItemLoader = SpiderUtils.add_value_to_holiday_item(
            holiday_item=ItemLoader(item=SunmoonItem(), response=response),
            response=response,
        )

        return holiday_item.load_item()


class SunmoonSpiderUpdate(SunmoonSpider):
    name: str = "sunmoon_spider_update"
    allowed_domains: list[str] = ["sunmoon.ac.kr"]
    custom_settings: dict[str, dict[str, int]] = {
        "ITEM_PIPELINES": {
            "spider.pipelines.SpiderPipelineUpdate": 300,
        }
    }

    bus_dict: dict[str, str] = SunmoonBus.select_crawled_url_and_bus_type()

    def parse_item(self, response: HtmlResponse) -> ItemLoader:
        if self.bus_dict.get(response.url) == "semester":
            semester_item: ItemLoader = SpiderUtils.add_value_to_semester_item(
                semester_item=ItemLoader(
                    item=SunmoonItem(), response=response
                ),
                response=response,
            )
            return semester_item.load_item()

        if self.bus_dict.get(response.url) == "holiday":
            holiday_item: ItemLoader = SpiderUtils.add_value_to_holiday_item(
                holiday_item=ItemLoader(item=SunmoonItem(), response=response),
                response=response,
            )
            return holiday_item.load_item()
