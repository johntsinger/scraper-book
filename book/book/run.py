from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl('book', domain='scrapy.org')
process.start() # the script will block here until the crawling is finished
