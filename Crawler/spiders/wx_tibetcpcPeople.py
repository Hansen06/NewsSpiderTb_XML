import re

from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from Crawler.util import *
from Crawler.items import NewsItem

#url里只有数字
class TiTibet3Spider(CrawlSpider):
    name = 'tibet_cpc_people'
    allowed_domains = [
        'tibet.cpc.people.com.cn'
    ]

    start_urls = [
        'http://tibet.cpc.people.com.cn/'
    ]

    deny_urls = [
        # r'.*?/video/.*?',
        # r'.*?/music/.*?'
    ]
    deny_domains = [
        # 'music.tibet3.com',
        # 'ti.tibet3.com/video'
    ]

    rules = (
        Rule(LinkExtractor(allow=r".*?tibet.cpc.people.com.cn/\d{2-10}/.*?", deny=r".*?tibet.cpc.people.com.cn/.*?"), follow=True),
        Rule(LinkExtractor(allow=r".*?tibet.cpc.people.com.cn/.*?", deny=r".*?tibet.cpc.people.com.cn/\d{2-10}/.*?"),callback="parse_item", follow=True)
    )

    @staticmethod
    def parse_item(response):
        sel = Selector(response)
        url = response.request.url
        if re.match(r'.*?tibet.cpc.people.com.cn/.*?', url):

            print('---------------------')
            print(url)

            content = response.xpath('/html/body/div[4]/div[1]/p[2]//text()').extract()
            print(content)
            # 移除编辑
            editor = response.xpath('//*[@class="-articleeditor"]/text()').extract_first()
            title = response.xpath('/html/body/div[4]/h1[1]//text()').extract()
            print(title)
            if editor:
                content.remove(editor)
            publish_time = sel.re(r'\d{4}.*?\d{2}.*?\d{2}.*?\d{2}:\d{2}')[0].replace('ལོའི་ཟླ་ ', '年').replace('ཚེས་', '月').replace('ཉིན།  ', '日')
            print(publish_time)
            if ' ' in publish_time:
                publish_time = publish_time.replace(' ', '')

            if content:
                item = NewsItem(
                    domainname='http://tibet.cpc.people.com.cn/',
                    chinesename='tibet3',
                    url=sel.root.base,
                    title=''.join(title),
                    subtitle=sel.css('.sub::text').extract_first(),
                    language='藏文',
                    encodingtype='utf-8',
                    corpustype='网络',
                    timeofpublish=publish_time,
                    content=''.join(content),
                    author=None
                )
                print(item.get("title", None))
                print(item.get("timeofpublish", None))
                print(item.get("source", None))
                print(item.get("author", None))
                # yield item
                # item = judge_time_news(item)
                # if item:
                yield item
