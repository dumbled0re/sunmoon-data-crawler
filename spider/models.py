from sqlalchemy import Column, func
from sqlalchemy.sql.sqltypes import TEXT, TIMESTAMP, Integer

from spider.utils.db_adapter import BASE, DBAdapter

db_adapter = DBAdapter(  # nosec
    dotenv_path=".env",
    env_db_host="DB_HOST",  # DB_HOST # SD_DB_HOST # MART_DB_HOST
    env_db_name="DB_NAME",  # DB_NAME # SD_DB_NAME # MART_DB_NAME
    env_db_user="DB_USER",  # DB_USER # SD_DB_USER # MART_DB_USER
    env_db_pass="DB_PASS",  # DB_PASS # SD_DB_PASS # MART_DB_PASS
    db_type="postgresql",
)


class SunmoonBus(BASE):
    __tablename__ = "sunmoon_bus"
    db_id = Column(Integer, primary_key=True, comment="DBで付与されるid")
    crawled_url = Column(TEXT, nullable=False, unique=True, comment="参照URL")
    start_date = Column(TEXT, comment="始まりの記載日時")
    end_date = Column(TEXT, comment="終わりの記載日時")
    bus_type = Column(TEXT, comment="学期中か休み中なのか")
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), comment="作成日時"
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新日時",
    )

    @staticmethod
    def select_all() -> list[dict[str, str]]:
        """
        バス情報をすべて取得
        """
        res = db_adapter.session.query(SunmoonBus).all()
        return [r.__dict__ for r in res]

    @staticmethod
    def select_all_crawled_url() -> list[str]:
        """
        参照URLをすべて取得
        """
        res = db_adapter.session.query(SunmoonBus.crawled_url).all()
        return [r.crawled_url for r in res]

    @staticmethod
    def select_crawled_url_and_bus_type() -> dict[str, str]:
        """
        参照URLとバスタイプのディクショナリを作成
        """
        res = db_adapter.session.query(
            SunmoonBus.crawled_url, SunmoonBus.bus_type
        ).all()
        return dict(
            zip([r.crawled_url for r in res], [r.bus_type for r in res])
        )

    @staticmethod
    def bulk_insert(bus_list: list[dict[str, str]]) -> None:
        """
        バス情報をまとめて保存
        """
        buses = [SunmoonBus(**dc) for dc in bus_list]
        db_adapter.session.bulk_save_objects(buses, return_defaults=True)
        db_adapter.session.commit()

    @staticmethod
    def bulk_update(bus_list: list[dict[str, str]]) -> None:
        """
        バス情報をまとめて更新
        """
        db_adapter.session.bulk_update_mappings(SunmoonBus, bus_list)
        db_adapter.session.commit()


class Driver:
    @staticmethod
    def create_tables() -> None:
        """
        テーブルの作成
        """
        db_adapter.make_tables(
            tables=[
                SunmoonBus,
            ]
        )
