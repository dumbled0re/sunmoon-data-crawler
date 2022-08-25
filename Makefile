crawl:
	@poetry run scrapy crawl sunmoon_spider

crawl_update:
	@poetry run scrapy crawl sunmoon_spider_update

db_local_build:
	cd tests/docker/ && docker-compose --env-file ../../.env up -d

db_local_down:
	cd tests/docker/ && docker-compose down

data_create_table:
	@poetry run python -m tests.data.table_operations create

data_drop_table:
	@poetry run python -m tests.data.table_operations drop

install:
	@poetry install
	@poetry run pre-commit install

pre-commit-check:
	@poetry run pre-commit run --all-files
