from src import PinterestScraper, PinterestConfig
import pandas as pd


def pinterest_crawl_to_csv(search_keywords: str) -> pd.DataFrame:
    configs = PinterestConfig(search_keywords=search_keywords,  # Search word
                              # total number of images to download (default = "100")
                              file_lengths=1000000,
                              # image quality (default = "orig")
                              image_quality="orig",
                              bookmarks="")         # next page data (default= "")

    # PinterestScraper(configs).download_images() # download images directly (photos/atatürk, photos/web-scraping)

    data = PinterestScraper(configs).get_urls()

    # table 생성 & 값 입력
    df = pd.DataFrame(columns=[
        "url",  "title", "description", "display_name", "display_description", "link", "created_at"], data=data)
    df['crawled_at'] = search_keywords

    return df


if __name__ == "__main__":

    search_keywords = ['짤 대전을 시작하지', '짤 저장소']
    tmp_list = ['분노', '경멸', '혐오', '공포', '행복', '절망', '귀여운', '중립', '말풍선', '슬픔', '슬픈', '놀람', '최신', '화남', '좋아', '황당', '닥쳐', '멘붕', '칭찬', '눈물', '오글',
                '철컹', '레전드', '정치', '솔로', '이말년', '침착맨', '무도', '무한도전', '커플', '눈물', '추노', '독수리', '웃긴', '고양이', '직장인', '해리포터', '유용한 짤', 'mbti', '트위터', '강아지']

    search_keywords.extend(word+" 밈" for word in tmp_list)
    search_keywords.extend(word+" 짤" for word in tmp_list)
    search_keywords.extend(word+" 짤방" for word in tmp_list)
    # 중복 값 제거
    search_keywords = list(set(search_keywords))

    # DataFrame
    result = pd.DataFrame(columns=[
                          "url",  "title", "description", "display_name", "display_description", "link", "created_at", "crawled_at"])
    for i in search_keywords:
        df = pinterest_crawl_to_csv(i)
        result = pd.concat([result, df])

    csv_path = r'Crawl_gh\csv'
    result.drop_duplicates(subset='url', inplace=True)
    result.to_csv(csv_path, encoding='utf-8')
