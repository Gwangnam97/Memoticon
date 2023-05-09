import pandas as pd
pd.set_option("mode.chained_assignment", None)
# df1 = pd.read_csv(r'C:\Users\Gwang\Desktop\새 폴더\re_tag2 - re_tag2.csv')
# df2 = pd.read_csv(r'C:\Users\Gwang\Desktop\새 폴더\김경진.csv')
# df3 = pd.read_csv(r'C:\Users\Gwang\Desktop\새 폴더\남광현.csv')
# ddf = pd.read_csv(r'C:\Users\Gwang\Desktop\새 폴더\윤환희.csv')
# df3.rename(columns={"tatal_final_tag":"total_final_tag"},inplace=True)
# df_merge = pd.concat([df1,df2])
# df_merge = pd.concat([df_merge,df3])
# df_merge = pd.concat([df_merge,df4])
# df_merge.to_csv(r'C:\Memoticon\data\data_hand_labeling.csv',index=False, encoding='utf-8-sig')

df_hand = pd.read_csv(r'C:\Memoticon\data\data_hand_labeling - merged_data.csv', encoding='utf-8-sig')
df_data_ver5 = pd.read_csv(r'C:\Memoticon\data\filtered_data_ver5.csv', encoding='utf-8-sig')

print(len(df_data_ver5))
print(len(df_data_ver5.drop_duplicates(subset=["url"],keep="first")))

df = pd.concat([df_hand,df_data_ver5])
df = df.astype({'url':'str'})

print(len(df))
print(len(df_hand))
print(len(df_hand.drop_duplicates(subset=["url"],keep="first")))

df = df.astype({'url':'str'})


# 중복 검출
tmp_count = df["url"].value_counts()

# url 유니크 데이터
unique_urls = tmp_count[tmp_count == 1].index
df_unique = df[df["url"].isin(unique_urls)]

# url 중복 데이터
duplicate_urls = tmp_count[tmp_count != 1].index
df_duplicate = df[df["url"].isin(duplicate_urls)]

print(f"len(df_unique) : {len(df_unique)}")

df_duplicate.sort_values(by="url", inplace=True)
print(f"len(df_duplicate) : {len(df_duplicate)}")

# 그룹화 및 병합
df_dup_merged = df_duplicate.groupby("url").agg({"hashtag": "sum"}).reset_index()
print(f"len(df_dup_merged) : {len(df_dup_merged)}", end="\n\n")

print(
    f'sample df_dup_merged["hashtag"] : \n{df_dup_merged["hashtag"].head(2)}',
    end="\n\n",
)

# 유니크, 중복 데이터 병합
df = pd.concat([df_unique, df_dup_merged]).reset_index(drop=True)

df = df[['url','hashtag']]
print(len(df))
print(len(df.drop_duplicates(subset='url')))
print(df.head())
df.to_csv('./001_병합+중복데이터삭제.csv')

# df = df.drop_duplicates(subset=["url"],keep="first").reset_index(drop=True)

# print(len(df))

# duplicated_df.to_csv(r'./duplicated_df.csv')
