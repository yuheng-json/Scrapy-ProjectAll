# -*- coding: utf-8 -*-
import scrapy
from fang.items import FangItem
'''
通过起始的url 来获取响应  响应的页面中有所有城市的连接  
我们要获取连接中的href 和 text值  href 为了拼接成二手房的连接
（为什么要拼接呢 因为原始的href 是 http://anqing.fang.com/
二手房的连接是 http://anqing.esf.fang.com/）
text的值  为了保存item

二手房的连接获取了之后  那么再次访问 然后获取响应信息  
解析出响应信息中的房地产名字 和 单价
'''

class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    start_urls = ['http://www.fang.com/SoufunFamily.html']

    province_text = ''

    def parse(self, response):
        global province_text
        tr_list = response.xpath('//div[@class="outCont"]//tr')
        for tr in tr_list[0:-1]:
            #get方法和extract方法是一个效果
            province = tr.xpath('./td//text()')[1].get().strip()
            #局部变量和全局变量的名字一致 那么想在局部变量的作用域下引用
            #全局变量  那么需要使用global
            #if province == '其它'：
            #    continue
            if province:
                province_text = province
            else:
                province = province_text
            #当a标签下没有标签的时候使用一个/
            a_list = tr.xpath('./td/a')
            for a in a_list:
                c_name = a.xpath('./text()')[0].get()
                print(c_name)
                c_href = a.xpath('./@href').extract_first()
                #http://anqing.fang.com/
                #http://anqing.esf.fang.com/
                #http://qz.esf.fang.com/
                href = c_href.split('.')[0]
                if c_name == '北京':
                    esf_href = 'http://esf.fang.com/'
                else:
                    esf_href = href + '.esf.fang.com/'

                print('------------------')
                print(esf_href)
                fang = FangItem(province='河北',city ='唐山')
                yield scrapy.Request(url=esf_href,callback=self.parse_detail,meta={'fang':fang})
                return
    def parse_detail(self,response):
        fang = response.meta['fang']
        print(fang.get('city'))
        print('9999999999999999999999')
        print(response.url)
        name = response.xpath('//span[@class = "tit_shop"]/text()').extract_first()
        price = response.xpath('//span[@class="red"]')
        price =price.xpath('string(.)').extract_first()
        fang['name'] = name
        fang['price'] = price
        yield fang
    #     #多页的下载     二手房的连接  http://anqing.esf.fang.com/
    #     # 和 <a href="/house/i35/">5</a>的href的值
    #     # href的值 是需要二手房的连接请求的响应 才能看到
        a_list = response.xpath('//div[@id="list_D10_15"]//a')
        for a in a_list:
            a_text = a.xpath('./text()').extract_first()
            if a_text == '下一页':
                next_url = a.xpath('./@href').extract_first()
                yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_detail,
                                     meta={'fang':fang})











