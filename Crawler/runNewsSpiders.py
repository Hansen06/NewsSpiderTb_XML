from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# 运行一个
process = CrawlerProcess(get_project_settings())

process.crawl('tibet_people')
process.crawl('tibet_tibet3')
process.crawl('tb_tibet')
process.crawl('tibet_xinhua')
process.crawl('tibetcm')
process.crawl('tibet_cpc_people')
process.crawl('tb_chinatibetnews')
process.crawl('qhtb')

process.start()
