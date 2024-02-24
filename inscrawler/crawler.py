from __future__ import unicode_literals

import glob
import os
import time
from builtins import open

from .browser import Browser
from .exceptions import RetryException
from .utils import retry


class Logging(object):
    PREFIX = "instagram-crawler"

    def __init__(self):
        try:
            timestamp = int(time.time())
            self.cleanup(timestamp)
            self.logger = open("/tmp/%s-%s.log" % (Logging.PREFIX, timestamp), "w")
            self.log_disable = True
        except Exception:
            self.log_disable = True

    def cleanup(self, timestamp):
        days = 86400 * 7
        days_ago_log = "/tmp/%s-%s.log" % (Logging.PREFIX, timestamp - days)
        for log in glob.glob("/tmp/instagram-crawler-*.log"):
            if log < days_ago_log:
                os.remove(log)

    def log(self, msg):
        if self.log_disable:
            return

        self.logger.write(msg + "\n")
        self.logger.flush()

    def __del__(self):
        if self.log_disable:
            return
        self.logger.close()


class InsCrawler(Logging):
    URL = "https://www.instagram.com"

    def __init__(self, username, password, has_screen=False):
        super(InsCrawler, self).__init__()
        self.browser = Browser(has_screen)
        self.page_height = 0
        self.login(username, password)
    
        
    def dismiss_save_login_prompt(self):
        save_login = self.browser.find_one('button')
        save_login.click()


    def login(self, username, password):
        browser = self.browser
        url = "%s/accounts/login/" % (InsCrawler.URL)
        browser.get(url)
        u_input = browser.find_one('input[name="username"]')
        u_input.send_keys(username)
        p_input = browser.find_one('input[name="password"]')
        p_input.send_keys(password + "\n")

        @retry(attempt=15)
        def check_login():
            if browser.find_one('input[name="username"]'):
                raise RetryException()

        check_login()
        self.dismiss_save_login_prompt()
        time.sleep(5)


    def load_user_profile(self, username):
        browser = self.browser
        url = "%s/%s/" % (InsCrawler.URL, username)
        browser.get(url)
        time.sleep(6)
        

    def get_user_posts(self):
        UPPER_BOUND = 25
        posts = []
        images = self.browser.find("img")
        for index, img in enumerate(images):
            if index > UPPER_BOUND:
                break
            caption = img.get_attribute("alt")
            img_src = img.get_attribute("src")
            posts.append(
                {
                    'caption': caption,
                    'img': img_src
                }
            )
        return posts
