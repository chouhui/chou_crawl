import scrapy
from fish.items.items import FishItem


class UstcSpider(scrapy.Spider):

    name = 'ustc'
    allowed_domains = ['sse.ustc.edu.cn']

    start_urls = ['https://sse.ustc.edu.cn/pages/tonz.php']

    def parse(self, response):

        item = FishItem()

        body = response.xpath('//ul[@class="list1"]/li')

        for bo in body:

            url_raw = bo.xpath('./a/@href').extract_first()
            url_pre = 'https://sse.ustc.edu.cn/'
            title = bo.xpath('./a/text()').extract_first().strip()
            date_ = bo.xpath('./a/em/text()').extract_first()


            item['url'] = url_pre + url_raw
            item['title'] = title
            item['date_'] = date_

            yield item