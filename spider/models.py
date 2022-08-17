from typing import Any

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


class Semester(BASE):
    __tablename__ = "semester_bus"
    bus_id = Column(Integer, primary_key=True, comment="DBで付与されるid")
    crawled_url = Column(TEXT, nullable=False, unique=True, comment="参照URL")
    start_date = Column(TEXT, comment="始まりの記載日時")
    end_date = Column(TEXT, comment="終わりの記載日時")
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
    def select_all() -> dict[int, Any]:
        """
        学期中のバス情報をすべて取得
        """
        res = db_adapter.session.query(Semester).all()
        return dict(zip([r.id for r in res], [r for r in res]))

    @staticmethod
    def bulk_insert(bus_list: list[dict[str, str]]) -> None:
        """
        バス情報をまとめて保存
        """
        buses = [Semester(**dc) for dc in bus_list]
        db_adapter.session.bulk_save_objects(buses, return_defaults=True)
        db_adapter.session.commit()

    @staticmethod
    def bulk_update(bus_list: list[dict[str, str]]) -> None:
        """
        バス情報をまとめて更新
        """
        db_adapter.session.bulk_update_mappings(Semester, bus_list)
        db_adapter.session.commit()


class Holiday(BASE):
    __tablename__ = "holiday_bus"
    bus_id = Column(Integer, primary_key=True, comment="DBで付与されるid")
    crawled_url = Column(TEXT, nullable=False, unique=True, comment="参照URL")
    start_date = Column(TEXT, comment="始まりの記載日時")
    end_date = Column(TEXT, comment="終わりの記載日時")
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
    def select_all() -> dict[int, Any]:
        """
        休みのバス情報をすべて取得
        """
        res = db_adapter.session.query(Semester).all()
        return dict(zip([r.id for r in res], [r for r in res]))

    @staticmethod
    def bulk_insert(bus_list: list[dict[str, str]]) -> None:
        """
        バス情報をまとめて保存
        """
        buses = [Holiday(**dc) for dc in bus_list]
        db_adapter.session.bulk_save_objects(buses, return_defaults=True)
        db_adapter.session.commit()

    @staticmethod
    def bulk_update(bus_list: list[dict[str, str]]) -> None:
        """
        バス情報をまとめて更新
        """
        db_adapter.session.bulk_update_mappings(Holiday, bus_list)
        db_adapter.session.commit()


class Driver:
    @staticmethod
    def create_tables() -> None:
        """
        テーブルの作成
        """
        db_adapter.make_tables(
            tables=[
                Semester,
                Holiday,
            ]
        )
