import pandas as pd

df = pd.read_csv(r'C:\Memoticon\data\data_origin.csv',index_col=[0])
ddf = pd.read_csv(r'C:\Memoticon\data\001_remain_url_status_is_200.csv',index_col=[0])

print(f'Before remain_url_status_is_200 :')
print(df.info())
print(f'After remain_url_status_is_200 :')
print(ddf.info(),end="\n\n")

df = pd.read_csv(r'C:\Memoticon\data\001_remain_url_status_is_200.csv',index_col=[0])
ddf = pd.read_csv(r'C:\Memoticon\data\002_drop_garbage_data.csv',index_col=[0])

print(f'Before drop_garbage :')
print(df.info())
print(f'After drop_garbage :')
print(ddf.info(),end="\n\n")


df = pd.read_csv(r'C:\Memoticon\data\002_drop_garbage_data.csv',index_col=[0])
ddf = pd.read_csv(r'C:\Memoticon\data\003_hand_cleaning.csv',index_col=[0])

print(f'Before hand_cleaning :')
print(df.info())
print(f'After hand_cleaning :')
print(ddf.info(),end="\n\n")


df = pd.read_csv(r'C:\Memoticon\data\003_hand_cleaning.csv',index_col=[0])
ddf = pd.read_csv(r'C:\Memoticon\data\004_word_filtering.csv',index_col=[0])

print(f'Before word_filtering :')
print(df.info())
print(f'After word_filtering :')
print(ddf.info(),end="\n\n")


