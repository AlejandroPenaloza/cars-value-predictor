import pandas as pd
import numpy as np
import scipy.stats
import re
import requests
import math
from bs4 import BeautifulSoup
import matplotlib as mlp
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg
import matplotlib.figure
import seaborn as sb
import datetime
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, LabelBinarizer
from sklearn.metrics import roc_curve, roc_auc_score


#PRICES SCRAPING

fst_page_listings_soup = BeautifulSoup(requests.get('https://www.truecar.com/used-cars-for-sale/listings/').content, 'lxml')
fst_page_prices_soup = fst_page_listings_soup.find_all('h4', {'data-test': 'vehicleCardPricingBlockPrice'})
fst_page_prices = re.findall('[0-9]+,[0-9]+', str(fst_page_prices_soup))


#Scraping rest of pages listings prices

def pricesscraper(number_of_page):
    nth_page_listings_soup = BeautifulSoup(requests.get('https://www.truecar.com/used-cars-for-sale/listings/?page=' + str(number_of_page)).content, 'lxml')
    nth_page_prices_soup = nth_page_listings_soup.find_all('h4', {'data-test': 'vehicleCardPricingBlockPrice'})
    nth_page_prices = re.findall('[0-9]+,[0-9]+', str(nth_page_prices_soup))
    return nth_page_prices


prices = list(map(pricesscraper, range(2, 600)))
prices = str(prices).replace('[', '').replace(']', '').split(', ')
prices = list(map(lambda x: x[1:-1], prices))
prices += fst_page_prices


#YEARS SCRAPING

fst_page_years_soup = fst_page_listings_soup.find_all('span', {'class': 'vehicle-card-year'})
fst_page_years = list(re.findall('[12][0-9]{3}', str(fst_page_years_soup)))


def yearsscraper(number_of_page):
    nth_page_listings_soup = BeautifulSoup(requests.get('https://www.truecar.com/used-cars-for-sale/listings/?page=' + str(number_of_page)).content, 'lxml')
    nth_page_years_soup = nth_page_listings_soup.find_all('span', {'class': 'vehicle-card-year'})
    nth_page_years = re.findall('[12][0-9]{3}', str(nth_page_years_soup))
    return nth_page_years


years = list(map(yearsscraper, range(2, 600)))
years = str(years).replace('[', '').replace(']', '').split(', ')
years = list(map(lambda x: x[1:-1], years))
years += fst_page_years


#MILEAGES SCRAPING

fst_page_listings_mileages = fst_page_listings_soup.find_all('div', {'class': 'font-size-1 text-truncate'})
fst_page_mileages_soup = re.findall('g>[0-9]*,[0-9]+', str(fst_page_listings_mileages))
fst_page_mileages = list(map(lambda mileage: mileage[2:], fst_page_mileages_soup))


def mileagesscraper(number):
    nth_page_listings_soup = BeautifulSoup(requests.get('https://www.truecar.com/used-cars-for-sale/listings/?page=' + str(number)).content, 'lxml')
    nth_page_mileages_soup = nth_page_listings_soup.find_all('div', {'class': 'font-size-1 text-truncate'})
    nth_page_mileages_unf = re.findall('g>[0-9]*,[0-9]+', str(nth_page_mileages_soup))
    nth_page_mileages = list(map(lambda mileage: mileage[2:], nth_page_mileages_unf))
    return nth_page_mileages


mileages = list(map(mileagesscraper, range(2, 600)))
mileages = str(mileages).replace('[', '').replace(']', '').split(', ')
mileages = list(map(lambda x: x[1:-1], mileages))
mileages += fst_page_mileages
