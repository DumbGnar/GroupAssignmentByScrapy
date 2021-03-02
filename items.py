# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ExpertItem(scrapy.Item):
    _id = scrapy.Field()            #主键
    subscriberId = scrapy.Field()   #用户ID，置为null
    email = scrapy.Field()          #邮箱
    name = scrapy.Field()    #专家姓名
    photographUrl = scrapy.Field()   #头像URL
    organization = scrapy.Field()    #机构
    researchArea = scrapy.Field()    #研究方向
    personalHomepage = scrapy.Field()   #专家主页
    updateDate = scrapy.Field()      #更新时间
    achievement = scrapy.Field()        #成果ID
    feedbackInformationId = scrapy.Field()  #反馈ID

    expert_description = scrapy.Field() #专家职务 
    expert_intro = scrapy.Field()   #个人简介

    expert_location = scrapy.Field()    #所在地区
    expert_expert = scrapy.Field()  #擅长领域 
pass

class AchievementItem(scrapy.Item):
    _id = scrapy.Field()            #主键
    title = scrapy.Field()     #文献标题    
    author = scrapy.Field()    #文献作者    
    achievementType = scrapy.Field()        #成果类型
    summary = scrapy.Field()  #文献摘要
    mainBody = scrapy.Field()   #正文
    hyperlink = scrapy.Field()       #details_URL
    downloadAddress = scrapy.Field()    #下载地址 待爬
    updateTime = scrapy.Field()     #更新时间
    periodical = scrapy.Field()     #文献对应期刊
    conference = scrapy.Field()     #会议
    pagination = scrapy.Field()     #页码
    
    achi_subject = scrapy.Field()   #关键词
    achi_article_list = scrapy.Field()  #参考文献
    
pass

class PatentItem(scrapy.Item):
    _id = scrapy.Field()        #成果ID
    title = scrapy.Field()      #标题
    author = scrapy.Field()     #作者(发明人）
    achievementtype = scrapy.Field()        #成果类型
    summary = scrapy.Field()    #摘要
    mainBody = scrapy.Field()   #正文
    hyperlink = scrapy.Field()  #链接
    downloadAddress = scrapy.Field()        #下载链接
    undateDate = scrapy.Field() #更新时间
    filingDate = scrapy.Field() #申请时间
    publicationDate = scrapy.Field()        #公开时间
    address = scrapy.Field()    #地址
    countryCode = scrapy.Field()            #国省代码
    applicationNumber = scrapy.Field()      #申请号
    publicationNumber = scrapy.Field()      #公开号

    #原数据库表中没有的
    patent_ipc = scrapy.Field()  #IPC分类
    patent_mainNumber = scrapy.Field()  #主分类号
    patent_owner = scrapy.Field()       #申请人
    patent_priorityNumber = scrapy.Field()  #优先权号
    patent_priorityDate = scrapy.Field()    #优先权日
pass
