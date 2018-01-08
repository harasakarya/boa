import urllib.request
from bs4 import BeautifulSoup
import re
from datetime import datetime as dt
import pandas

class Scraper():

    def get_current_price(self, name):

        self.soup = BeautifulSoup(urllib.request.urlopen('https://coinmarketcap.com/currencies/' + name + '/historical-data/'), 'html.parser')

        price =  re.findall(r"[-+]?\d*\.\d+|\d+", self.soup.find('span', attrs={'id':'quote_price'}).text)
        return float(price[0])

    def get_price_history(self, name):

        self.soup = BeautifulSoup(urllib.request.urlopen('https://coinmarketcap.com/currencies/' + name + '/historical-data/?start=20130428&end=20180104'), 'html.parser')

        series = pandas.Series()

        for row in reversed(self.soup.findAll('table')[0].tbody.findAll('tr')):
            series = series.append(pandas.Series([float(row.findAll('td')[4].contents[0])], [dt.strptime(row.findAll('td')[0].contents[0], "%b %d, %Y").strftime("%Y-%m-%d")]))

        if dt.now().strftime("%Y-%m-%d") not in series:
            series = series.append(
                pandas.Series([self.get_current_price(name)], [dt.now().strftime("%Y-%m-%d")]))

        return(series)
