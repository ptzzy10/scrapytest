import logging

import sys
from scrapy import Request, FormRequest
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler(sys.stdout)])

class LoginGitSpider(CrawlSpider):
    name = 'logingit'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']
    rules = (
        # 消息列表
        Rule(LinkExtractor(allow=('/issues/\d+',),
                           restrict_xpaths='//ul[starts-with(@class, "table-list")]/li/div[2]/a[2]'),
             callback='parse_page'),
        # 下一页, If callback is None follow defaults to True, otherwise it defaults to False
        Rule(LinkExtractor(restrict_xpaths='//a[@class="next_page"]')),
    )
    post_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        "Host": "github.com",
        "Upgrade - Insecure - Requests": "1"
    }


    def start_requests(self):
        return [Request('https://github.com/login',
                        meta={'cookiejar':1},callback=self.post_login)]

    def post_login(self,response):
        authenticity_token = response.xpath(
            '//input[@name = "authenticity_token"]/@value'
        ).extract_first()

        logging.info('authenticity_token = '+authenticity_token)

        return [FormRequest.from_response(response,
                                          url='https://github.com/session',
                                          meta={'cookiejar': response.meta['cookiejar']},
                                          headers=self.post_headers,  # 注意此处的headers
                                          formdata={
                                              'commit':'Sign in',
                                              'utf8': '✓',
                                              'login': '282233803@qq.com',
                                              'password': 'zzy830725',
                                              'authenticity_token': authenticity_token
                                          },
                                          callback=self.after_login,
                                          dont_filter=False
                                          )]

    def after_login(self, response):
        # 登录之后，开始进入我要爬取的私信页面
        for url in self.start_urls:
            logging.info('letter url=' + url)
            # 因为我们上面定义了Rule，所以只需要简单的生成初始爬取Request即可
            # yield self.make_requests_from_url(url)
            yield Request(url, meta={'cookiejar': response.meta['cookiejar']})
            # 如果是普通的Spider，而不是CrawlerSpider，没有定义Rule规则，
            # 那么就需要像下面这样定义每个Request的callback
            # yield Request(url, dont_filter=True,
            #               # meta={'dont_redirect': True,
            #               #       'handle_httpstatus_list': [302]},
            #               callback=self.parse_page, )

    def parse_page(self, response):
        """这个是使用LinkExtractor自动处理链接以及`下一页`"""
        logging.info(u'--------------消息分割线-----------------')
        logging.info(response.url)
        issue_title = response.xpath(
            '//span[@class="js-issue-title"]/text()').extract_first()
        logging.info(u'issue_title：' + issue_title.encode('utf-8'))

        # def parse_page(self, response):
        #     """这个是不使用LinkExtractor我自己手动处理链接以及下一页"""
        #     logging.info(response.url)
        #     for each_msg in response.xpath('//ul[@class="Msgs"]/li'):
        #         logging.info('--------------消息分割线-----------------')
        #         logging.info(''.join(each_msg.xpath('.//div[@class="msg"]//*/text()').extract()))
        #     next_page = response.xpath('//li[@class="page next"]/a')
        #     if next_page:
        #         logging.info(u'继续处理下一页')
        #         yield Request(response.url + next_page.xpath('@href').extract())
        #     else:
        #         logging.info(u"已经处理完成，没有下一页了")

    def _requests_to_follow(self, response):
        """重写加入cookiejar的更新"""
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [l for l in rule.link_extractor.extract_links(response) if l not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = Request(url=link.url, callback=self._response_downloaded)
                # 下面这句是我重写的
                r.meta.update(rule=n, link_text=link.text, cookiejar=response.meta['cookiejar'])
                yield rule.process_request(r)
