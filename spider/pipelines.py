import scrapy


class SpiderPipeline:
    def process_item(self, item: scrapy.Item) -> scrapy.Item:
        return item
