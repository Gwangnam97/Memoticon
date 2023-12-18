import snscrape.modules.twitter as sntwitter
import snscrape.modules.facebook as snfacebook
import pandas as pd

data_list = []
tmp_list = []
query = "드립"
user_list = [] 
limit = 100

# for i,facebook in enumerate(snfacebook.Facebook)


for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query,mode = sntwitter.TwitterSearchScraperMode.USER).get_items()):
    if i>=limit:
        break
    else:
        try:
            user_list.append(tweet)
        except:
            print("망했는데?")
            
df_user = pd.DataFrame(user_list)

for y in range(22,20,-1):
    term =[
    f"since:20{y}-10-01 until:20{y}-12-31",
    f"since:20{y}-07-01 until:20{y}-09-30",
    f"since:20{y}-04-01 until:20{y}-06-31",
    f"since:20{y}-01-01 until:20{y}-03-31"]
    for tm in term:
        for user_name in df_user.username:
            query = f"from:{user_name} {tm}"
            limit = 5000
            for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
                if i >= limit:
                    print(user_name, tm)
                    break
                else:
                    try:
                        data_list.append(tweet)
                    except:
                        tmp_list.append(tweet)
            print(user_name)
        print(len(data_list)),"개", tm, print(len(tmp_list))

pd.DataFrame(data_list).to_csv("./data_list2.csv")
pd.DataFrame(tmp_list).to_csv("./tmp_list2.csv")