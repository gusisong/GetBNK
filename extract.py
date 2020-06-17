# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2020/3/31 20:43
# @Author: Gu Sisong
import pandas as pd
import time
import pandas.io.formats.excel


def Pivot():
    dfOrigin = pd.read_csv('./cache_OriginBNK/Origin.csv', encoding='GB2312')
    dfOriginPivot = dfOrigin.pivot_table(index=['零件号', '供应商SAP号', '采购工厂', '单位'], values='价格', columns=['价格类型'])
    dfOriginPivot.rename(columns={'包装费': '包装费(原始)', '操作费': '操作费(原始)', '运输费': '运输费(原始)'}, inplace=True)
    dfOriginPivot.to_csv('./cache_OriginBNK/OriginPivot.csv', encoding='GB2312')
    dfOriginPivot = pd.read_csv('./cache_OriginBNK/OriginPivot.csv', encoding='GB2312')
    # print([column for column in dfOriginPivot])

    dfLatest = pd.read_csv('./cache_LatestBNK/Latest.csv', encoding='GB2312')
    # 拆为2个DataFrame分别做透视
    newDfLatest1 = pd.DataFrame(dfLatest, columns=['零件号', '供应商SAP号', '采购工厂', '价格类型', '价格'])
    dfLatestPivot1 = newDfLatest1.pivot_table(index=['零件号', '供应商SAP号', '采购工厂'], values='价格', columns='价格类型')
    dfLatestPivot1.rename(columns={'包装费': '包装费(最新)', '操作费': '操作费(最新)', '运输费': '运输费(最新)'}, inplace=True)
    dfLatestPivot1.to_csv('./cache_LatestBNK/LatestPivot1.csv', encoding='GB2312')
    dfLatestPivot1 = pd.read_csv('./cache_LatestBNK/LatestPivot1.csv', encoding='GB2312')
    # print([column for column in dfLatestPivot1])

    newDfLatest2 = pd.DataFrame(dfLatest, columns=['零件号', '供应商SAP号', '采购工厂', '价格类型', '服务商SAP号'])
    dfLatestPivot2 = newDfLatest2.pivot_table(index=['零件号', '供应商SAP号', '采购工厂'], values='服务商SAP号', columns='价格类型')
    dfLatestPivot2.rename(columns={'包装费': '包装费(服务商)', '操作费': '操作费(服务商)', '运输费': '运输费(服务商)'}, inplace=True)
    dfLatestPivot2.to_csv('./cache_LatestBNK/LatestPivot2.csv', encoding='GB2312')
    dfLatestPivot2 = pd.read_csv('./cache_LatestBNK/LatestPivot2.csv', encoding='GB2312')
    # print([column for column in dfLatestPivot2])

    dfLatestPivot = pd.merge(dfLatestPivot1, dfLatestPivot2, how='left')
    # dfLatestPivot.to_csv('./cache_LatestBNK/LatestPivot.csv', encoding='GB2312')

    dfPivot = pd.merge(dfOriginPivot, dfLatestPivot, how='outer')
    dfPivot.rename(columns={'零件号': '无色标零件号', '供应商SAP号': '供应商号', '采购工厂': '工厂'}, inplace=True)
    # dfPivot.to_csv('./cache_LatestBNK/Pivot.csv', encoding='GB2312')

    basic_info = pd.read_excel('BNK费用查询模板(请勿修改文件名和表头).xlsx')
    basic_info.to_csv('./cache_LatestBNK/basic_info.csv', encoding='GB2312')
    basic_info = pd.read_csv('./cache_LatestBNK/basic_info.csv', encoding='GB2312')
    dfPivotFinal = pd.merge(basic_info, dfPivot, how='left')
    dfPivotFinal = dfPivotFinal[
        ['零件号', '无色标零件号', '供应商号', '工厂', 'SUPPLIER_ID', '单位', '运输费(原始)', '操作费(原始)', '包装费(原始)', '运输费(最新)', '运输费(服务商)',
         '操作费(最新)', '操作费(服务商)', '包装费(最新)', '包装费(服务商)']]

    # 清除默认Excel表头格式
    # pandas.io.formats.excel.header_style = None

    dfPivotFinal.to_csv(
        './BNK查询结果/BNK查询结果_{0}.csv'.format(time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))),
        encoding='GB2312',
        index=None)


def main():
    print('正在整合数据')
    Pivot()
    print('查询结果已导出')


if __name__ == '__main__':
    main()
