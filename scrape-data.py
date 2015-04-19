#!/usr/bin/python

import requests
import sys
import bs4
from time import sleep
import pprint

'''
Some example urls
# 100% US Stock market
url='http://www.portfoliovisualizer.com/backtest-asset-class-allocation?s=y&mode=2&annualOperation=1&endYear=2013&initialAmount=15000&portfolio3=Custom&portfolio2=Custom&portfolio1=Custom&TotalStockMarket1=100&annualAdjustment=15000&startYear=1972'

# initial=500k, 30% Large cap value, 70% Small cap value
url='http://www.portfoliovisualizer.com/backtest-asset-class-allocation?s=y&SmallCapValue1=70&mode=2&LargeCapValue1=30&annualOperation=1&endYear=2013&initialAmount=500000&portfolio3=Custom&portfolio2=Custom&portfolio1=Custom&annualAdjustment=15000&startYear=1972'

# 15% Large cap value, 50% Small cap value, 25% LT bond, 10% TIPS
#url='http://www.portfoliovisualizer.com/backtest-asset-class-allocation?s=y&SmallCapValue1=50&TIPS1=10&mode=2&LargeCapValue1=15&annualOperation=1&endYear=2013&LongTermBond1=25&initialAmount=15000&portfolio3=Custom&portfolio2=Custom&portfolio1=Custom&annualAdjustment=15000&startYear=1972'
'''

# run scrape-classes.py to get all the portfolio classes
portfolio = {
    'LargeCapValue1': 10,
    'SmallCapValue1': 10,
    'IntlStockMarket1': 10,
    'IntlValue1': 10,
    'REIT1': 10,
    'EmergingMarket1':10,
    'TIPS1': 10,
    'LongTermBond1': 10,
    'Gold1':10,
    'Commodities1':10
}

model = {
    'annualOperation': 1,
    'startYear': 1972,      # will be replaced
    'endYear': 2013,        # will be replaced
    'initialAmount': 100000,
    'portfolio3': 'Custom',
    'portfolio2': 'Custom',
    'portfolio1': 'Custom',
    'annualAdjustment': 18000
}

tot_years = 15
print "Analying this portfolio over %d years" % (tot_years)
pprint.pprint(portfolio)

url = 'http://www.portfoliovisualizer.com/backtest-asset-class-allocation?s=y'
url += "".join(['&%s=%s' % (a, str(model[a])) for a in model])
url += "".join(['&%s=%s' % (a, str(portfolio[a])) for a in portfolio])
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text)

# Sweep start and end year based on given portfolio

header_flag = True
sys.stderr.write('Base URL:\n' + url + '\n')
for start_year in range(1972, 2014):
    sleep(1)
    end_year = start_year + tot_years - 1
    if end_year > 2014:
        break
    
    response = requests.get(url.replace('1972', str(start_year)).replace('2013', str(end_year)))
    soup = bs4.BeautifulSoup(response.text)

    if header_flag:
        header_flag = False
        line = soup.find(id='growthChart').find_all("table")[1].find_all("th")
        # Write the header line from the first row in the table
        header_str = 'start_year|end_year|' + "|".join([a.text for a in line])
        #sys.stdout.write(header_str)
        print header_str

    out_str = str(start_year) + '|' + str(end_year) + '|' 
    line = soup.find(id='growthChart').find_all("table")[1].find("tbody").find_all("td")
    out_str += "|".join([a.text.strip().replace('\n','').split('    ')[0] for a in line])
    print out_str

