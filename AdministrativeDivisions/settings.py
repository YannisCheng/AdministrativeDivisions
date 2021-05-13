# -*- coding: utf-8 -*-

# Scrapy settings for Northern_Open_Space project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import datetime

BOT_NAME = 'AdministrativeDivisions'

SPIDER_MODULES = ['AdministrativeDivisions.spiders']
NEWSPIDER_MODULE = 'AdministrativeDivisions.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Northern_Open_Space (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }
# 设置请求头部，添加url
# 指定用户终端，否则有些网站会禁止访问，显示403
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'Northern_Open_Space.middlewares.NorthernOpenSpaceSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'Northern_Open_Space.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'AdministrativeDivisions.pipelines.AdministrativeDivisionsPipeline': 300,  # 保存到mysql数据库
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
FEED_EXPORT_ENCODING = 'utf-8'

# Mysql数据库的配置信息 --------------------
MYSQL_HOST = 'localhost'
MYSQL_DB_NAME = 'area_database'  # 数据库名字，请修改
MYSQL_USER = 'root'  # 数据库账号，请修改
MYSQL_PASSWORD = 'Admin_1126'  # 数据库密码，请修改
MYSQL_PORT = 3306  # 数据库端口
ENCODE = 'utf8'

# area_database中的table名 --------------
TABLE_PROVINCE = 'province_table'
TABLE_CITY = 'city_table'
TABLE_COUNTY = 'county_table'
TABLE_TOWN = 'town_table'
TABLE_VILLAGE = 'village_table'

# 仅做测试使用 ---------------------------
TABLE_PROVINCE2 = 'province_table2'

# 控制台日志输出到文件 --------------------
# 或者直接在控制台中使用：
# scrpay crawl spider_name  -s LOG_FILE=all.log
#LOG_FILE = 'log/scrapy_{}.log'.format(datetime.datetime.now())
#LOG_LEVEL = 'DEBUG'

# spider配置 ---------------------------
# 基础配置 - 唯一名称
SPIDER_NAME = "NOS"
# 待爬取的年份
SPIDER_TARGET_YEAR = "2020"
# 基础配置 - 允许访问的域名
SPIDER_DOMAINS = ["www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm"]
# 基础配置 - 开发爬取的地址
SPIDER_START_URLS = ["http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/" + SPIDER_TARGET_YEAR + "/index.html"]
