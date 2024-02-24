# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .inscrawler.crawler import InsCrawler
import os

# your Instragram credentials (to be used when scraping the website)
USERNAME = os.environ.get('USERNAME', '')
PASSWORD = os.environ.get('PASSWORD', '')


def get_posts_by_user(user_to_search):
    ins_crawler = InsCrawler(username=USERNAME, password=PASSWORD, has_screen=False)
    # need to load the user's profile before scraping their posts
    ins_crawler.load_user_profile(user_to_search)
    return ins_crawler.get_user_posts()
