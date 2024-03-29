import requests
import json
import os
import urllib
import sys


class Scraper:

    def __init__(self, config, image_urls=[]):
        self.config = config
        self.image_urls = image_urls

    # Set config for bookmarks (next page)
    def setConfig(self, config):
        self.config = config

    # Download images
    def download_images(self):
        folder = "photos/"+self.config.search_keyword.replace(" ", "-")
        number = 0
        # prev get links
        results = self.get_urls()
        try:
            os.makedirs(folder)
            print("Directory ", folder, " Created ")
        except FileExistsError:
            a = 1
        arr = os.listdir(folder+"/")
        for i in results:
            if str(i + ".jpg") not in arr:
                try:
                    file_name = str(i.split("/")[len(i.split("/"))-1])
                    download_folder = str(folder) + "/" + file_name
                    print("Download ::: ", i)
                    urllib.request.urlretrieve(i,  download_folder)
                    number = number + 1
                except Exception as e:
                    print(e)

    # get_urls return array
    def get_urls(self):
        SOURCE_URL = self.config.source_url,
        DATA = self.config.image_data,
        URL_CONSTANT = self.config.search_url
        r = requests.get(URL_CONSTANT, params={
                         "source_url": SOURCE_URL, "data": DATA})
        jsonData = json.loads(r.content)
        resource_response = jsonData["resource_response"]
        data = resource_response["data"]
        results = data["results"]

        # json 으로 내용 확인
        # with open('myfile.txt', 'w') as f:
        #     print(resource_response, file=f)

        for i in results:
            # self.image_urls.append(
            #     i["images"][self.config.image_quality]["url"])

            if i['rich_summary'] != None:
                display_description = i['rich_summary']['display_description']
                display_name = i['rich_summary']['display_name']
            else:
                display_description = "None"
                display_name = "None"

            self.image_urls.append(
                dict(
                    url=i["images"][self.config.image_quality]["url"],  # 사진 url
                    title=i['grid_title'],  # 제목
                    description=i['description'],   # 설명
                    created_at=i['created_at'],  # 생성 날짜
                    link=i['link'],  # 원본 url
                    display_description=display_description,
                    display_name=display_name
                )
            )

        if len(self.image_urls) < int(self.config.file_length):
            try:
                self.config.bookmarks = resource_response["bookmark"]
            except:
                return None

            print("Creating links : ", len(self.image_urls))
            self.get_urls()

        # return self.image_urls[0:self.config.file_length]
        return self.image_urls[0:self.config.file_length]

        # if len(str(resource_response["bookmark"])) > 1 : connect(query_string, bookmarks=resource_response["bookmark"])
