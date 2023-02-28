import os
import sys
from typing import Any

from dotenv import load_dotenv
from sqlalchemy import Column, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import TEXT, TIMESTAMP, Integer

load_dotenv()
Base: Any = declarative_base()


class SunmoonBus(Base):
    __tablename__ = "sunmoon_bus"
    db_id = Column(Integer, primary_key=True)
    crawled_url = Column(TEXT, nullable=False, unique=True)
    start_date = Column(TEXT)
    end_date = Column(TEXT)
    bus_type = Column(TEXT)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


def create_table() -> None:
    """
    テスト用のテーブル枠の作成
    """
    engine = create_engine(
        "postgresql://{user}:{password}@{host}:{port}/{dbname}".format(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_DOCKER_PORT", 5432),
            dbname=os.getenv("POSTGRES_DB"),
        ),
        echo=True,
    )
    Base.metadata.create_all(bind=engine)


def drop_table() -> None:
    engine = create_engine(
        "postgresql://{user}:{password}@{host}:{port}/{dbname}".format(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_DOCKER_PORT", 5432),
            dbname=os.getenv("POSTGRES_DB"),
        ),
        echo=True,
    )
    Base.metadata.drop_all(bind=engine)


if __name__ == "__main__":
    args = sys.argv
    assert len(args) >= 2, "引数が足りません"
    if args[1] == "create":
        create_table()
    elif args[1] == "drop":
        drop_table()
