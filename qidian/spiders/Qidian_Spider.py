from scrapy import Spider, Request
from qidian.items import QidianItem,xiaoshuoItem

from lxml import etree
import re


class QidianSpider(Spider):#全部完本小说信息
    name = 'qidian'

    def start_requests(self):
        url = 'https://www.qidian.com/finish'
        yield Request(url = url,callback=self.parse_page)

    def parse_page(self, response):
        selector = etree.HTML(response.text)

        max_page = selector.xpath('//div[@class="pagination fr"]/@data-pagemax')[0]
        max_page =int(max_page)
        for i in range(max_page):#获取完本小说的所有页码
            url = 'https://www.qidian.com/finish?action=hidden&orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=2&page={}'.format(str(i+1))
            yield Request(url=url,callback=self.parse_id)
    def parse_id(self, response):
        selector = etree.HTML(response.text)
        ids = selector.xpath('//div[@class="book-mid-info"]/h4/a/@data-bid')
        for id in ids:
            url_id ='https://book.qidian.com/info/{}'.format(str(id))
            #url_id = 'https://book.qidian.com/info/3242304'
            yield Request(url=url_id,meta={'id':id},callback=self.parse_info)

    def parse_info(self,response):
        selector = etree.HTML(response.text)
        item = QidianItem()
        item['id'] = response.meta['id']
        item['name'] =selector.xpath('//div[@class="book-info "]/h1/em/text()')[0]
        item['author'] =selector.xpath('//div[@class="book-info "]/h1/span/a/text()')[0]
        item['introduce'] =selector.xpath('//p[@class="intro"]/text()')[0]
        item['yuepiao'] =selector.xpath('//p[@class="num"]/i/text()')[0]
        item['dashang'] =selector.xpath('//i[@class="rewardNum"]/text()')[0]
        yield item





class FreeSpoder(Spider):#免费小说信息加内容：无序
    name = 'free'

    def start_requests(self):
        url = 'https://www.qidian.com/free/all'
        yield Request(url = url,callback=self.parse_page)

    def parse_page(self, response):#获取总页码
        selector = etree.HTML(response.text)

        max_page = selector.xpath('//div[@class="pagination fr"]/@data-pagemax')[0]
        max_page =int(max_page)
        #for i in range(max_page):#获取完本小说的所有页码
        for i in range(max_page):#获取完本小说的所有页码

            url = 'https://www.qidian.com/free/all?orderId=&vip=hidden&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=1&page={}'.format(str(i+1))
            yield Request(url=url,callback=self.parse_id)

    def parse_id(self, response):
        selector = etree.HTML(response.text)
        ids = selector.xpath('//div[@class="book-mid-info"]/h4/a/@data-bid')
        for id in ids:
            url_id ='https://book.qidian.com/info/{}#Catalog'.format(str(id))
            #url_id ='https://book.qidian.com/info/1011283836#Catalog'
            yield Request(url=url_id,meta={'id':id},callback=self.parse_chapter)

    def parse_chapter(self,response):
        selector = etree.HTML(response.text)
        id = response.meta['id']
        title = selector.xpath('//ul[@class="cf"]/li/a/text()')
        title_urls=selector.xpath('//ul[@class="cf"]/li/a/@href')
        name =selector.xpath('//div[@class="book-info "]/h1/em/text()')



        for index in  range(len(title_urls)):

            url = 'https://'+title_urls[index]


            #url = 'https://read.qidian.com/chapter/v7qgwK_WRqBH9vdK3C5yvw2/MUXVNej_isf4p8iEw--PPw2'
            yield Request(url = url,meta={'id':id,'name':name},callback=self.parse_info)

    def parse_info(self,response):
         selector = etree.HTML(response.text)
         title = selector.xpath('//div[@class="text-head"]/h3/text()')
         infos =selector.xpath('//div[@class="read-content j_readContent"]/p/text()')
         info = ' '.join(infos)
         item = xiaoshuoItem()
         item["id"] = response.meta['id']
         item['title']= response.meta['name']
         item['chapter']=title
         item['info']=info


         yield item
class FreeSpoders(Spider):#免费小说信息加内容：有序
    name = 'frees'

    def start_requests(self):
        url = 'https://www.qidian.com/free/all'
        yield Request(url = url,callback=self.parse_page)

    def parse_page(self, response):#获取总页码
        selector = etree.HTML(response.text)

        max_page = selector.xpath('//div[@class="pagination fr"]/@data-pagemax')[0]
        max_page =int(max_page)
        #for i in range(max_page):#获取完本小说的所有页码
        for i in range(1):#获取完本小说的所有页码

            url = 'https://www.qidian.com/free/all?orderId=&vip=hidden&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=1&page={}'.format(str(i+1))
            yield Request(url=url,callback=self.parse_id)

    def parse_id(self, response):
        selector = etree.HTML(response.text)
        ids = selector.xpath('//div[@class="book-mid-info"]/h4/a/@data-bid')
        for id in ids:
            #url_id ='https://book.qidian.com/info/{}#Catalog'.format(str(id))
            url_id ='https://book.qidian.com/info/1011283836#Catalog'
            yield Request(url=url_id,meta={'id':id},callback=self.parse_chapter)

    def parse_chapter(self,response):
        selector = etree.HTML(response.text)
        id = response.meta['id']
        name =selector.xpath('//div[@class="book-info "]/h1/em/text()')
        first_chapter = selector.xpath('//a[@class="red-btn J-getJumpUrl "]/@href')[0]
        first_url = 'https:'+first_chapter
        #first_url = 'https://read.qidian.com/chapter/v7qgwK_WRqBH9vdK3C5yvw2/rCM7Ofs7oqHgn4SMoDUcDQ2'

        yield Request(url = first_url,meta={'id':id,'name':name},callback=self.parse_info)



    def parse_info(self,response):
         selector = etree.HTML(response.text)
         last = selector.xpath('//a[@id="j_chapterNext"]/text()')
         title = selector.xpath('//div[@class="text-head"]/h3/text()')
         infos =selector.xpath('//div[@class="read-content j_readContent"]/p/text()')
         info = ' '.join(infos)
         id = response.meta['id']
         name = response.meta['name']
         item = xiaoshuoItem()
         item["id"] = id
         item['title']= name
         item['chapter']=title
         item['info']=info
         yield item



         next_chapter = selector.xpath('//a[@id="j_chapterNext"]/@href')[0]
         YN = selector.xpath('//a[@id="j_chapterNext"]/text()')[0]

         if str(YN) == '下一章':
             next_url = 'http:'+next_chapter
             yield Request(url = next_url,meta={'id':id,'name':name},callback=self.parse_info)

         else:

             return None



























