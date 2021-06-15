from web_scrap import SetIndexSpider
from mongo_db import MongoDB
from scrapy.crawler import CrawlerProcess

import pymongo

mongo = MongoDB()

if __name__ == "__main__":
    # prep mongo
    mongo.create_database()
    mongo.create_collection()
    # start web scrap
    process = CrawlerProcess()
    process.crawl(SetIndexSpider)
    process.start()

