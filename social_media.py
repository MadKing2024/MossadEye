#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

class SocialMediaChecker:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def check_whatsapp(self, number):
        url = f"https://wa.me/{number}"
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except:
            return False

    def check_telegram(self, number):
        url = f"https://t.me/{number}"
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except:
            return False

    def check_facebook(self, number):
        url = f"https://facebook.com/phone/{number}"
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except:
            return False
