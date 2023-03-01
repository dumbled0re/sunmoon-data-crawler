#! /bin/bash
cd /home/ec2-user/sunmoon-data-crawler
docker exec my_scrapy scrapy crawl sunmoon_spider_update
