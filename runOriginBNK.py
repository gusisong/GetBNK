from scrapy import cmdline

print('[费用查询]正在抓取')
cmdline.execute('scrapy crawl OriginBNK -o ./cache_OriginBNK/Origin.csv'.split())
print('[费用查询]抓取完毕')