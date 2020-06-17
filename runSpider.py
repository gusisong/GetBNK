import os

print('run OriginBNK spider')
os.system('scrapy crawl OriginBNK -o ./cache/Origin.csv')
print('run LatestBNK spider')
os.system('scrapy crawl LatestBNK -o ./cache/Latest.csv')
