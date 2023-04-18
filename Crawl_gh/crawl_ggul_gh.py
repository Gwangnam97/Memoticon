# %%
import requests
from bs4 import BeautifulSoup as bs
import time

# requests base setting
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


url_limit = range(1, 15187261)


def ggoorr_crawl_all(urls):
    try:
        fornt_url = "https://ggoorr.net/all/"
        url = fornt_url + str(urls)

        # get html
        soup = bs(requests.get(url, headers=headers).text, "lxml")

        # check status
        # status = req.status_code

        # target, labeling imgs, title
        find_img = soup.find_all("img", {"editor_component": "image_link"})
        img_list = []
        for tag in find_img:
            src = tag.get('src')
            img_list.append(src)

        find_vid = soup.find_all("video")
        vid_list = []
        for tag in find_vid:
            src = tag.get('src')
            vid_list.append("https://cdn.ggoorr.net/"+src)

        find_title = soup.find("h1", {"class": "np_18px"}).get_text()

        tmp = dict(
            title=find_title,
            img=img_list,
            vid=vid_list,
        )
        return tmp
    except:
        print("passed")
        pass


result_list = []
# result_list.append(ggoorr_crawl_all(15187211))
# result_list.append(ggoorr_crawl_all(15185966))
for i in url_limit:
    result_list.append(ggoorr_crawl_all(i))
    time.sleep(1)


print(result_list)

# %%
