# -*- coding: utf-8 -*-

# Scrapy settings for sinanews project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'sinanews'

SPIDER_MODULES = ['sinanews.spiders']
NEWSPIDER_MODULE = 'sinanews.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sinanews (+http://www.yourdomain.com)'
ITEM_PIPELINES=['sinanews.pipelines.SinanewsPipeline']



