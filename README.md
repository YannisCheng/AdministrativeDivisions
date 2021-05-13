# 说明

2021-05-12 11:27:35

- [scrapy官方文档](https://scrapy-chs.readthedocs.io/zh_CN/1.0/intro/tutorial.html)



## 本项目功能
从 `国际统计局` 官网获取 `全国5级行政区划数据`。

- [基础地址](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/)

- [数据库数据量准确性确认地址](http://data.stats.gov.cn/easyquery.htm?cn=C01)



## 数据采集层级：
```
http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/
统计用区划和城乡划分代码
|____http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html
|____2020（年）
     |____http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/37.html
     |____山东省（1级）
           |____http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/37/3701.html
           |____济南市（2级）
                |____http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/37/01/370102.html
                |____历下区（3级）
                     |____http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/37/01/02/370102001.html
                     |____解放路街道（4级）
                          |____370102001002 111 解放桥社区居委会（5级）
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
