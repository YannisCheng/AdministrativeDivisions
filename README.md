# 说明

2021-05-12 11:27:35

- [scrapy官方文档](https://scrapy-chs.readthedocs.io/zh_CN/1.0/intro/tutorial.html)


- Scrapy的架构

![Scrapy的架构](img/scrapy_architecture.png)



## 本项目功能
从 `国际统计局` 官网获取 `全国5级行政区划数据`。

- [基础地址](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/)

- [数据库数据量准确性确认地址](http://data.stats.gov.cn/easyquery.htm?cn=C01)


## 数据采集
### 被采集网站层级：
```
http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/
统计用区划和城乡划分代码
|
|____http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html
|____2020（被采集年份）
     |
     |____http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/37.html
     |____山东省（1级）
           |
           |____http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/37/3701.html
           |____济南市（2级）
                |
                |____http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/37/01/370102.html
                |____历下区（3级）
                     |
                     |____http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/37/01/02/370102001.html
                     |____解放路街道（4级）
                          |
                          |____370102001002 111 解放桥社区居委会（5级）
```

### 采集层级与对应数据表及其字段:

```
省（1级）
id|province_name|province_code|grade|
-------------------------------------
15|山东省        |37           |    1|


市（2级）
id |city_name   |city_code|province_code|grade|
-----------------------------------------------
114|济南市       |3701     |37           |    2|


区（3级）
id  |county_name|county_code |city_code|province_code|grade|
------------------------------------------------------------
2669|历下区      |370102      |3701     |37           |    3|


街道（4级）
id   |town_name|town_code|county_code |city_code|province_code|grade|
---------------------------------------------------------------------
33375|解放路街道 |370102001|370102      |3701     |37           |    4|

社区（5级）
id    |village_name |village_code|town_code|county_code |city_code|province_code|grade|
---------------------------------------------------------------------------------------
463812|解放桥社区居委会|370102001002|370102001|370102      |3701     |37           |    5|
```

## 环境配置

[Python及Scrapy安装](https://scrapy-chs.readthedocs.io/zh_CN/1.0/intro/install.html)

*注意：*
1. 当使用自己下载的 `Python3` 安装其 `Scrapy` 、`pymysql` 组件时，应使用 `pip3` 工具。
2. 自己安装的新版 `Python3` 安装路径为为：`/usr/local/Cellar/pythonXXX`
3. macOS自带 `Python` 路径为 `/usr/bin/python`

## 本项目要求
1. Python3 
2. Scrapy
3. pymysql

## 项目中实际使用到的文件

主爬取文件为 `NOSSpider.py` ;
配置文件为 `setting.py`;
mysql配置文件为：`pipelines.py`

## 项目运行
在 `AdministrativeDivisions/AdministrativeDivisions/`目录下运行：`scrapy crawl NOS`.
运行时间不等，最长的一次为2h。

## 日志输出配置
在 `settings.py`文件中配置了将 "控制台日志输出至指定文件中"。
