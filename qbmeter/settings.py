# -*- coding: utf-8 -*-

# Scrapy settings for qbmeter project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'qbmeter'

SPIDER_MODULES = ['qbmeter.spiders']
NEWSPIDER_MODULE = 'qbmeter.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'qbmeter-bot (+orangain@gmail.com)'

DOWNLOAD_DELAY = 2.0
RANDOMIZE_DOWNLOAD_DELAY = False
