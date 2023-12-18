import numpy as np
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread as gs
import warnings
warnings.simplefilter(
    action='ignore', category=FutureWarning)  # FutureWarning 제거

json_file = 'pencore1208-137514fd3f71.json'


df_select = pd.read_csv('select_stock.ver1.1.csv')


df_select['stk_cd'] = df_select['stk_cd'].apply(lambda x: '{0:0>6}'.format(x))


df_history = pd.read_csv('history_dt.csv', header=None, low_memory=False)
df_history.rename(columns={0: 'stk_cd', 1: 'dt', 2: 'o_prc', 3: 'h_prc', 4: 'l_prc', 5: 'c_prc', 6: 'vol', 7: 'chg_rt', 8: 'm30_prc', 9: 'm50_prc',
                           10: 'm10_prc', 11: 'm20_prc', 12: 'm60_prc', 13: "m30_vol", 14: 'm50_vol', 15: 'm10_vol', 16: 'm20_vol', 17: 'm60_vol', 18: 'stk_dt_no'}, inplace=True)


df = df_history[df_history['stk_cd'].isin(
    df_select['stk_cd'])].reset_index(drop=True)


column_name = [element.upper() for element in df.columns]
df.columns = column_name


df = df[['STK_CD', 'DT', 'C_PRC', 'O_PRC', 'H_PRC', 'L_PRC', 'VOL']]
df["DT"] = pd.to_datetime(df["DT"])
df.loc[:, "C_PRC":] = df.loc[:, "C_PRC":].astype(int)


# 전일 대비 상승, 하락 변수 생성하기
df["diff"] = df["C_PRC"].diff()


def UD(diff):
    """
    diff 값을 입력받아 0이면 ups, downs을 0으로 
    0보다 크면 ups 에 diff값을 작으면 downs 에 abs(diff) 값을 반환합니다.
    ups = 전날 주가보다 오늘 주가가 상승할 때의 주가 상승폭(up)
    downs = 전날 주가보다 오늘 주가가 하락할 때의 주가 하락폭(down)
    """
    ups = 0
    downs = 0
    # 전날주가 - 오늘주가가 0 초과
    if diff > 0:
        # 상승치를 ups에 대입
        ups = diff
    elif diff < 0:  # 전날주가 - 오늘주가가 0 미만
        # 하락치의 절대값 (abs)를 downs 에 대입
        downs = abs(diff)
    # ups와 downs 를 Series(DataFrame 칸) 으로 만들어서 리턴
    return pd.Series([ups, downs])


def upload_to_spreadsheet(df, sheet_name="sample"):

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        json_file, scope
    )

    gc = gs.authorize(credentials)
    # GET https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values:batchGet
    spreadsheet_key = '1VBHyz4w3ImqsGrku6ajzgHH1T79P19ho9i9N7YpR1vs'
    wks = sheet_name  # sheet_name
    spreadsheet = gc.open_by_key(spreadsheet_key)
    values = [df.columns.values.tolist()]
    values.extend(df.values.tolist())
    spreadsheet.values_update(
        wks, params={"valueInputOption": "USER_ENTERED"}, body={"values": values}
    )
    print("done upload_to_spreadsheet\n")


#  df["diff"] 컬럼 데이터에 UD 함수를 실행해서 상승분과 하락분을 계산하고
# 상승분은 U, 하락분은 D 컬럼에 저장
df[["U", "D"]] = df["diff"].apply(UD)
df[["U", "D"]] = df["diff"].apply(UD)

# AU / AD 변수 생성하기
# * AU = 일정기간(N일,보통14일) 동안의 U의 평균값(average ups)
# * AD = 일정기간(N일,보통14일) 동안의 D의 평균값(average downs)
df["AU"] = df["U"].rolling(14).mean()

# AD = 일정기간(N일,보통14일) 동안의 D의 평균값(average downs)
df["AD"] = df["D"].rolling(14).mean()

# RS = AU(일정기간(N일,보통14일) 동안의 U의 평균값(average ups) ) / AD (일정기간(N일,보통14일) 동안의 D의 평균값(average downs))
df["RS"] = df["AU"] / df["AD"]

# AU / (AU+AD) = RS / (1+RS)
df["RSI"] = df["RS"] / (1 + df["RS"])

# RSI signal 만들기
# * RSI 시그널 = RSI의 이동평균선 (6일의 이동평균선 사용)

# RSI_signal 변수를 생성합니다.
df['RSI_signal'] = df["RSI"].rolling(6).mean()

# DT 컬럼 (날짜) 를 인덱스로 설정
# df = df.set_index("DT")

# RSI의 해석
# 1. RSI는 50%를 기준으로, 50% 이상은 매수세 우세, 50% 이하는 매도세 우세를 나타냅니다.
# 2. RSI가 70% 이상이면 매수세가 상당히 커서 초과매수 국면에 돌입했다고 판단합니다.
# 3. RSI가 30% 이하이면 매도세가 상당히 커서 초과매도 국면에 돌입했다고 판단합니다.
# 4. RSI가 시그널선을 상향돌파하면 단기적으로 매수세가 늘어나는 추세라고 판단합니다.
# 5. RSI가 시그널선을 하향돌파하면 단기적으로 매도세가 늘어나는 추세라고 판단합니다.


df = df.fillna('0')
df['DT'] = df['DT'].astype(str)
df.loc[:, "U":] = df.loc[:, "U":].astype(str)
df_tmp = df_select[['stk_cd', 'stk_nm']]
df_tmp = df_tmp.rename(columns={'stk_cd': 'STK_CD'})

# print(dict(enumerate(df_tmp["STK_CD"])))
print(dict(zip(df_tmp['STK_CD'], df_tmp['stk_nm'])))
df['STK_NM'] = df['STK_CD'].map(dict(zip(df_tmp['STK_CD'], df_tmp['stk_nm'])))

# column_name = [element.lower() for element in df.columns]
# df.columns = column_name
# upload_to_spreadsheet(df, 'RSI')

# SELL (rate of return) 수익률
# (sell 종가 - buy 종가) / buy 종가 * 100

# 1. 매수 RSI가 30% 미만 & RSI_SIGNAL 을 초과할 때 or 만날 때
# 2. 매도 RSI가 70% 초과 & RSI_SIGANL 보다 떨어질 때 or 만날 때

df = df[['STK_CD', 'STK_NM',  'DT', 'C_PRC',  'RSI', 'RSI_signal']]

df[['RSI', 'RSI_signal']] = df[['RSI', 'RSI_signal']].astype('float32')
# df[['RSI', 'RSI_signal']] = df[['RSI', 'RSI_signal']].astype('int32')

# df = df.loc[(df[["RSI"]] < 0.3) & (df[["RSI"]] > 0.7)]

# df = pd.concat([df[df['RSI'] > 0.7], df[df['RSI'] < 0.3]]).sort_values(by=["STK_CD", "DT"])
df = df[df["RSI"] != 0]
df["DT"] = pd.to_datetime(df["DT"])

# Select rows where RSI is less than 0.3 and RSI_signal is greater than or equal to DT
condition1 = (df['RSI'] <= 0.3) & (df['RSI_signal'] <=
                                   0.3) & (df['RSI_signal'] >= df['RSI'])
dt_values1 = df.loc[condition1]


# Select rows where RSI is greater than or equal to 0.7 and RSI_signal is less than DT
condition2 = (df['RSI'] >= 0.7) & (df['RSI_signal'] >=
                                   0.7) & (df['RSI_signal'] <= df['RSI'])
dt_values2 = df.loc[condition2]


# Combine the two results and print the values of DT
dt_values = pd.concat([dt_values1, dt_values2]
                      ).sort_values(by=['STK_CD', 'DT'])

condition1 = (dt_values['DT'] >= '2020-01-01')
dt_values = dt_values.loc[condition1]

dt_values['RSI'] = dt_values['RSI'].round(2)
df = dt_values.copy()


def 수익률구하기(df, stk_cd: str):

    df = dt_values[dt_values["STK_CD"] == stk_cd]
    # print(df)

    # 매수 / 매도 시점
    # - 매수 조건
    #  1) RSI 30% 이하일 때
    #  2) RSI < RSI Signal
    #  3) RSI가 하락에서 상승으로 변경 시

    # - 매도 조건
    #  1) RSI 70% 이상일 때
    #  2) RSI > RSI Signal
    #  3) RSI가 상승에서 2번 하락으로 꺾일 시
    #  매도 못했을 때 12월 내에, RSI가 70% 이상일 경우 바로 매도....
    #  ex) 탑엔지니어링

    condition1 = (df['RSI'] <= 0.3)
    df_001 = df.loc[condition1].reset_index(drop=True)
    rsi_data = df_001['RSI'][0]

    buy_dict = []
    for i in range(len(df_001)):

        if rsi_data > df_001['RSI'][i]:
            rsi_data = df_001['RSI'][i]
            add_dict = {
                "DT": df_001['DT'][i],
                "C_PRC": df_001['C_PRC'][i]
            }
            buy_dict.append(add_dict)
        elif rsi_data < df_001['RSI'][i]:
            rsi_data = df_001['RSI'][i]

    df_buy = pd.DataFrame(buy_dict)

    # RSI가 하락에서 상승으로 변경 시
    # print(df_buy.loc[:0])

    condition2 = (df['RSI'] >= 0.7)
    df_002 = df.loc[condition2].reset_index(drop=True)
    rsi_data = df_002['RSI'][0]

    sell_dict = []
    for i in range(len(df_002)):

        if rsi_data > df_002['RSI'][i]:
            rsi_data = df_002['RSI'][i]
            # print(df_002['DT'][i])
            # print(df_002['C_PRC'][i])
            add_dict = {
                "DT": df_002['DT'][i],
                "C_PRC": df_002['C_PRC'][i]
            }
            sell_dict.append(add_dict)
        elif rsi_data < df_002['RSI'][i]:
            rsi_data = df_002['RSI'][i]

    df_sell = pd.DataFrame(sell_dict)
    # RSI가 상승에서 하락 추세 전환 2번일 경우

    # df_sell = df_sell.loc[df_sell['DT'] > df_buy['DT']]

    df_sell = df_sell[np.where(df_sell['DT'] > df_buy['DT'][0])[
        0][0]:].reset_index(drop=True)
    # print(f'df_sell : {df_sell}')
    # print(f'df_buy : {df_buy}')
    # print(df_result)

    # 수익률 = (('sell 종가' - 'buy 종가') % 'buy 종가') * 100
    # print(f'df_sell.loc[1:] : {df_sell.loc[:]}')
    try:
        df_result = pd.concat(
            [df_buy.loc[:0], df_sell.loc[1:1]]).reset_index(drop=True)
        sell = df_result['C_PRC'][1]
        buy = df_result['C_PRC'][0]
        print(f'buy : {buy}\nsell : {sell}')
        return ((sell - buy) * 100) // buy

    except:
        df_result = pd.concat(
            [df_buy.loc[:0], df_sell.loc[:0]]).reset_index(drop=True)
        sell = df_result['C_PRC'][1]
        buy = df_result['C_PRC'][0]
        print(f'buy : {buy}\nsell : {sell}')
        return ((sell - buy) * 100) // buy


result = 0
for i in df_select["stk_cd"].unique():
    print(f'stk_cd : {i}')
    수익률 = 수익률구하기(df, i)
    print(f'수익률 : {수익률}\n')
    result += 수익률


result = round(result / 9, 1)
print(f"총 수익률 : {result}%")
print(f'총 수익 : {(result * 250) / 100}억원')
