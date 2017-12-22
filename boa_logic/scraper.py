import urllib.request
from bs4 import BeautifulSoup
import re

class Scraper():
    def __init__(self):
        self.btc_page = urllib.request.urlopen('https://coinmarketcap.com/currencies/bitcoin/historical-data/')
        self.eth_page = urllib.request.urlopen('https://coinmarketcap.com/currencies/ethereum/historical-data/')
        self.ltc_page = urllib.request.urlopen('https://coinmarketcap.com/currencies/litecoin/historical-data/')
        self.bch_page = urllib.request.urlopen('https://coinmarketcap.com/currencies/bitcoin-cash/historical-data/')

        self.btc_soup = BeautifulSoup(self.btc_page, 'html.parser')
        self.eth_soup = BeautifulSoup(self.eth_page, 'html.parser')
        self.ltc_soup = BeautifulSoup(self.ltc_page, 'html.parser')
        self.bch_soup = BeautifulSoup(self.bch_page, 'html.parser')

    def get_bct_price(self):
        btc_price = re.findall(r"[-+]?\d*\.\d+|\d+", self.btc_soup.find('span', attrs={'id':'quote_price'}).text)
        return float(btc_price[0])

    def get_eth_price(self):
        eth_price = re.findall(r"[-+]?\d*\.\d+|\d+", self.eth_soup.find('span', attrs={'id':'quote_price'}).text)
        return float(eth_price[0])

    def get_ltc_price(self):
        ltc_price = re.findall(r"[-+]?\d*\.\d+|\d+", self.ltc_soup.find('span', attrs={'id':'quote_price'}).text)
        return float(ltc_price[0])

    def get_bch_price(self):
        bch_price = re.findall(r"[-+]?\d*\.\d+|\d+", self.bch_soup.find('span', attrs={'id':'quote_price'}).text)
        return float(bch_price[0])
