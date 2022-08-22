import re

from scrapy.http.response.html import HtmlResponse
from scrapy.loader import ItemLoader

from spider.utils.constants import BUS_LOG
from spider.utils.logger import get_logger

logger = get_logger(__name__, BUS_LOG)


class SpiderUtils:

    regex_date = re.compile(r"\d{4}.\d{1,2}.\d{1,2}")

    def __init__(self) -> None:
        pass

    @staticmethod
    def preprocess_text(text: str) -> str:
        """
        文章の正規化(不要な記号の削除)
        Args:
            text (str): テキスト
        Returns:
            str: 正規化したテキスト
        """
        return bytes(
            re.sub(
                " +",
                " ",
                text.strip()
                .replace("\t", " ")
                .replace("\u3000", " ")
                .replace("\xa0", " ")
                .replace("\n", " ")
                .replace("\r", " ")
                .replace("<br/>", " ")
                .replace("\\", "\\\\"),
            ),
            "utf-8",
        ).decode("utf-8", "ignore")

    @classmethod
    def add_value_to_semester_item(
        cls, semester_item: ItemLoader, response: HtmlResponse
    ) -> ItemLoader:
        """クローリングしたデータをアイテムローダーに追加したものを返すメソッド

        Args:
            semester_item (ItemLoader): アイテム保存用のオブジェクト
            response (HtmlResponse): HTMLレスポンスオブジェクト
        Returns:
            semester_item: クローリングした学期中のバスデータを保存したアイテムローダー
        """

        start_date = None
        end_date = None

        scheduled_period = response.xpath(
            "//h4[@class='title22']/text()"
        ).get()

        scheduled_period_list = cls.regex_date.findall(scheduled_period)
        if len(scheduled_period_list) == 2:
            start_date = scheduled_period_list[0]
            end_date = scheduled_period_list[1]

        semester_item.add_value("start_date", start_date)
        semester_item.add_value("end_date", end_date)
        semester_item.add_value("crawled_url", response.url)
        semester_item.add_value("bus_type", "semester")

        return semester_item

    @classmethod
    def add_value_to_holiday_item(
        cls, holiday_item: ItemLoader, response: HtmlResponse
    ) -> ItemLoader:
        """クローリングしたデータをアイテムローダーに追加したものを返すメソッド

        Args:
            holiday_item (ItemLoader): アイテム保存用のオブジェクト
            response (HtmlResponse): HTMLレスポンスオブジェクト
        Returns:
            holiday_item: クローリングした休み中のバスデータを保存したアイテムローダー
        """

        start_date = None
        end_date = None

        scheduled_period = response.xpath(
            "//h4[@class='title22 mgT50']/span/text()"
        ).get()

        scheduled_period_list = cls.regex_date.findall(scheduled_period)
        if len(scheduled_period_list) == 2:
            start_date = scheduled_period_list[0]
            end_date = scheduled_period_list[1]

        holiday_item.add_value("start_date", start_date)
        holiday_item.add_value("end_date", end_date)
        holiday_item.add_value("crawled_url", response.url)
        holiday_item.add_value("bus_type", "holiday")

        return holiday_item
