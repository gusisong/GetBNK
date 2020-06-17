# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import pandas as pd

type_list = ['102', '103', '104']
basic_info = pd.read_excel('BNK费用查询模板(请勿修改文件名和表头).xlsx')


class LatestBNKSpider(scrapy.Spider):
    name = 'LatestBNK'
    allowed_domains = ['svw.csvw.com']
    start_urls = ['http://svw.csvw.com/empnew/wps/myportal/']

    # 用户登录
    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                "username": "65078",
                "password": "Holyshit2@",
                "login-form-type": "pwd"
            },
            callback=self.parse_page
        )

    # 获取登录成功状态，访问需要登录后才能访问的页面
    def parse_page(self, response):
        for i in range(0, len(basic_info)):
            for CostType in type_list:
                url = (
                    'http://svw.csvw.com/sol-bnk/pages/bnk/csc/priceNotAView.jsf?partNum={0}&priceType={1}&supplierSapCode={2}&supplierId={3}&partType=P&procureFactory={4}'.format(
                        basic_info.iloc[i]['无色标零件号'], CostType, str(basic_info.iloc[i]['供应商号']),
                        str(basic_info.iloc[i]['SUPPLIER_ID']), str(basic_info.iloc[i]['工厂'])))
                yield Request(url, callback=self.parse_newpage)

    # 处理响应内容
    def parse_newpage(self, response):
        PartNum = response.xpath('/html/body/table//tr/td/form/table//tr[1]/td/table//tr/td[2]/text()').get()
        SupSapNum = response.xpath('/html/body/table//tr/td/form/table//tr[1]/td/table//tr/td[3]/text()').get()
        Plant = response.xpath('/html/body/table//tr/td/form/table//tr[1]/td/table//tr/td[4]/text()').get()
        CostType = response.xpath('/html/body/table//tr/td/form/table//tr[1]/td/table//tr/td[5]/text()').get()

        if response.xpath('//td[@class="rich-table-cell "]/text()').getall() == []:
            LspSapNum = None
        else:
            LspSapNum = response.xpath('//td[@class="rich-table-cell "]/text()').getall()[-2]

        if response.xpath('//td[@class="rich-table-cell "]/text()').getall() == []:
            Price = None
        else:
            Price = response.xpath('//td[@class="rich-table-cell "]/text()').getall()[-1]

        item = {
            "零件号": PartNum,
            "供应商SAP号": SupSapNum,
            "采购工厂": Plant,
            "价格类型": CostType,
            "服务商SAP号": LspSapNum,
            "价格": Price,
        }
        yield item
