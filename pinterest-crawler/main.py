
from src import PinterestScraper, PinterestConfig
import pandas as pd


configs = PinterestConfig(search_keywords="짤", # Search word
                          file_lengths=500000,     # total number of images to download (default = "100")
                          image_quality="orig", # image quality (default = "orig")
                          bookmarks="")         # next page data (default= "")


PinterestScraper(configs).download_images()     # download images directly

# data_list = []
print(PinterestScraper(configs).get_urls())     # just bring image links



