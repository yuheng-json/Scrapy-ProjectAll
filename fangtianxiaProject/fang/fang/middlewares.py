# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html


class FangDownloaderMiddleware(object):

    def process_request(self, request, spider):
        request.meta['proxy']='http://112.126.65.26:12345'
        return None