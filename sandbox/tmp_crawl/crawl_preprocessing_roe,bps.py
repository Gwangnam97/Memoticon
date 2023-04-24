import pandas as pd
import numpy as np

"""['2019/12' '1.41' '23.52' '5.41' '6.82' '6.50' '7.03' '1.25' '1.34' '1.31'
 '4.68' '6.30' '17.40' '32.69' '2.25' '10.03' '11.21' '2.54' '4.75' '6.93'
 '14.22' '7.94' '10.78' '32.82' '6.27' '9.58' '32.25' '5.83' '3.20' '4.55'
 '8.04' '0.86' '14.05' '23.15' '17.84' '11.95' '30.57' '0.81' '14.24'
 '5.29' '5.55' '2.98' '1.28' '7.36' '2018/12' '5.62' '17.78' '4.32'
 '50.19' '5.96' '0.92' '3.33' '7.25' '15.29' '8.01' '19.66' '4.62' '6.22'
 '11.50' '14.69' '7.75' '5.20' '4.79' '25.13' '11.14' '5.37' '4.73' '3.75'
 '11.44' '5.57' '14.90' '9.59' '2.80' '13.50' '9.60' '5.35' '11.65' '4.39'
 '21.11' '7.20' '1.77' '7.28' '5.45' '18.78' '6.57' '11.57' '11.32' '3.81'
 '9.62' '1.22' '7.29' '20.88' '9.87' '0.85' '3.61' '7.58' '8.53' '0.15'
 '10.23' '5.74' '11.76' '14.98' '2.57' '33.47' '8.52' '11.13' '1.75'
 '14.28' '14.61' '0.89' '7.57' '7.69' '3.32' '12.70' '2022/03' nan '27.49'
 '19.30' '8.87' '12.71' '16.62' '12.98' '13.08' '6.66' '17.15' '22.72'
 '17.12' '12.32' '5.13' '20.96' '4.90' '9.16' '21.61' '18.62' '21.91'
 '25.42' '29.57' '8.78' '7.34' '15.06' '16.91' '7.01' '7.12' '15.67'
 '23.82' '8.59' '14.59' '16.97' '15.10' '12.20' '15.47' '15.86' '12.68'
 '9.72' '11.37' '14.49' '29.85' '8.79' '9.79' '20.57' '4.52' '26.19'
 '17.88' '15.84' '8.50' '12.79' '10.00' '2.59' '20.32' '9.68' '5.49'
 '19.94' '20.64' '4.57' '18.91' '21.89' '8.58' '20.20' '24.47' '4.49'
 '18.76' '6.37' '22.33' '13.49' '14.66' '26.20' '11.48' '12.26' '19.70'
 '4.34' '8.95' '2.08' '8.97' '12.94' '9.17' '17.76' '3.53' '1.51' '5.67'
 '15.73' '12.15' '8.30' '15.34' '19.83' '8.15' '26.85' '13.10' '11.25'
 '16.66' '2021/06' '2.84' '18.50' '8.11' '9.47' '6.00' '15.55' '19.00'
 '18.71' '26.81' '5.54' '23.33' '20.10' '7.97' '14.91' '10.04' '15.18'
 '7.78' '12.06' '19.01' '47.71' '12.35' '5.59' '11.74' '16.03' '5.36'
 '10.44' '24.22' '18.68' '15.80' '2.00' '2.23' '18.90' '36.00' '11.03'
 '6.19' '7.85' '9.82' '9.92' '4.28' '13.89' '2.52' '8.65' '23.63' '25.33'
 '1.49' '13.84' '4.89' '13.02' '4.23' '1.06' '7.30' '5.43' '21.19' '10.33'
 '14.87' '21.81' '6.72' '13.61' '13.79' '44.43' '21.14' '7.26' '1.26'
 '2.13' '6.39' '4.10' '11.58' '11.64' '20.25' '11.94' '8.57' '12.38'
 '5.26' '23.84' '9.55' '15.94' '7.55' '7.91' '7.47' '16.78' '32.13' '8.21'
 '-0.24' '48.06' '15.71' '9.88' '13.31' '8.20' '20.45' '14.50' '35.97'
 '17.13' '5.93' '12.07' '1.29' '32.65' '18.92' '21.18' '7.05' '19.87'
 '17.28' '18.57' '18.60' '7.76' '10.43' '12.44' '9.43' '16.33' '17.14'
 '17.94' '21.10' '9.73' '11.45' '3.19' '26.46' '16.10' '14.77' '7.80'
 '18.32' '20.30' '21.37' '1.45']
 스틱인베스트먼트026890 nan : 신생기업 2020년 이전 데이터 없음 crawled_index = [232, 233] # https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A026890&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701
 이리츠코크렙088260 : 신생기업 2020년 이전 데이터 없음  crawled_index = [440, 441] # https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A088260&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701 """

df_crawl_roe_rawdata = pd.read_csv('df_crawl_roe_rawdata.csv', index_col=[0])
df_crawl_bps_rawdata = pd.read_csv(
    'df_crawl_BPS(원)_rawdata.csv', index_col=[0])


def preprocessing(df):
    df = df.drop([232, 233, 440, 441])

    # index_filtering
    tmp_a = df[df['0'] == '2018/12'].index
    tmp_b = tmp_a.append(tmp_a + 1).sort_values()

    df_since_2018 = df.loc[tmp_b].reset_index(drop=True)
    df = df.drop(tmp_b).reset_index(drop=True)

    df = df.rename(columns=df.iloc[0]).drop(df.index[0]).reset_index(drop=True)
    df = df.drop(list(range(1, 689, 2)), axis=0).reset_index(drop=True)

    df_since_2018 = df_since_2018.rename(columns=df_since_2018.iloc[0]).drop(
        df_since_2018.index[0]).reset_index(drop=True)
    df_since_2018 = df_since_2018.drop(
        list(range(1, 7, 2)), axis=0).reset_index(drop=True)
    df_since_2018 = df_since_2018.loc[:, ['2019/12', '2020/12', 'stk_cd']]

    tmp_rename = ['2019/12', '2020/12', '2020/12[E]', 'stk_cd']
    df_since_2018.columns = tmp_rename
    df_since_2018 = df_since_2018.drop(
        '2020/12[E]', axis=1).reset_index(drop=True)

    df_roe_result = pd.merge(df, df_since_2018, how='outer', on=[
        '2019/12', '2020/12', 'stk_cd'])

    no_data = ['026890', '088260']
    tmp_df = pd.DataFrame({'stk_cd': no_data})

    df_roe_result = pd.merge(df_roe_result, tmp_df, how='outer', on='stk_cd')
    return df_roe_result


df_finance = pd.read_csv(
    '_with_stock_finance_as_select_s_stk_cd_s_stk_nm_sum_case_when_f__202302081934.csv')
df_finance['stk_cd'] = df_finance['stk_cd'].apply(
    lambda x: '{0:0>6}'.format(x))
df_finance.reset_index(drop=True, inplace=True)
print(df_finance.shape)


def preprocessing(df, target):
    df = df[['0', '8']].rename(columns={'0': target, '8': 'stk_cd'})
    df = df.iloc[lambda x: x.index % 2 == 1].reset_index(drop=True)
    return df


df_roe = preprocessing(df_crawl_roe_rawdata, 'ROE')
df_bps = preprocessing(df_crawl_bps_rawdata, 'BPS')


df_finance = pd.merge(
    df_finance, df_roe[['ROE', 'stk_cd']], how='inner', on=['stk_cd'])
df_finance = pd.merge(
    df_finance, df_bps[['BPS', 'stk_cd']], how='inner', on=['stk_cd'])



df_pcr = pd.read_csv('pcr_data.csv')
df_pcr.rename(columns={df_pcr.columns[0]: 'stk_cd'}, inplace=True)
df_pcr['stk_cd'] = df_pcr['stk_cd'].apply(lambda x: '{0:0>6}'.format(x))

df_finance = pd.merge(
    df_finance, df_pcr[['2019_PCR', 'stk_cd']], how='inner', on=['stk_cd'])
df_finance.rename(columns={'2019_PCR': 'PCR'}, inplace=True)
print(df_finance)

df_finance.to_csv('./finance+ROE+BPS+PCR.csv',
                  index=True, header=True)
