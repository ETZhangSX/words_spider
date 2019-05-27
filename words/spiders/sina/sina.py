# -*- coding: utf-8 -*-

from scrapy import Request, Spider

from words import utils
from words.spiders.sina.sitemap import sitemap


class SinaSpider(Spider):
    name = 'sina'
    # allowed_domains = ['blog.sina.com.cn']
    # start_urls = ['http://blog.sina.com.cn/lm/top/ent/day.html']
    # rules = (
    #     Rule(LinkExtractor(allow=r'blog.sina.com.cn', restrict_css='table.table1 > tr'), callback='parse_user',
    #          process_request='process_user_link_request'),
    # )

    def start_requests(self):
        for city in sitemap:
            url = sitemap.get(city)
            meta = {
                'city': city
            }
            yield Request(url, meta=meta)

    @staticmethod
    def exclude(title):
        return len(title) <= 4

    def parse(self, response):
        city = response.meta['city']

        parent_css = '.hot-news, .ull, .best-list, .side-ul, .news-list'
        for title, url in utils.extract_articles(response, parent_css, exclude=self.exclude):
            print(title, url, city)
            # pcss = '.article-body'
            # rep = Request(url)
            # utils.get_article(rep, pcss)
            # print('Finished')
            utils.persist_article_abstract('sina', title, url, city)



    # def parse(self, response):
    #     link = LinkExtractor(restrict_css='ul.cont_xiaoqu > li')
    #     links = link.extract_links(response)
    #     print(type(links))
    #     for link in links:
    #         print(link)
    #     pass
