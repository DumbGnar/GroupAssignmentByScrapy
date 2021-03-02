# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import Spider
from groupScrapy.items import ExpertItem, AchievementItem, PatentItem
import re
import time

class ExpertSpider(Spider):
    #爬虫名称
    name = "Spider"
    #定义一个当前专家UID
    expert_uid = 206
    #定义一个要爬取的最大UID
    expert_max_uid = 206

    #专利爬取
    patent_year = 2006
    patent_month = 10
    patent_day = 15
    patent_last_four = 0
    #定义一个最大patent_year
    max_patent_year = 2007
    #测试用
    patent_test = True
    patent_counts = 5

    #根据当前专家UID返回专家主页url
    def get_expert_url(self):
        basic_url = "http://www.91zzj.com/Expert/ExpertInfo?uid=E"
        #要填充八位数字
        addict_url = "{0:8d}".format(self.expert_uid).replace(' ', '0', 7)
        #获得要访问的URL
        result_url = basic_url + addict_url
        return result_url
    pass

    #根据当前专家UID返回专家头像图片url，UID不变
    def get_expert_image_url(self):
        basic_url = "http://www.91zzj.com/CommanClass/avatar.ashx?size=300&uid=E"
        #要填充八位数字
        addict_url = "{0:8d}".format(self.expert_uid).replace(' ', '0', 7)
        #获得要访问的URL
        result_url = basic_url + addict_url
        return result_url
    pass

    #专利：根据当前专利选项返回专利url
    def get_patent_url(self):
        basic_url = "http://zhuanli.soqi.com/CN"
        #要填充12位专利ID号
        basic_url = basic_url + "{0:4d}".format(self.patent_year).replace(' ', '0', 3)
        basic_url = basic_url + "{0:2d}".format(self.patent_month).replace(' ', '0', 1)
        basic_url = basic_url + "{0:2d}".format(self.patent_day).replace(' ', '0', 1)
        basic_url = basic_url + "{0:4d}".format(self.patent_last_four).replace(' ', '0', 3)
        return basic_url

    #专利工具类：生成最后12位
    def get_patent_url_last12(self):
        res = "{0:4d}".format(self.patent_year).replace(' ', '0', 3) + "{0:2d}".format(self.patent_month).replace(' ', '0', 1)
        res = res + "{0:2d}".format(self.patent_day).replace(' ', '0', 1) + "{0:4d}".format(self.patent_last_four).replace(' ', '0', 3)
        res = "CN" + res
        return res
    
    #根据当前patent参数计算下一个patent参数
    def patent_move_to_next(self):
        self.patent_last_four += 1
        if self.patent_last_four >= 10000:
            self.patent_last_four = 0
            self.patent_day += 1
            if self.patent_day >= 19:
                self.patent_day = 2
                self.patent_month += 1
                if self.patent_month >= 12:
                    self.patent_month = 7
                    self.patent_year += 1
                
        
    #生成初始请求start_Request
    def start_requests(self):
        start_url = self.get_expert_url()
        yield Request(start_url, callback = self.parse)
        #不根据name查询专利
        patent_url = self.get_patent_url()
        yield Request(patent_url, callback = self.parse_patent_url)
        pass

    #根据页面爬取专利
    def parse_patent_url(self, response):
        #获取专利名
        patent_name = response.xpath("//div[@class='col-md-7 comCommerBox']/h1/text()").extract_first()
        #获取表格中的专利信息
        one_selector = response.xpath("//div[@class='col-md-7 comCommerBox']//tbody")
        #获取申请号
        applicationNumber = one_selector.xpath("./tr[1]/td[1]/text()").extract_first()
        #获取申请日
        filingDate = one_selector.xpath("./tr[2]/td[1]/text()").extract_first()
        #获取公开号
        publicationNumber = one_selector.xpath("./tr[3]/td[1]/text()").extract_first()
        #获取公开日
        publicationDate = one_selector.xpath("./tr[4]/td[1]/text()").extract_first()
        #获取IPC分类号
        patent_ipc = one_selector.xpath("./tr[5]/td[1]/text()").extract_first()
        #获取主分类号
        patent_mainNumber = one_selector.xpath("./tr[6]/td[1]/text()").extract_first()
        #获取申请人
        patent_owner = one_selector.xpath("./tr[7]/td[1]/text()").extract_first()
        #获取发明人
        author = one_selector.xpath("./tr[8]/td[1]/text()").extract_first()
        #获取优先权号
        patent_priorityNumber = one_selector.xpath("./tr[9]/td[1]/text()").extract_first()
        #获取优先权日
        patent_priorityDate = one_selector.xpath("./tr[10]/td[1]/text()").extract_first()
        #获取地区
        address = one_selector.xpath("./tr[11]/td[1]/text()").extract_first()
        #爬取摘要内容
        summary = response.xpath("//div[@class='row']/div[@class='col-md-12 content-cf']/text()").extract_first() 
        #生成Item实例
        item = PatentItem()
        item["_id"] = self.get_patent_url_last12()
        item["title"] = patent_name
        item["author"] = author
        item["achievementtype"] = None
        item["summary"] = summary
        item["mainBody"] = "暂不提供正文"
        item["hyperlink"] = self.get_patent_url()
        item["downloadAddress"] = self.get_patent_url()
        item["undateDate"] = str(time.strftime("%F"))
        item["filingDate"] = filingDate
        item["publicationDate"] = publicationDate
        item["address"] = address
        item["countryCode"] = None
        item["applicationNumber"] = applicationNumber
        item["publicationNumber"] = publicationNumber
        item["patent_ipc"] = patent_ipc
        item["patent_mainNumber"] = patent_mainNumber
        item["patent_owner"] = patent_owner
        item["patent_priorityNumber"] = patent_priorityNumber
        item["patent_priorityDate"] = patent_priorityDate
        #生成下一个Request
        self.patent_move_to_next()
        if self.patent_year < self.max_patent_year:
            if self.patent_test is True:
                #开启了测试模式，爬取次数等于patent_counts
                self.patent_counts = self.patent_counts - 1
                if self.patent_counts >= 0:
                    #生成下一次爬取的Request
                    next_url = self.get_patent_url()
                    yield Request(next_url, callback = self.parse_patent_url)
            else:
                #生成下一次爬取的Request
                next_url = self.get_patent_url()
                yield Request(next_url, callback = self.parse_patent_url)
        #返回Item
        yield item

    #根据详细页面获取参考文献
    def parse_ref_url(self, response):
        #获取参考文献信息
        achi_reference = response.xpath("//div[@id='referenceRelate']//div[@class='relate']//div[@class='article-list']/ul[@class='referenceInfo']/li").xpath("string(.)").extract()
        #获取会议（基金）信息
        conference = response.xpath("//div[@class='article-detail']/div[@class='fund']/span[2]/text()").extract_first()
        #填写参考项和会议项
        item = response.meta["item"]
        item["achi_article_list"] = achi_reference
        item["conference"] = conference
        yield item
        pass

    #搜索解析函数
    def search_parse(self, response):
        #获取专家
        expert_item = response.meta["expertItem"]
        #按照XPATH提取信息
        #当前页面显示的10个结果的偏移地址
        self.Patent_Index = 0
        list_selector = response.xpath("//div[@class='search-result-list']/div[@class='simple-list']/dl")
        for one_selector in list_selector:
            #获取文献标题
            achi_title = one_selector.xpath("./dt[1]/a/text()").extract_first()
            #详细信息页URL
            achi_details_url = one_selector.xpath("./dt[1]/a/@href").extract_first()
            #获取作者
            achi_author = one_selector.xpath("./dd[3]/span[@class='author']/span/a/@title").extract()
            #获取文献对应期刊
            achi_paper = one_selector.xpath("./dd[3]/span[@class='from']/a[1]/text()").extract_first()
            #期刊具体信息
            achi_paper_details = one_selector.xpath("./dd[3]/span[@class='vol']/text()").extract_first()
            #文献摘要
            achi_abstract = one_selector.xpath(".//span[@class='abstract']/span[2]/text()").extract_first()
            #关键字
            achi_subject = one_selector.xpath(".//span[@class='subject']/span/a/@title").extract()
            #生成Item实例
            item = AchievementItem()

            item["title"] = achi_title
            #将作者类型改为JSON类型
            is_first_author = True
            item["author"] = []
            for one_author_name in achi_author:
                if is_first_author is True:
                    if one_author_name == expert_item["name"]:
                        item["author"].append({"author":expert_item["_id"], "authorName":one_author_name, "role":"FIRST_AUTHOR(1)"})
                    else:
                        item["author"].append({"author":None, "authorName":one_author_name, "role":"FIRST_AUTHOR(1)"})
                    is_first_author = False
                else:
                    if one_author_name == expert_item["name"]:
                        item["author"].append({"author":expert_item["_id"], "authorName":one_author_name, "role":"OTHER_AUTHORS(4)"})
                    else:
                        item["author"].append({"author":None, "authorName":one_author_name, "role":"OTHER_AUTHORS(4)"})
            item["achievementType"] = None
            item["summary"] = achi_abstract
            item["mainBody"] = None
            item["hyperlink"] = "http://qikan.cqvip.com" + achi_details_url
            #获取id值，id值和维普特定的论文保持一致
            url_number_list = re.findall(r"\d+", item["hyperlink"])
            if url_number_list is None:
                item["_id"] = None
            else:
                item["_id"] = url_number_list[-1]
            item["downloadAddress"] = "http://qikan.cqvip.com" + achi_details_url
            item["updateTime"] = time.strftime("%F")
            item["periodical"] = achi_paper
            item["conference"] = None
            item["pagination"] = achi_paper_details
            item["achi_subject"] = achi_subject
            #根据hyperLink解析出参考文献和会议
            ref_url = item["hyperlink"]
            yield Request(ref_url, callback = self.parse_ref_url, meta = {"item":item})
            #填写专家剩余的achievement项
            if item["_id"] is not None:
                expert_item["achievement"].append(item["_id"])
        #返回专家item
        yield expert_item
        pass

    #主解析函数
    def parse(self, response):
        #按照XPATH提取信息
        #头像URL地址
        expert_image = self.get_expert_image_url()
        #星级
        #原网页没这个功能就离谱
        #专家姓名
        expert_name = response.xpath("//div[@class='ep-intro-list w860 f_left m-top15']/h2[1]/span[1]/text()").extract_first()
        #专家描述
        expert_description = response.xpath("//div[@class='ep-intro-list w860 f_left m-top15']/h2[1]/span[2]/text()").extract_first()
        #专家所属团队
        expert_team = response.xpath("//div[@class='ep-intro-list w860 f_left m-top15']/dl[1]/dd[1]/span/a/text()").extract_first()
        #专家所在地区
        expert_location = response.xpath("//div[@class='ep-intro-list w860 f_left m-top15']//dd[@id='lab_szdq']/text()").extract_first()
        #专家擅长领域
        expert_expert = response.xpath("//div[@class='ep-intro-list w860 f_left m-top15']/dl[3]/dd[@id='lab_ssly']/text()").extract_first()
        #专家研究方向
        expert_research = response.xpath("//div[@class='ep-intro-list w860 f_left m-top15']//div[@class='clear p-top10']/span/text()").extract()
        #专家基本信息
        expert_intro = response.xpath(".//div[@class='ft16 w95pct m-center intro-con']").xpath("string(.)").extract()
        #生成Item实例
        item = ExpertItem()
        item["_id"] = str(self.expert_uid)
        item["subscriberId"] = None;
        item["email"] = "testEmail@163.com"
        item["name"] = expert_name
        item["photographUrl"] = expert_image 
        item["organization"] = expert_team
        item["researchArea"] = expert_research
        item["personalHomepage"] = None
        item["updateDate"] = str(time.strftime("%F"))
        item["achievement"] = []      #交给search_parse进行填写
        item["feedbackInformationId"] = None    #后端生成
        item["expert_description"] = expert_description  
        item["expert_location"] = expert_location
        item["expert_expert"] = expert_expert  
        item["expert_intro"] = expert_intro
        
        self.expert_uid += 1
        if self.expert_uid <= self.expert_max_uid:
            #生成下一个Request
            yield Request(self.get_expert_url(), callback = self.parse)
            #如果专家名不为null，则产生一次检索爬取
        if not item["name"] is None:
            #产生一次检索型爬取,爬取成果
            search_url = "http://qikan.cqvip.com/Qikan/Search/Index?key=A%3d%{0}".format(item["name"])
            yield Request(search_url, meta = {"expertItem":item},callback = self.search_parse)
            #12/30改，将专家Item和自己的成就联系到一起
            #yield item
    


        

        