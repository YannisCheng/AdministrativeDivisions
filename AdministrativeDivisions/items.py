# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

"""
区域代码含义：

37  07  84  118   224
省  市   区   镇   街道
"""

"""
注意：此处的 items.py 文件未使用，而是直接在NOSSpider中拼接的sql语句。
"""

# 一级
class ProvinceItem(scrapy.Item):
    # 省级名称
    province_name = scrapy.Field()
    province_href = scrapy.Field()
    # 省级区域代码 - 完整
    province_code = scrapy.Field()
    # 省级区域代码 - 2位 简化
    simple_province_code = scrapy.Field()
    pass


# 二级
class CityItem(scrapy.Item):
    # 地级市名称
    city_name = scrapy.Field()
    # 地级市区域代码 - 完整
    city_code = scrapy.Field()
    # 地级市区域代码 - 2位 简化
    simple_city_code = scrapy.Field()
    pass


# 三级
class CountyItem(scrapy.Item):
    # 区县名称
    county_name = scrapy.Field()
    county_href = scrapy.Field()
    # 区县区域代码 - 完整
    county_code = scrapy.Field()
    # 区县区域代码 - 2位 简化
    simple_county_code = scrapy.Field()
    pass


# 四级
class TownItem(scrapy.Item):
    # 镇名称
    town_name = scrapy.Field()
    town_href = scrapy.Field()
    # 镇区域代码 - 完整
    town_code = scrapy.Field()
    # 镇区域代码 - 3位 简化
    simple_town_code = scrapy.Field()
    pass


# 五级
class VillageItem(scrapy.Item):
    # 居委会名称
    village_name = scrapy.Field()
    village_href = scrapy.Field()
    # 居委会区域代码 - 完整
    village_code = scrapy.Field()
    # 居委会区域代码 - 3位 简化
    simple_village_code = scrapy.Field()
    # 城乡分类代码 - 3位
    village_category_code = scrapy.Field()
    pass
