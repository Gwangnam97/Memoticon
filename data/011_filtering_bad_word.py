import pandas as pd

df = pd.read_csv(r'C:\Memoticon\data\data.tsv', sep='\t',encoding="utf-8-sig")
print(df.info())

# List of keywords to filter out
filter_list = [
    "대권",
    "박형준",
    "강경화",
    "청문회",
    "변희재",
    "손혜원",
    "김진태",
    "홍준표",
    "의원",
    "국당",
    "후보자",
    "윤석렬",
    "박근혜",
    "총리후보",
    "대권후보",
    "최민희",
    "19",
    "29금",
    "75G컵",
    "75c컵",
    "A컵녀",
    "G컵인데요",
    "H컵녀",
    "ass",
    "bj",
    "manga",
    "manhwa",
    "sexy",
    "ㅗㅜㅑ",
    "가슴",
    "꼴리다",
    "꼴린말",
    "노출",
    "딸감",
    "모델",
    "미성년자",
    "벗기다",
    "변태",
    "보추",
    "비제이",
    "비키니",
    "빨갱이",
    "뽕가슴슴가구라사",
    "뽕가슴슴가구라사기",
    "사고",
    "성기",
    "성인용",
    "성인용품",
    "성추행",
    "성폭행",
    "섹스",
    "섹시",
    "소전철혈보스한테서팬티파밍하는만화후방",
    "아프리카",
    "야당",
    "야동",
    "야릇",
    "야설",
    "야짤",
    "야하",
    "야한",
    "야함",
    "야해",
    "야해도",
    "야해요",
    "야해지",
    "야했던",
    "약후방",
    "여자가슴",
    "여친",
    "엮쓰썸쓰가슴가슴",
    "오우야",
    "완꼴",
    "개꼴",
    "왕가슴",
    "유튜브",
    "은꼴",
    "음란마귀",
    "일본",
    "작은가슴",
    "젖",
    "최소B컵",
    "크리스마스",
    "큰가슴",
    "테러",
    "트위치",
    "팬더",
    "팬더티비",
    "후방",
    "김영춘",
    "자한당",
    "도지사",
    "대선후보",
    "서울시장",
    "윤석열",
    "이재명",
    "대통령",
    "국힘",
    "조국",
    "조후보",
    "진보",
    "보수",
    "교육감",
    "박정희",
    "자유당",
    "국민의당",
    "문재인",
    "새누리당",
    "국회의원",
    "대선",
    "국정원",
    "미래통합당",
    "안철수",
    "부실후보",
]

filter_list = list(set(filter_list))
# filter_list.sort()

# index_contain_filtering_word
index_cfw = []

for filter_word in filter_list:
    contain_word_index_list = df[df["hashtag"].str.contains(filter_word)].index
    index_cfw.extend(contain_word_index_list)

index_cfw = list(set(index_cfw))
# print(f"num of filterd index = len(index_cfw) : {len(index_cfw)}", end="\n\n\n")
# =======================================================================================
# df2 = df.loc[df.index.isin(index_cfw)]
# df2.to_csv("./inappropriate_words_filtered.csv", index=False)
# =======================================================================================

df.drop(index_cfw, inplace=True)
print(df.info())

df.to_csv('test.csv',index=False,sep='\t')
