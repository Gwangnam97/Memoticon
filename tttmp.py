# import pandas as pd

# df = pd.read_csv(r'C:\Memoticon\Crawl_gh\csv\naver.csv')
# df = df.drop(columns='img',axis=1)
# df.to_csv('./teeest.csv',index=True)


# cursor.execute('SELECT url FROM pin_test order by rand() limit 1')
cursor.execute('SELECT url FROM teeest order by rand() limit 3')

# Fetch results
results = cursor.fetchall()
results[0][0]
results[1][0]
results[2][0]

res = {"version": "2.0",
       "template": {"outputs": [{
                                "listCard": {
                                    "header": {
                                        "title": "listCard 테스트"
                                    },
                                    "items": [
                                        {
                                            "title": "listCard 테스트#1",
                                            "description": "listCard 테스트#1 description",
                                            "imageUrl": results[0][0],
                                            "link": {
                                                "web": results[0][0]
                                            }
                                        },
                                        {
                                            "title": "listCard 테스트#2",
                                            "description": "listCard 테스트#2 description",
                                            "imageUrl": results[1][0],
                                            "link": {
                                                "web": results[1][0]
                                            }
                                        },
                                        {
                                            "title": "listCard 테스트#3",
                                            "description": "listCard 테스트#3 description",
                                            "imageUrl": results[2][0],
                                            "link": {
                                                "web": results[2][0]
                                            }
                                        },
                                    ],
                                    "buttons": [
                                        {
                                            "label": "네이버링크",
                                            "action": "webLink",
                                            "webLinkUrl": "https://www.naver.com"
                                        }
                                    ]
                                }
                                }
                                ]
                    }
       }
