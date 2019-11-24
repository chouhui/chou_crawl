# coding:utf_8
import scrapy
from fish.items.items import FinanceNewsItem


class UstcSpider(scrapy.Spider):

    name = 'zzw_finance'
    DOWNLOAD_DELAY = 0.5

    # allowed_domains = ['https://search.sina.com.cn']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',


    }
    cookie = 'QiHooGUID=4A5681DB291E651FF2C87DDACF993203.1563956704150; __guid=15484592.1157352840870527700.1563956705089.8806; dpr=2; webp=1; __huid=11%2BTqwVfPPXlQDTdBpkz9rmmKvB1rUA7Lf2b6sOUyL1r0%3D; _S=dh1qllajv021vaic27jtqsn885; count=9; gtHuid=1'

    cookie_l = cookie.split('; ')
    cookies = {}
    for i in cookie_l:
        k, v = i.split('=')
        cookies[k] = v
    # print cookies

    def start_requests(self):

        for i in range(1, 65):

            yield scrapy.Request("https://www.so.com/s?q=%E8%82%A1%E4%BB%B7%E4%B8%8B%E8%B7%8C&pn={}&site=ce.cn&rg=1&inurl=&psid=4bf39f656c71f69a42cf0057c112444c&src=srp_paging&fr=zz_www_ce_cn".format(i))

    def parse(self, response):

        # item = FishItem()

        body = response.xpath('//ul[@class="result"]/li')

        for res in body:
            item = FinanceNewsItem()
            titles = res.xpath('./h3/a//text()').extract()
            title = ''.join(titles)
            url = res.xpath('./h3/a/@data-url').extract_first()
            # time = res.xpath('./h2/span/text()').extract_first().split(' ', 1)[-1]

            item['title'] = title
            item['url'] = url
            # item['create_time'] = time
            try:

                yield scrapy.Request(url, meta={'item': item}, callback=self.parse2)

            except:
                print url

    def parse2(self, response):

        # print response.body
        body = response.xpath('//div[@id="articleText"]//text()').extract()

        try:
            time = response.xpath('//span[@id="articleTime"]/text()').extract_first().strip()
        except:
            time = response.xpath('//span[@class="time"]/text()').extract_first().strip()
        if not body:
            body = response.xpath('//article//p//text()').extract()
        content = ''.join(body).strip()

        if '.h2' in body[0]:
            body = body[2:]
            content = ''.join(body).strip()

        item = response.meta['item']

        item['content'] = content
        item['create_time'] = time
        item['source'] = 'zzw'

        if item['content'] and u'股价' in item['title'] and u'跌' in item['title']:

            yield item

