crawl:
	@poetry run scrapy crawl sunmoon_spider

crawl_update:
	@poetry run scrapy crawl sunmoon_spider_update

install:
	@poetry install
	@poetry run pre-commit install

pre-commit-check:
	@poetry run pre-commit run --all-files
