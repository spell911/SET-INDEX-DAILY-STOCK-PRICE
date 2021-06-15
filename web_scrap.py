# use scrapy library
import scrapy
# for running the spider
from scrapy.crawler import CrawlerProcess
from datetime import date
from mongo_db import MongoDB

mongo = MongoDB()

class SetIndexSpider(scrapy.Spider):
    """
    Scrap the set index stock price data to json.

    """
    name = "set_index_stock_price"
    # start_requests to marketdata.set

    def start_requests(self):
        """
        Start request website.

        """
        yield scrapy.Request(url='https://marketdata.set.or.th/mkt/marketsummary.do', callback=self.parse_table)
    # parse method

    def parse_table(self, response):
        """
        Parse the data we interesting, In case is set stock price.
        Then put them to json format.

        """
        #table_blocks = response.xpath('//*[@class="table table-info"]//tbody')
        for row in response.xpath('//*[@class="table-info"]//tbody//tr'):
            index_ = row.xpath('td[1]//a//text()').extract_first()
            if index_ is None:
                index_ = row.xpath('td[1]//text()').extract_first().strip()
            stock = {
                'date_': date.today().strftime("%Y-%m-%d"),
                'index_': index_,
                'price': row.xpath('td[2]//text()').extract_first(),
                'change': row.xpath('td[3]//font//text()').extract_first(),
                'change_percent': row.xpath('td[4]//font//text()').extract_first(),
                'high': row.xpath('td[5]//text()').extract_first(),
                'low': row.xpath('td[6]//text()').extract_first(),
                'volume': row.xpath('td[7]//text()').extract_first(),
                'value': row.xpath('td[8]//text()').extract_first()
            }
            obj_id = mongo.insert_one(stock)
            print('obj_id : {}'.format(obj_id))
            pass


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(SetIndexSpider)
    process.start()
