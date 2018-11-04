# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import  Rule
from movie.items import MovieItem
from scrapy_redis.spiders import RedisCrawlSpider
'''
1 修改继承的类为RedisCrawlSpider
2 导入RedisCrawlSpider的库
3 删除多余的库
4 由于默认提供的init方法不能使用 所以我们需要自己添加allowed_domains
5 注释start_urls 因为start_urls是由master给的 所以不能自己去写起始的url
eg：大哥带我们去追女生  大哥一声令下 我们才知道去追谁
6 添加redis_key  其实际就是lpush的key 也就是由master端给的起始的url
7 定义提取连接的规则
8 运行  scrapy runspider 文件的名字（fenbushi.py）
9 由master端的redis  给起始的url命令
  lpush redis_key的值  起始的url
  lpush fen:start_urls http://www.ygdy8.net/html/gndy/dyzz/index.html
10 修改settings
        ① 添加三个组件
        ② redis管道以及master的redis配置
        🌂 延迟下载 注意素质
'''


class FenbushiSpider(RedisCrawlSpider):
    name = 'fenbushi'
    allowed_domains = ['www.ygdy8.net']
    # start_urls = ['http://http://www.ygdy8.net/html/gndy/dyzz/index.html/']
    redis_key = 'fen:start_urls'

    rules = (
    Rule(LinkExtractor(allow=r'list_23_\d+.html'), callback='parse_item', follow=True),
    )
    def parse_item(self, response):
        a_list = response.xpath('//div[@class="co_content8"]//table//a')
        for a in a_list:
            # 要注意关注seletor对象中的data属性值
            title = a.xpath('./text()').extract_first()
            href = a.xpath('./@href').extract_first()
            url = 'http://www.ygdy8.net' + href
            movie = MovieItem(title=title)
            # yield Request(参数)  url 发送的请求  callback 执行的方法  meta就是 响应时候携带的参数
            yield scrapy.Request(url=url, callback=self.parse_detail, meta={'movie': movie})
        # response就是Request方法中url执行之后的响应

    def parse_detail(self, response):
        movie = response.meta['movie']
        src = response.xpath('//div[@id="Zoom"]//p[1]/img[1]/@src').extract_first()
        movie['src'] = src
        yield movie
