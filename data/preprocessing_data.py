import pandas as pd


def preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    print(f"origin len : {len(df)}")
    df.drop(
        columns=["text", "hashtag", "crawled_at", "text_tag", "ocr_text", "ocr_tag"],
        inplace=True,
    )

    # 컬럼명 변경
    df.rename(columns={"total_tag": "hashtag"}, inplace=True)

    # 쓰레기 버리기
    df = df[df["hashtag"] != "삭제되었거나,비공개된,게시물입니다."]
    df = df[df["url"] != "https://www.ppomppu.co.kr/images/icon_app_20160427.png"]
    df = df[df["hashtag"] != ""]
    df.drop_duplicates(inplace=True)
    df.dropna(subset="hashtag", inplace=True)
    print(f"after drop len : {len(df)}")

    # 중복 검출
    # print(f'df["url"].nunique() : {df["url"].nunique()}')
    tmp_count = df["url"].value_counts()

    # url 유니크 데이터
    unique_urls = tmp_count[tmp_count == 1].index
    df_unique = df[df["url"].isin(unique_urls)]

    # url 중복 데이터
    duplicate_urls = tmp_count[tmp_count != 1].index
    df_duplicate = df[df["url"].isin(duplicate_urls)]

    print(f"len(df_unique) : {len(df_unique)}")
    # print(df_unique)

    df_duplicate.sort_values(by="url", inplace=True)
    print(f"len(df_duplicate) : {len(df_duplicate)}")
    # print(df_duplicate.head(20))

    # 그룹화 및 병합
    df_dup_merged = df_duplicate.groupby("url").agg({"hashtag": "sum"}).reset_index()
    print(f"len(df_dup_merged) : {len(df_dup_merged)}", end="\n\n")

    print(
        f'sample df_dup_merged["hashtag"] : \n{df_dup_merged["hashtag"].head(2)}',
        end="\n\n",
    )

    # 유니크, 중복 데이터 병합
    df = pd.concat([df_unique, df_dup_merged]).reset_index(drop=True)

    # 문자열 분리 및 중복 제거 함수
    def split_and_remove_duplicates(row):
        split_values = row["hashtag"].split(",")
        unique_values = list(set(split_values))
        return ",".join(unique_values)

    # `,`로 시작하는 row를 삭제하는 함수
    def remove_comma_starting_rows(row):
        if row["hashtag"].startswith(","):
            return row["hashtag"][1:]
        else:
            return row["hashtag"]

    # apply() 메소드를 이용하여 각 row에 함수 적용
    df["hashtag"] = df.apply(remove_comma_starting_rows, axis=1)
    df["hashtag"] = df.apply(split_and_remove_duplicates, axis=1)

    print(f"After preprocessing len(df) : {len(df)}")
    print(f"After preprocessing df.head() : \n{df.head()}", end="\n\n")

    # List of keywords to filter out
    filter_list = [
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
    ]

    filter_list = list(set(filter_list))
    # filter_list.sort()

    # index_contain_filtering_word
    index_cfw = []

    for filter_word in filter_list:
        contain_word_index_list = df[df["hashtag"].str.contains(filter_word)].index
        index_cfw.extend(contain_word_index_list)

    index_cfw = list(set(index_cfw))
    print(f"num of filterd index = len(index_cfw) : {len(index_cfw)}", end="\n\n\n")
    # =======================================================================================

    df2 = df.loc[df.index.isin(index_cfw)]
    df2.to_csv("./filtered.csv", index=False)

    # =======================================================================================

    df.drop(index_cfw, inplace=True)
    print(f"final len(df) : {len(df)}")
    print(f"final df.head() : \n{df.head()}", end="\n\n")

    return df


def get_hashtag_count(df: pd.DataFrame) -> pd.DataFrame:
    # 각 태그마다 등장 횟수를 세어서 내림차순으로 정렬
    hashtag_count = (
        df["hashtag"].str.split(",", expand=True).stack().value_counts().reset_index()
    )
    hashtag_count.columns = ["hashtag", "count"]

    # split 실행 후 생성된 공백 제거
    df_hc = hashtag_count[1:]

    # 1글자 태그 삭제
    df_hc = df_hc.loc[df_hc["hashtag"].str.len() > 1]

    print(f"df_hc.head() : \n{df_hc.head()}")


pd.set_option("mode.chained_assignment", None)


if __name__ == "__main__":
    path = "C:\Memoticon\data\data.csv"
    df = pd.read_csv(rf"{path}", low_memory=False, memory_map=True)
    df = preprocessing(df)
    df_tag = get_hashtag_count(df)
    df_tag.to_csv('./hashtag.csv')
