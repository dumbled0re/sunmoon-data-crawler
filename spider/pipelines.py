import time
from typing import Union

from scrapy import Spider

from spider.items import HolidayItem, SemesterItem
from spider.models import Driver, Holiday, Semester
from spider.utils.constants import BUS_LOG
from spider.utils.logger import get_logger
from spider.utils.slack_notify import SlackNotify
from spider.utils.spider_utils import SpiderUtils

logger = get_logger(__name__, BUS_LOG)


class SpiderPipeline:
    """スパイダーから引き渡されたアイテムオブジェクトを処理するパイプライン"""

    def __init__(self) -> None:
        self._semester = Semester()
        self._holiday = Holiday()
        self._db_driver = Driver()
        self._spider_utils = SpiderUtils()
        self._slack = SlackNotify()
        self._semester_list: list[dict[str, str]] = list()
        self._holiday_list: list[dict[str, str]] = list()
        self._num_semesters: int = 0
        self._num_holidays: int = 0

    def open_spider(self, spider: Spider) -> None:
        """スパイダーの起動前に呼び出されるメソッド

        Args:
            spider (Spider): スパイダークラスのインスタンス
        """

        self.start_time = time.time()
        self._db_driver.create_tables()
        self._slack.slack_notify("[Sunmoon] 収集処理を開始")
        spider.start_urls = [
            "https://lily.sunmoon.ac.kr/Page2/About/About08_04_02_01_01_01.aspx"
        ]

    def process_item(
        self, item: Union[SemesterItem, HolidayItem], spider: Spider
    ) -> Union[SemesterItem, HolidayItem]:
        """DB保存前にインスタンスごとにバルクに保存し、DBへのアクセス頻度を調整するメソッド

        Args:
            item (SemesterItem or HolidayItem): スパイダーから返されるアイテムオブジェクト
            spider (Spider): スパイダークラスのインスタンス
        Returns:
            item: DBに保存するアイテムオブジェクト
        """

        try:
            if isinstance(item, SemesterItem):
                semester_rows = dict(item)
                self._semester_list.append(semester_rows)
                return item
        except Exception as error:
            logger.exception(error, extra=dict(spider=spider))
            raise

        try:
            if isinstance(item, HolidayItem):
                holiday_rows = dict(item)
                self._holiday_list.append(holiday_rows)
                return item
        except Exception as error:
            logger.exception(error, extra=dict(spider=spider))
            raise

    def close_spider(self, spider: Spider) -> None:
        """スパイダー終了時に呼び出されるメソッド

        Args:
            spider (Spider): スパイダークラスのインスタンス
        """

        try:
            if self._semester_list:
                self._semester.bulk_insert(self._semester_list)
                self._num_semesters += len(self._semester_list)

            if self._holiday_list:
                self._holiday.bulk_insert(self._holiday_list)
                self._num_holidays += len(self._holiday_list)

        except Exception as error:
            logger.exception(error, extra=dict(spider=spider))
            raise

        elapsed_time = int(time.time() - self.start_time)

        elapsed_hour = elapsed_time // 3600
        elapsed_minute = (elapsed_time % 3600) // 60
        elapsed_second = elapsed_time % 3600 % 60

        elapsed_time_format = f"{str(elapsed_hour).zfill(2)}:{str(elapsed_minute).zfill(2)}:{str(elapsed_second).zfill(2)}"

        logger.info(
            f"[Sunmoon] 追加件数{self._num_semesters + self._num_holidays}件 収集時間: {elapsed_time_format}"
        )
        self._slack.slack_notify(
            f"[Sunmoon] 追加件数{self._num_semesters + self._num_holidays}件 収集時間: {elapsed_time_format}"
        )
