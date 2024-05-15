import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import random
from random import choice
import time

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.14.1) Presto/2.12.388 Version/12.16'
]

class AmazonReviewScraper:
    def __init__(self, reviews_url, len_page=3):
        self.reviews_url = reviews_url
        self.len_page = len_page
        self.headers = {
            'authority': 'www.amazon.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'user-agent': choice(USER_AGENTS),
            'Referer': 'https://www.google.com/'
        }
    
    def _reviews_html(self):
        soups = []
        for page_no in range(1, self.len_page + 1):

            params = {
                'ie': 'UTF8',
                'reviewerType': 'all_reviews',
                'filterByStar': 'all_stars',
                'pageNumber': page_no,
            }
            response = requests.get(self.reviews_url, headers=self.headers, params=params)  # Update here
            soup = BeautifulSoup(response.text, 'lxml')
            soups.append(soup)
            time.sleep(random.randint(2, 10))
            print(page_no)
        return soups
    
    def _get_reviews(self, html_data):
        data_dicts = []
        boxes = html_data.select('div[data-hook="review"]')
        for box in boxes:
           
            try:
                stars = box.select_one('[data-hook="review-star-rating"]').text.strip().split(' out')[0]
            except Exception as e:
                stars = 'N/A'
            try:
                description = box.select_one('[data-hook="review-body"]').text.strip()
            except Exception as e:
                description = 'N/A'
            data_dict = {

                'Stars' : stars,

                'Description' : description
            }
            data_dicts.append(data_dict)
        return data_dicts
    
    def scrape_reviews(self):
        html_datas = self._reviews_html()
        reviews = []
        for html_data in html_datas:
            review = self._get_reviews(html_data)
            reviews += review
        df_reviews = pd.DataFrame(reviews)
        return df_reviews