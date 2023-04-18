from src import PinterestScraper, PinterestConfig
import pandas as pd


def pinterest_crawl_to_csv(search_keywords):
    configs = PinterestConfig(search_keywords=search_keywords,  # Search word
                              # total number of images to download (default = "100")
                              file_lengths=10,
                              # image quality (default = "orig")
                              image_quality="orig",
                              bookmarks="")         # next page data (default= "")

    # PinterestScraper(configs).download_images() # download images directly (photos/atatürk, photos/web-scraping)

    data = PinterestScraper(configs).get_urls()

    # table 생성 & 값 입력
    df = pd.DataFrame(columns=["url",  "title", "description",
                      "display_description", "link", "created_at"], data=data)
    return df


if __name__ == "__main__":
    csv_path = r'C:\Memoticon\Crawl_gh\pinterest.csv'

    search_keywords = ['밈', '밈 짤', '밈 고양이', '밈 강아지', '밈 절망',
                       '밈 한국어', '밈 그리기', '밈 유머 짤', '짤 모음',
                       '짤 말풍선', '짤 귀여운', '짤', '짤 모음', '짤 대전을 시작하지',
                       '짤 gif', '웃긴 짤', '29살 짤', '트위터 짤', '트위터',
                       '고양이 짤', '무한도전 짤', '직장인 짤', '해리포터 짤', 'mbti짤',
                       'mbti밈', '인터넷 밈 짤', '동물 짤 밈', '밈 짜증', '짜증나는 밈',
                       '웃긴 밈 짜증', '짜장면 밈', '짜파게티 밈', '짜증날 때 밈', '행복할 때 밈',
                       '슬플 때 밈', '유용한 짤', '카톡할때 유용한 짤', '유용한 카톡 짤', '짤 저장소']

    result = pd.DataFrame(columns=[
                          "url",  "title", "description",   "display_description", "link", "created_at"])

    for i in search_keywords:
        df = pinterest_crawl_to_csv(i)
        result = pd.concat([result, df])

    result.drop_duplicates(subset='url', inplace=True)
    result.to_csv(csv_path, encoding='utf-8')
