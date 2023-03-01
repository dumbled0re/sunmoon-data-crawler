import time
from datetime import datetime
from typing import Optional

from scrapy import Spider
from src.items import SunmoonItem
from src.models import Driver, SunmoonBus
from src.utils.constants import BUS_LOG
from src.utils.logger import get_logger
from src.utils.slack_notify import SlackNotify
from src.utils.spider_utils import SpiderUtils

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


class SpiderPipelineUpdate(SpiderPipeline):
    """スパイダーから引き渡されたアイテムオブジェクトを処理するパイプライン"""

    def open_spider(self, spider: Spider) -> None:
        """スパイダーの起動前に呼び出されるメソッド

        Args:
            spider (Spider): スパイダークラスのインスタンス
        """

        logger.info("[Sunmoon] 更新処理を開始")
        # self._slack.slack_notify("[Sunmoon] 更新処理を開始")
        spider.start_urls = self._sunmoon_bus.select_all_crawled_url()
        self._db_data = self._sunmoon_bus.select_all()
        self._update_data_list: list[dict[str, str]] = []
        self._is_semester = False
        self._is_holiday = False

    def process_item(self, item: SunmoonItem, spider: Spider) -> SunmoonItem:
        """DB保存前にインスタンスごとにバルクに保存し、DBへのアクセス頻度を調整するメソッド(Pipelineにデータが渡される時に実行される)

        Args:
            item (SunmoonItem): スパイダーから返されるアイテムオブジェクト
            spider (Spider): スパイダークラスのインスタンス
        Returns:
            item: DBに保存するアイテムオブジェクト
        """

        try:
            db_data = self.__get_data_from_db(item)
            if db_data:
                if self.__check_change_data(db_data, item):
                    update_data = dict(item)
                    update_data["db_id"] = db_data.get("db_id")
                    self._update_data_list.append(update_data)
                    if update_data.get("bus_type") == "semester":
                        self._is_semester = True
                    if update_data.get("bus_type") == "holiday":
                        self._is_holiday = True
                return item
            else:
                raise ValueError("ValueError")
        except ValueError as error:
            logger.exception(error, extra=dict(spider=spider))
            raise
        except Exception as error:
            logger.exception(error, extra=dict(spider=spider))
            raise

    def __get_data_from_db(
        self, item: SunmoonItem
    ) -> Optional[dict[str, str]]:
        """DBから特定のデータを取得

        Args:
            item (SunmoonItem): スパイダーから返されるアイテムオブジェクト
        Returns:
            dict : DBデータ
        """
        for data_dict in self._db_data:
            if data_dict["bus_type"] == item["bus_type"]:
                return data_dict
        return None

    def __check_change_data(
        self, db_data: dict[str, str], item: SunmoonItem
    ) -> bool:
        """既存のデータに対して変更が合ったかどうかをBOOL値で返す

        Args:
            db_data (dict): DBのデータ
            item (SunmoonItem): スパイダーから返されるアイテムオブジェクト
        Returns:
            bool: 真偽値
        """

        update_db_start_date = str(db_data["start_date"]).split()[0]
        update_db_end_date = str(db_data["end_date"]).split()[0]
        update_item_start_date = str(
            datetime.strptime(item["start_date"].replace(".", ""), "%Y%m%d")
        ).split()[0]
        update_item_end_date = str(
            datetime.strptime(item["end_date"].replace(".", ""), "%Y%m%d")
        ).split()[0]

        if (
            update_db_start_date != update_item_start_date
            or update_db_end_date != update_item_end_date
        ):
            return True
        return False

    def close_spider(self, spider: Spider) -> None:
        """スパイダー終了時に呼び出されるメソッド

        Args:
            spider (Spider): スパイダークラスのインスタンス
        """

        try:
            if self._update_data_list:
                self._sunmoon_bus.bulk_update(self._update_data_list)
        except Exception as error:
            logger.exception(error, extra=dict(spider=spider))
            raise

        if self._is_semester and self._is_holiday:
            logger.info("[Sunmoon] 学期中と休み期間の時刻表が更新されました")
            self._slack.slack_notify("[Sunmoon] 学期中と休み期間の時刻表が更新されました")
        elif self._is_semester:
            logger.info("[Sunmoon] 学期中の時刻表が更新されました")
            self._slack.slack_notify("[Sunmoon] 学期中の時刻表が更新されました")
        elif self._is_holiday:
            logger.info("[Sunmoon] 休み期間の時刻表が更新されました")
            self._slack.slack_notify("[Sunmoon] 休み期間の時刻表が更新されました")
        else:
            logger.info("[Sunmoon] 更新されていませんでした")
