create_env_local:
	cp ./.env.example ./app/.env.local

docker_build:
	cd docker/ && docker-compose --env-file ../app/.env up -d --build

docker_up:
	cd docker/ && docker-compose --env-file ../app/.env up -d

docker_down:
	cd docker/ && docker-compose down

data_create_table:
	docker exec -it my_scrapy python src/data/table_operations.py create

data_drop_table:
	docker exec -it my_scrapy python src/data/table_operations.py drop

crawl:
	docker exec -it my_scrapy scrapy crawl sunmoon_spider

crawl_update:
	docker exec -it my_scrapy scrapy crawl sunmoon_spider_update

install:
	@poetry install
	@poetry run pre-commit install

pre-commit-check:
	@poetry run pre-commit run --all-files
