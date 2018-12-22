import re

from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from Crawler.util import *
from Crawler.items import NewsItem


class QhtbSpider(CrawlSpider):
    name = 'qhtb'
    allowed_domains = [
        'www.qhtb.cn'
    ]

    start_urls = [
        'http://www.qhtb.cn/'
    ]

    deny_urls = [
        r'.*?/radio/.*?',
    ]

    deny_domains = [
        'www.qhtb.cn/radio'
    ]

    rules = (
        Rule(LinkExtractor(allow=r".*?www.qhtb.cn/.*?/\d{4}-\d{2}-\d{2}/\.*?", deny=r".*?www.qhtb.cn/.*?"),follow=True),
        Rule(LinkExtractor(allow=r".*?www.qhtb.cn/.*?", deny=deny_urls),callback="parse_item", follow=True)
    )
    @staticmethod
    def parse_item(response):
        print('ok')
        sel = Selector(response)
        url = response.request.url
        if re.match(r'.*?/\d{4}-\d{2}-\d{2}/.*?', url):
            print('---------------------')
            print(url)
            content = response.xpath('/html/body/div[4]/div[1]/div[1]/div[1]/div[2]//p//text()').extract()
            print(content)
            # 移除编辑
            editor = response.xpath('//*[@class="-articleeditor"]/text()').extract_first()
            if editor:
                content.remove(editor)
            publish_time = sel.re(r'\d{4}.\d{2}.\d{2}')[0]
            print(publish_time)
            if ' ' in publish_time:
                publish_time = publish_time.replace(' ', '')

            if content:
                item = NewsItem(
                    domainname='http://www.qhtb.cn/',
                    chinesename='tibetxinhua',
                    url=sel.root.base,
                    title=sel.css('.article-title .contenttitle a::text').extract_first(),
                    subtitle=sel.css('.sub::text').extract_first(),
                    language='藏文',
                    encodingtype='utf-8',
                    corpustype='网络',
                    timeofpublish=publish_time,
                    content=''.join(content),
                    source=sel.css('#Articlely > div.laiyuan > a::text').extract_first(),
                    author=sel.css('#contentK > div.xinxi > span:nth-child(3)::text').extract_first()
                )
                print(item.get("title", None))
                print(item.get("timeofpublish", None))
                print(item.get("source", None))
                print(item.get("author", None))
                # yield item
                # item = judge_time_news(item)
                # if item:
                yield item