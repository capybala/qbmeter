# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division, print_function

import re
import urllib
from datetime import datetime

import scrapy

from ..items import Store, Availability

PAGE_RE = re.compile(r'pid=(\d+)')


class QbSpider(scrapy.Spider):
    name = "qb"
    allowed_domains = ["www.qbhouse.co.jp"]
    start_urls = (
        'http://www.qbhouse.co.jp/search/',
    )

    def parse(self, response):
        prefs = response.css('#map a > p::text').extract()

        def add_suffix(pref):
            if pref == '北海道':
                return pref
            elif pref == '東京':
                return pref + '都'
            elif pref in ('京都', '大阪'):
                return pref + '府'
            else:
                return pref + '県'

        keywords = [add_suffix(pref) for pref in prefs]
        scrapy.log.msg(' '.join(keywords))

        for keyword in keywords:
            url = 'http://www.qbhouse.co.jp/search/list.php' + \
                '?parking_cd_k=1&keywords5={0}&method=kwd'.format(
                    urllib.quote_plus(keyword.encode('utf-8')))
            yield scrapy.Request(url, callback=self.parse_list)

    def parse_list(self, response):

        def parse_locations(response):
            script_text = response.css('#main_map script::text')
            latitudes = script_text.re(r'{lat:(.+?),')
            longitudes = script_text.re(r'lng:(.+?)}')
            store_ids = script_text.re(r'detail.php\?id=(\d+)')
            assert len(latitudes) == len(longitudes) == len(store_ids)
            locations = {}
            for latitude, longitude, store_id in zip(latitudes, longitudes, store_ids):
                locations[store_id] = (latitude, longitude)
            return locations

        locations = parse_locations(response)
        now = datetime.now()

        def parse_store(tr):
            store = Store()
            store['id'] = tr.css('::attr(id)').re(r'tr(\d+)')[0]
            store['url'] = 'http://www.qbhouse.co.jp/search/detail.php?id={0}'.format(store['id'])
            store['name'] = tr.css('td.name a::text').extract()[0]
            store['latitude'], store['longitude'] = locations[store['id']]
            store['timestamp'] = now

            item = Availability()
            item['html'] = tr.extract()
            item['store_id'] = tr.css('::attr(id)').re(r'tr(\d+)')[0]
            item['signal'] = tr.css('img.store-light::attr(src)').re(r'light-(\w+)')[0]
            item['num_waiting'], item['num_available'] = \
                tr.css('p.store-avail::text').re(r'待ち人数：(.*?)名  /  稼働席数：(.*?)席')
            item['timestamp'] = now

            return store, item

        for tr in response.css('.shoplist tr[id^="tr"]'):
            store, availability = parse_store(tr)
            yield store
            yield availability

        if len(response.css('a > img[alt="NEXT"]')) == 0:
            return

        def next_page(url):
            m = PAGE_RE.search(url)
            if m is None:
                return url + '&pid=2'

            return PAGE_RE.sub('pid={0}'.format(int(m.group(1)) + 1), url)

        next_url = next_page(response.url)
        yield scrapy.Request(next_url, callback=self.parse_list)
