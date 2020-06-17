from scrapy import cmdline

print('[价格演变(非A价)]正在抓取')
cmdline.execute('scrapy crawl LatestBNK -o ./cache_LatestBNK/Latest.csv'.split())
print('[价格演变(非A价)]抓取完毕')