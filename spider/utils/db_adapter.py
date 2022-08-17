import os
from typing import Any, Optional
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker

BASE = declarative_base()


class DBAdapterError(Exception):
    pass


def is_path_exists(path: Optional[str]) -> bool:
    if path is None or os.path.exists(path):
        return True
    raise DBAdapterError(f"{path}が存在しません！")


class DBAdapter:
    def __init__(
        self,
        dotenv_path: str,
        db_type: Optional[str] = None,
        env_db_host: Optional[str] = None,
        env_db_name: Optional[str] = None,
        env_db_user: Optional[str] = None,
        env_db_pass: Optional[str] = None,
    ):
        # dotenv_pathの存在チェック
        is_path_exists(dotenv_path)

        # dotenv読み込み
        load_dotenv(verbose=True, override=True, dotenv_path=dotenv_path)

        # 環境変数名のデフォルト
        if env_db_host is None:
            env_db_host = "DB_HOST"
        if env_db_name is None:
            env_db_name = "DB_NAME"
        if env_db_user is None:
            env_db_user = "DB_USER"
        if env_db_pass is None:
            env_db_pass = "DB_PASS"  # nosec

        # DBのデフォルト
        if db_type is None:
            db_type = "sqlite"

        self.DB_HOST = os.environ.get(env_db_host)
        self.DB_NAME = os.environ.get(env_db_name)
        self.DB_USER = os.environ.get(env_db_user)
        self.DB_PASS = os.environ.get(env_db_pass)
        self.DB_URL = self.make_db_url(db_type)

        self.__engine = create_engine(
            self.DB_URL, encoding="utf-8", echo=False
        )
        self.__session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
        )
        # log.debug(f"DB_URL: {self.DB_URL}")

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def engine(self) -> Engine:
        return self.__engine

    def make_db_url(self, db_type: str) -> str:
        # db urlの作成
        db_types = {
            "postgresql": "postgresql+psycopg2",
            "mysql": "mysql+pymysql",
            "sqlite": "sqlite",
        }
        if db_type.lower() not in db_types.keys():
            raise DBAdapterError(
                f"予期せぬ db_type が渡されました。利用できる db_type は{','.join(db_types.keys())}です"
            )
        if db_type == "sqlite":
            if self.DB_NAME:
                return f"{db_types[db_type]}:///{self.DB_NAME}.db"
            else:
                raise DBAdapterError("DB_NAME が指定されていません")
        # sqlite以外
        else:
            if self.DB_USER and self.DB_PASS and self.DB_HOST and self.DB_NAME:
                return f"{db_types[db_type]}://{self.DB_USER}:{quote_plus(self.DB_PASS)}@{self.DB_HOST}/{self.DB_NAME}"
            else:
                raise DBAdapterError("DB 接続情報が十分ではありません")

    def make_tables(self, tables: Optional[list[Any]] = None) -> None:
        if tables is None:
            tables = []
        args = {}
        if tables:
            args["tables"] = [table.__table__ for table in tables]
        BASE.metadata.create_all(bind=self.__engine, **args)

    def add(self, instance: Any) -> None:
        self.__session.add(instance=instance)
        self.__session.commit()

    def add_all(self, instances: list[Any]) -> None:
        self.__session.add_all(instances=instances)
        self.__session.commit()

    def is_exists(self, table: Any, **kwargs: Any) -> bool:
        return (
            self.__session.query(table).filter_by(**kwargs).first() is not None
        )
