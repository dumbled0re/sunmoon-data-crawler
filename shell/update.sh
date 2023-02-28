#! /bin/bash
cd /home/ec2-user/sunmoon-data-crawler
/home/ec2-user/.pyenv/shims/poetry run scrapy crawl sunmoon_spider_update
