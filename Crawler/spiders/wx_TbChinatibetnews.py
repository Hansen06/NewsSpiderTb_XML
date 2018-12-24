import re

from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from Crawler.util import *
from Crawler.items import NewsItem


class TbChinatibetnewsSpider(CrawlSpider):
    name = 'tb_chinatibetnews'

    allowed_domains = [
        'tb.chinatibetnews.com'
    ]

    start_urls = [
        'http://tb.chinatibetnews.com/'
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
        Rule(LinkExtractor(allow=r".*?tb.chinatibetnews.com/\/.*/\d{2-8}/.*?", deny=r".*?tb.chinatibetnews.com/.*?"),follow=True),
        Rule(LinkExtractor(allow=r".*?tb.chinatibetnews.com/.*?", deny=r".*?tb.chinatibetnews.com/\/.*/\d{2-8}/.*?"),callback="parse_item", follow=True)
    )

    @staticmethod
    def parse_item(response):
        sel = Selector(response)
        url = response.request.url
        if re.match(r'.*?tb.chinatibetnews.com/.*?', url):

            print('---------------------')
            print(url)

            content = response.xpath('/html/body/div[4]/div[1]/div[2]/ul[1]/li[2]/div[2]/div[1]//p//text()').extract()
            print(content)
            # 移除编辑
            editor = response.xpath('//*[@class="-articleeditor"]/text()').extract_first()
            title = response.xpath('/html/body/div[4]/div[1]/div[2]/ul[1]/li[1]/p[2]//text()').extract()
            if editor:
                content.remove(editor)
            publish_time = sel.re(r'\d{4}-\d{2}-\d{2}')[0]
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
