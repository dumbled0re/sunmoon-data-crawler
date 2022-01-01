from sqlalchemy import Column, create_engine, func
from sqlalchemy.sql.sqltypes import TEXT, TIMESTAMP, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import dotenv

dotenv.load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DATABASEURL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

Base = declarative_base()
engine = create_engine(DATABASEURL, echo=False)
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

class Bus(Base):
    __tablename__ = 'sunmoon_bus'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    title = Column(TEXT)
    creation_date = Column(TEXT)
    url = Column(TEXT)

    # 更新日時
    title_updated_at = Column(TIMESTAMP(timezone=True), default=func.now())
    creation_date_updated_at = Column(TIMESTAMP(timezone=True), default=func.now())

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

def create_table():
    Base.metadata.create_all(engine)

def recreate_table():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def add_several_company_records(bus_list):
    bus = [Bus(**dc) for dc in bus_list]
    session.bulk_save_objects(bus, return_defaults=True)
    session.commit()

def update_several_company_records(bus_list):
    session.bulk_update_mappings(Bus, bus_list)
    session.commit()

def query_all_bus_records():
    records = session.query(Bus).all()
    return records

def query_all_bus_id():
    records = session.query(Bus.company_id).all()
    return records
