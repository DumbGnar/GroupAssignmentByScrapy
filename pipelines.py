# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from groupScrapy.items import AchievementItem, ExpertItem, PatentItem
import re
import pymongo
import time

class NoneExpertPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, AchievementItem):
            return item
        if isinstance(item, PatentItem):
            return item
        #空值判断
        if not item["name"]:
            raise DropItem("")
        #修改一下expert_description格式（去掉括号）
        str_list = re.findall(r"\w*", item["expert_description"])
        item["expert_description"] = str()
        for substr in  str_list:
            item["expert_description"] += substr
        #修改expert_intro格式改为str
        altered_intro = str()
        for one_str in item["expert_intro"]:
            altered_intro += one_str
        item["expert_intro"] = altered_intro
        return item
pass

class AchievementPipeline(object):
    #初始化主键值
    def open_spider(self, spider):
        self._id = 0
        pass

    def process_item(self, item, spider):
        if isinstance(item, ExpertItem):
            return item
        if isinstance(item, PatentItem):
            return item
        if item["_id"] is None:
            raise DropItem()
        #期刊出处去掉书名号
        str_list = re.findall(r"\w+", item["periodical"])
        item["periodical"] = str()
        for substr in str_list:
            item["periodical"] += substr
        return item

class PatentPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, ExpertItem):
            return item
        if isinstance(item, AchievementItem):
            return item

        if item["publicationDate"] is None:
            raise DropItem()

        if item["author"] is not None:
            item["author"] = item["author"].split(";")
        return item

class MongoDBPipeline(object):
    #初始化数据库，连接数据库
    def open_spider(self, spider):
        #获取settings.py中的数据库信息
        host = spider.settings.get("MONGO_HOST")    #主机
        port = spider.settings.get("MONGO_PORT")    #端口
        db_name = spider.settings.get("MONGO_NAME") #数据库
        collection_expert_name = spider.settings.get("MONGO_COLLECTION_EXPERT")     #专家集合
        collection_achi_name = spider.settings.get("MONGO_COLLECTION_ACHIEVEMENT")  #专家成果集合
        collection_patent_name = spider.settings.get("MONGO_COLLECTION_PATENT")     #专家专利集合
        #连接数据库
        self.db_client = pymongo.MongoClient(host = host, port = port)      #获取客户端对象
        self.db = self.db_client[db_name]       #获取数据库对象
        self.db_expert_collection = self.db[collection_expert_name]         #获取专家信息集合
        self.db_achi_collection = self.db[collection_achi_name]             #获取专家成果集合
        self.db_patent_collection = self.db[collection_patent_name]         #获取专家专利集合
        #删除原来的集合
        self.db_expert_collection.delete_many({})
        self.db_achi_collection.delete_many({})
        self.db_patent_collection.delete_many({})
        pass
    #将item存到对应的集合中
    def process_item(self, item, spider):
        #将item转化为dict数据类型
        item_dict = dict(item)
        if isinstance(item, ExpertItem):
            #插入到专家信息集合中
            self.db_expert_collection.insert_one(item_dict)
        elif isinstance(item, AchievementItem):
            self.db_achi_collection.insert_one(item_dict)
        elif isinstance(item, PatentItem):
            self.db_patent_collection.insert_one(item_dict)
        return item
    pass
    #关闭数据库连接
    def close_spider(self, spider):
        #关闭连接工作
        self.db_client.close()

class LoggingPipeline(object):
    #以追写模式打开一个Logging文件
    def open_spider(self, spider):
        self.file = open("Spider.log", mode = 'a', encoding = "utf-8")
        self.file.write("\n")
        self.file.write("Scrapy Spider Starts! -- {0} --\n".format(str(time.strftime("%b %d %Y %H:%M:%S"))))
        self.expertCounts = 0
        self.achievementCounts = 0
        self.patentCounts = 0
    pass
    #处理（做一个简单的统计）
    def process_item(self, item, spider):
        if isinstance(item, ExpertItem):
            self.expertCounts += 1
        elif isinstance(item, AchievementItem):
            self.achievementCounts += 1
        elif isinstance(item, PatentItem):
            self.patentCounts += 1
        return item
    pass
    #处理结束
    def close_spider(self, spider):
        self.file.write("Expert : {0}\n".format(self.expertCounts))
        self.file.write("Achievement : {0}\n".format(self.achievementCounts))
        self.file.write("Patent : {0}\n".format(self.patentCounts))
        self.file.write("Scrapy Finished Successfully! -- {0} --\n".format(str(time.strftime("%b %d %Y %H:%M:%S"))))
        self.file.close()

