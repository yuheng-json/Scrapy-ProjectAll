# -*- coding: utf-8 -*-
import scrapy
from movie.items import MovieItem
'''
需求：爬取电影天堂 一级页面和二级页面的数据  该数据存储到一个item对象中
一级页面
title //div[@class="co_content8"]//table//a/text()
href //div[@class="co_content8"]//table//a/@href

http://www.ygdy8.net/html/gndy/dyzz/20181025/57658.html
二级页面
src  //div[@id="Zoom"]/span/p[1]/img[1]/@src

'''

class MvSpider(scrapy.Spider):
    name = 'mv'
    allowed_domains = ['www.ygdy8.net']
    start_urls = ['http://www.ygdy8.net/html/gndy/dyzz/index.html']
    #该方法的返回值类型  是一个可以迭代的对象
    def parse(self, response):
        a_list = response.xpath('//div[@class="co_content8"]//table//a')
        for a in a_list:
            #要注意关注seletor对象中的data属性值
            title = a.xpath('./text()').extract_first()
            href = a.xpath('./@href').extract_first()
            url = 'http://www.ygdy8.net' + href
            movie = MovieItem(title=title)
            #yield Request(参数)  url 发送的请求  callback 执行的方法  meta就是 响应时候携带的参数
            yield scrapy.Request(url=url,callback=self.parse_detail,meta={'movie':movie})
    #response就是Request方法中url执行之后的响应
    def parse_detail(self,response):
        movie = response.meta['movie']
        src = response.xpath('//div[@id="Zoom"]//p[1]/img[1]/@src').extract_first()
        movie['src']=src
        yield movie











