from urllib import parse
import pandas as pd
import numpy as np

target_list = ['PCR']
list_bps = []
list_roe = []
df_result = pd.DataFrame()
df = pd.read_csv('_with_stock_finance_as_select_s_stk_cd_s_stk_nm_sum_case_when_f__202302081934.csv',
                 header=None, low_memory=False)
df[0] = df[0].apply(lambda x: '{0:0>6}'.format(x))

def scrap():
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
        url = "http://comp.fnguide.com/SVO2/ASP/SVD_Invest.asp?%s" % (
            get_param)
        print(url)
        tables = pd.read_html(url, header=0)
        return (tables)

    code = df[0].values
    df2 = pd.DataFrame()

    for x in code:
        a = get_fnguide(x)

        df = pd.DataFrame(a[3])

        new_list = list()
        for i in df[df.columns[0]].values:
            # print(i.split('계산')[0].split('(')[0].strip())
            new_list.append(i.split('계산')[0].split('(')[0].strip())
        df[df.columns[0]] = new_list

        try:
            a = df[df[df.columns[0]] == target_list[0]].index[0]
            print(df[df[df.columns[0]] == target_list[0]].rename(index={a: x}))
            df2 = pd.concat(
                [df2, df[df[df.columns[0]] == target_list[0]].rename(index={a: x})])
        except:
            # concat empty df
            print(f'Error : {x}')
    return df2


df = pd.read_csv('pcr_rawdata.csv', low_memory=False,index_col=[0])
a = df[df['2019/03'].notnull()].dropna(axis=1).drop('IFRS 연결',axis=1)
a = a.rename(columns={'2019/03' : 2019})
b = df[['2019/12']].rename(columns={'2019/12' : 2019})
b = b.drop(index='stk_cd')
c = pd.concat([a,b])
c = c.rename(columns={2019: '2019_PCR'})

c.to_csv('./pcr_data.csv',encoding='UTF-8')
print(c)
