import time

from scrapy import Spider

from spider.items import SunmoonItem
from spider.models import Driver, SunmoonBus
from spider.utils.constants import BUS_LOG
from spider.utils.logger import get_logger
from spider.utils.slack_notify import SlackNotify
from spider.utils.spider_utils import SpiderUtils

logger = get_logger(__name__, BUS_LOG)


class SpiderPipeline:
    """スパイダーから引き渡されたアイテムオブジェクトを処理するパイプライン"""

    def __init__(self) -> None:
        self._sunmoon_bus = SunmoonBus()
        self._db_driver = Driver()
        self._spider_utils = SpiderUtils()
        self._slack = SlackNotify()
        self._bus_list: list[dict[str, str]] = list()
        self._num_data: int = 0

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

    def process_item(self, item: SunmoonItem, spider: Spider) -> SunmoonItem:
        """DB保存前にインスタンスごとにバルクに保存し、DBへのアクセス頻度を調整するメソッド

        Args:
            item (SunmoonItem): スパイダーから返されるアイテムオブジェクト
            spider (Spider): スパイダークラスのインスタンス
        Returns:
            item: DBに保存するアイテムオブジェクト
        """

        try:
            if isinstance(item, SunmoonItem):
                bus_rows = dict(item)
                self._bus_list.append(bus_rows)
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
            if self._bus_list:
                self._sunmoon_bus.bulk_insert(self._bus_list)
                self._num_data += len(self._bus_list)
        except Exception as error:
            logger.exception(error, extra=dict(spider=spider))
            raise

        elapsed_time = int(time.time() - self.start_time)

        elapsed_hour = elapsed_time // 3600
        elapsed_minute = (elapsed_time % 3600) // 60
        elapsed_second = elapsed_time % 3600 % 60

        elapsed_time_format = f"{str(elapsed_hour).zfill(2)}:{str(elapsed_minute).zfill(2)}:{str(elapsed_second).zfill(2)}"

        logger.info(
            f"[Sunmoon] 追加件数{self._num_data}件 収集時間: {elapsed_time_format}"
        )
        self._slack.slack_notify(
            f"[Sunmoon] 追加件数{self._num_data}件 収集時間: {elapsed_time_format}"
        )
