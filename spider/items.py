from itemloaders.processors import TakeFirst
from scrapy.item import Field, Item


class SemesterItem(Item):
    start_date = Field(output_processor=TakeFirst())
    end_date = Field(output_processor=TakeFirst())
    crawled_url = Field(output_processor=TakeFirst())


class HolidayItem(Item):
    start_date = Field(output_processor=TakeFirst())
    end_date = Field(output_processor=TakeFirst())
    crawled_url = Field(output_processor=TakeFirst())
