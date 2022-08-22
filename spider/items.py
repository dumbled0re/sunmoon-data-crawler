from itemloaders.processors import TakeFirst
from scrapy.item import Field, Item


class SunmoonItem(Item):
    start_date = Field(output_processor=TakeFirst())
    end_date = Field(output_processor=TakeFirst())
    crawled_url = Field(output_processor=TakeFirst())
    bus_type = Field(output_processor=TakeFirst())
