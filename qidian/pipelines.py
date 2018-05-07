# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo




class QidianPipeline(object):
    collection_name = 'user'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spiser(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #self.db[self.collection_name].update({'id': item['id']}, dict(item), True)
        self.db[self.collection_name].insert_one(dict(item))

        # id相同，只更新，不插入，去重作用。
        return 'ok!'


class QidiantextPipeline(object):

    def process_item(self, item, spider):

        title = str(item['title'][0])
        chapter= str(item['chapter'][0])
        info = str(item['info'])



        fo = open(title+'.txt', "ab+")         #打开小说文件
        # 以二进制写入章节题目 需要转换为utf-8编码，否则会出现乱码
        fo.write(('\r' + chapter + '\r\n').encode('UTF-8'))
        # 以二进制写入章节内容
        fo.write((info+'\r\n').encode('UTF-8'))
        #fo.close()
