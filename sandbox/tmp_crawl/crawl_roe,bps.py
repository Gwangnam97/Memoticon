from urllib import parse
import pandas as pd
import numpy as np
"""
ROE, BPS(원) 구하기
"""


target_list = ['ROE', 'BPS(원)']
list_bps = []
list_roe = []
df_result = pd.DataFrame()
df = pd.read_csv(
    '_with_stock_finance_as_select_s_stk_cd_s_stk_nm_sum_case_when_f__202302081934.csv',  low_memory=False)
df['stk_cd'] = df['stk_cd'].apply(lambda x: '{0:0>6}'.format(x))


def get_fnguide(code):
    get_param = {
        'pGB': 1,
        'gicode': 'A%s' % (code),
        'cID': '',
        'MenuYn': 'Y',
        'ReportGB': '',
        'NewMenuID': 101,
        'stkGb': 701,
    }
    get_param = parse.urlencode(get_param)
    url = "http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?%s" % (get_param)
    print(url)
    tables = pd.read_html(url, header=0)
    return (tables)


def fuxkin_stock(code, target):

    # 테이블 다른 종목 필터링
    if code == '088260':
        df = get_fnguide('088260')[11]
    elif code == '145270':
        df = get_fnguide('145270')[12]
    elif code == '155900':
        df = get_fnguide('155900')[13]
    else:
        df = get_fnguide(code)[10]
    df = df.set_index(list(df)[0])
    df = df.rename(columns=df.iloc[0]).drop(df.index[0])
    tmp = pd.DataFrame([[code]], index=['stk_cd'])
    df2 = pd.concat([df.loc[target], tmp]).rename({0: target}, axis=1)
    return df2.reset_index().T


# int_i = 0
# for i in df['stk_cd']:
#     print(i, '\t', int_i)
#     int_i += 1

#     target_data = fuxkin_stock(str(i), target_list[1])
#     print(target_data)
#     print()

#     df_result = pd.concat([df_result, target_data], axis=0, ignore_index=True)
#     df_result.reset_index(inplace=True, drop=True)

# print(df_result)
# df_result.to_csv(f'./df_crawl_{target_list[1]}_rawdata.csv')
