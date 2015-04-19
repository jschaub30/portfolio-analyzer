#!/usr/bin/python

import requests
import bs4

# 100% US Stock market
url='http://www.portfoliovisualizer.com/backtest-asset-class-allocation?s=y&mode=2&annualOperation=1&endYear=2013&initialAmount=15000&portfolio3=Custom&portfolio2=Custom&portfolio1=Custom&TotalStockMarket1=100&annualAdjustment=15000&startYear=1972'

response = requests.get(url)
soup = bs4.BeautifulSoup(response.text)

b=[a.attrs['id'] for a in soup.find_all('input') if 'id' in a.attrs]
print "'" + "':\n'".join([a for a in b if a[-1]=='1']) + "'"

