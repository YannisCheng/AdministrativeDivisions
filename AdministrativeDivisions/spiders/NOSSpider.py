# -*- coding: UTF-8 -*-
# 要在代码中使用"中文"注释，应该首先添加如上注释，说明是中文注释
import json
from scrapy import Spider, Selector
from scrapy.http.request import Request

from AdministrativeDivisions.pipelines import AdministrativeDivisionsPipeline
from AdministrativeDivisions.settings import TABLE_PROVINCE, TABLE_CITY, TABLE_COUNTY, TABLE_TOWN, TABLE_VILLAGE

"""错误提示："""
# 1. 2019-01-30 23:48:22  从本项目的一个文件中导入此文件中的某一个类时，需要导入一个完整的路劲。否则提示：ImportError: No module named items
#
# 2. 2019-01-30 23:50:11  在 settings文件中编写路径类时，同样需要编写带有路径的文件类，否则不认，同上错误
# from Northern_Open_Space.items import ProvinceItem, CityItem
#
# 3. 当连接MySQL数据库提示：
#        pymysql.err.OperationalError: (1045, u"Access denied for user 'root'@'localhost' (using password: No)")
#    时，啥也别说了：通过以下命令改密码!!!
#        ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'yourpassword';
#

"""
从"国家统计局"官网爬取行政区域数据，url: http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/
采集数据后的结果确认url：http://data.stats.gov.cn/easyquery.htm?cn=C01
"""


class NOSSpider(Spider):
    # 基础配置 - 唯一名称
    name = "NOS"

    # 待爬取的年份
    yearTarget = "2020"

    # 基础配置 - 允许访问的域名
    allowed_domains = ["www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm"]

    # 基础配置 - 开发爬取的地址
    start_urls = ["http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/" + yearTarget + "/index.html"]

    """第一级：省级、直辖市 数据爬取"""

    def parse(self, response, m_year_target=yearTarget):
        sel = Selector(response)
        node = sel.xpath('//tr[@class="provincetr"]/td/a/text()')
        node_href = sel.xpath('//tr[@class="provincetr"]/td/a/@href')

        for item_node, item_node2 in zip(node, node_href):
            # 名称 ："山东省"
            province_name = json.dumps(item_node.extract(), ensure_ascii=False)
            # 名称 ："37.html"
            province_href = json.dumps(item_node2.extract(), ensure_ascii=False)
            # 名称 ："37"
            province_code = province_href[1:3]

            # ---- log ----
            print("省级：" + province_name + ',' + province_code + ',' + province_href)

            self.insertIntoProvince(province_code, province_name)
            cl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/" + m_year_target + "/" + province_href[1:8]
            yield Request(url=cl, callback=self.parse_second, dont_filter=True)

    def insertIntoProvince(self, province_code, province_name):
        # 将获取的数据插入到数据库中
        db = AdministrativeDivisionsPipeline()
        sql = "insert into " + TABLE_PROVINCE + " (" + 'province_name,' + 'province_code,' + 'simple_province_code,' + 'grade' + ") VALUE (" + province_name + "," + province_code + '0000000000' + "," + province_code + "," + "1" + ")"
        db.insertIntoTable(sql=sql)

    """第二级：地级市 数据爬取"""

    def parse_second(self, response, m_year_target=yearTarget):
        second = Selector(response)
        node_city = second.xpath('//tr[@class="citytr"]/td/a/text()')

        # ---- log ----
        print("市级：")
        print(len(node_city))
        print("市级：" + json.dumps(node_city.extract(), ensure_ascii=False))

        node_city_href = second.xpath('//tr[@class="citytr"]/td/a/@href')

        self.insertToCity(node_city)

        # 城市href list
        city_href = []

        for href_item in node_city_href:
            city_href_item = json.dumps(href_item.extract(), ensure_ascii=False)
            # 将单个 "城市href" 添加至 "list中"
            city_href.append(city_href_item)
        # 做 "list去重"
        city_href = list(set(city_href))

        for item in city_href:
            cl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/" + m_year_target + "/" + item[1:13]
            # 第三级url拼接
            yield Request(url=cl, callback=self.parse_thread, dont_filter=True)

    def insertToCity(self, node_city):
        # 循环赋值
        n = len(node_city)
        m = 0
        while m < n:
            code = json.dumps((node_city[m:m + 1]).extract(), ensure_ascii=False)
            name = json.dumps((node_city[m + 1:m + 2]).extract(), ensure_ascii=False)

            # ---- log ----
            print("市级：" + code[1:len(code) - 1])
            print("市级：" + name[1:len(name) - 1])

            db = AdministrativeDivisionsPipeline()
            sql = "insert into " + TABLE_CITY + " (" + 'city_code,' + 'city_name,' + 'simple_city_code,' + 'grade' + ") VALUE (" + code[
                                                                                                                                   1:len(
                                                                                                                                       code) - 1] + "," + name[
                                                                                                                                                          1:len(
                                                                                                                                                              name) - 1] + "," + (
                                                                                                                                                                                     code[
                                                                                                                                                                                     1:len(
                                                                                                                                                                                         code) - 1])[
                                                                                                                                                                                 1:5] + "," + "2" + ")"
            db.insertIntoTable(sql=sql)
            m = m + 2

    """第三级：区县乡级 数据爬取"""

    def parse_thread(self, response, m_year_target=yearTarget):
        thread = Selector(response)
        node_county = thread.xpath('//tr[@class="countytr"]/td/a/text()')
        node_county_href = thread.xpath('//tr[@class="countytr"]/td/a/@href')

        self.insertIntoCounty(node_county)  # 县区级 代码list
        county_codes = []

        # 县区级 名称list
        county_name = []

        # 县区级 href list
        county_href = []

        for item, href_item in zip(node_county, node_county_href):
            county = json.dumps(item.extract(), ensure_ascii=False)
            # 检测当前字符串是否全部为 数字 ？
            if county[1:13].isdigit():
                # 将字符串数据存至list类型数据中
                county_codes.append(county)
                # print("代码：")
            else:
                county_name.append(county)
                # print("名称：")

            county_href_item = json.dumps(href_item.extract(), ensure_ascii=False)
            # 将单个 "县区级 href" 添加至 "list中"
            county_href.append(county_href_item)

        # 做 "list去重"
        county_href = list(set(county_href))
        county_codes = list(set(county_codes))
        county_name = list(set(county_name))

        for href, codes in zip(county_href, county_codes):
            cl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/" + m_year_target + "/" + codes[1:3] + "/" + href[
                                                                                                                1:15]
            # http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/21/13/211321.html
            # 第四级url拼接
            yield Request(url=cl, callback=self.parse_fourth, dont_filter=True)

    def insertIntoCounty(self, node_county):
        n = len(node_county)
        m = 0
        while m < n:
            code = json.dumps((node_county[m:m + 1]).extract(), ensure_ascii=False)
            name = json.dumps((node_county[m + 1:m + 2]).extract(), ensure_ascii=False)

            # ---- log ----
            print("区级：" + code[1:len(code) - 1])
            print("区级：" + name[1:len(name) - 1])

            db = AdministrativeDivisionsPipeline()
            sql = "insert into " + TABLE_COUNTY + " (" + 'county_code,' + 'county_name,' + 'simple_county_code,' + 'grade' + ") VALUE (" + code[
                                                                                                                                           1:len(
                                                                                                                                               code) - 1] + "," + name[
                                                                                                                                                                  1:len(
                                                                                                                                                                      name) - 1] + "," + (
                                                                                                                                                                                             code[
                                                                                                                                                                                             1:len(
                                                                                                                                                                                                 code) - 1])[
                                                                                                                                                                                         1:7] + "," + "3" + ")"
            db.insertIntoTable(sql=sql)
            m = m + 2

    """第四级：街道、居委会级 数据爬取"""

    def parse_fourth(self, response, m_year_target=yearTarget):
        thread = Selector(response)
        node_towntr = thread.xpath('//tr[@class="towntr"]/td/a/text()')
        node_towntr_href = thread.xpath('//tr[@class="towntr"]/td/a/@href')

        # ---- log ----
        print("街道：" + json.dumps(node_towntr.extract(), ensure_ascii=False))

        self.insertIntoTown(node_towntr)  # 街道办 代码list
        town_codes = []

        # 街道办 名称list
        town_name = []

        # 街道办 href list
        town_href = []

        for item, href_item in zip(node_towntr, node_towntr_href):
            town = json.dumps(item.extract(), ensure_ascii=False)
            # 检测当前字符串是否全部为 数字 ？
            if town[1:13].isdigit():
                town_codes.append(town)
                # print("代码：")
            else:
                town_name.append(town)
                # print("名称：")

            towntr_href_item = json.dumps(href_item.extract(), ensure_ascii=False)
            # 将单个 "街道办 href" 添加至 "list中"
            town_href.append(towntr_href_item)

        # 做 "list去重"
        town_href = list(set(town_href))
        town_codes = list(set(town_codes))
        town_name = list(set(town_name))

        for href, code in zip(town_href, town_codes):
            cl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/" + m_year_target + "/" + code[1:3] + "/" + code[
                                                                                                               3:5] + "/" + href[
                                                                                                                            1:18]
            # http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/21/13/21/211321001.html
            # code : 211321001000
            # href : 21/211321001.html
            # 第五级url拼接
            yield Request(url=cl, callback=self.parse_Five, dont_filter=True)

    def insertIntoTown(self, node_towntr):
        n = len(node_towntr)
        m = 0
        while m < n:
            code = json.dumps((node_towntr[m:m + 1]).extract(), ensure_ascii=False)
            name = json.dumps((node_towntr[m + 1:m + 2]).extract(), ensure_ascii=False)

            # ---- log ----
            print("街道：" + code[1:len(code) - 1])
            print("街道：" + name[1:len(name) - 1])

            db = AdministrativeDivisionsPipeline()
            sql = "insert into " + TABLE_TOWN + " (" + 'town_code,' + 'town_name,' + 'simple_town_code,' + 'grade' + ") VALUE (" + code[
                                                                                                                                   1:len(
                                                                                                                                       code) - 1] + "," + name[
                                                                                                                                                          1:len(
                                                                                                                                                              name) - 1] + "," + (
                                                                                                                                                                                     code[
                                                                                                                                                                                     1:len(
                                                                                                                                                                                         code) - 1])[
                                                                                                                                                                                 7:10] + "," + "4" + ")"
            db.insertIntoTable(sql=sql)

            m = m + 2

    """第五级：社区级 数据爬取"""

    def parse_Five(self, response):
        thread = Selector(response)
        node_village = thread.xpath('//tr[@class="villagetr"]/td/text()')

        # ---- log ----
        print("社区：" + json.dumps(node_village.extract(), ensure_ascii=False))

        n = len(node_village)
        m = 0
        while m < n:
            code = json.dumps((node_village[m:m + 1]).extract(), ensure_ascii=False)
            simple_code = json.dumps((node_village[m + 1:m + 2]).extract(), ensure_ascii=False)
            name = json.dumps((node_village[m + 2:m + 3]).extract(), ensure_ascii=False)

            # ---- log ----
            print("社区：" + code[1:len(code) - 1])
            print("社区：" + simple_code[1:len(simple_code) - 1])
            print("社区：" + name[1:len(name) - 1])
            print("社区：" + (code[11:14]))

            db = AdministrativeDivisionsPipeline()
            sql = "insert into " + TABLE_VILLAGE + " (" + \
                  'village_code,' + 'village_name,' + 'simple_village_code,' + 'village_category_code,' + 'grade' + ") VALUE (" + \
                  code[1:len(code) - 1] + "," + name[1:len(name) - 1] + "," + code[11:14] + "," + simple_code[1:len(
                simple_code) - 1] + "," + "5" + ")"
            db.insertIntoTable(sql=sql)

            m = m + 3
