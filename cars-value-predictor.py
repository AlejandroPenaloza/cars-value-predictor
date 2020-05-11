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


# 'VEHICLES PRICES SCRAPING FROM WEB PAGE LISTINGS'

# 'Function to get the raw HTML soups from all 600 web pages'


def get_soups(website_number):
    get_url = requests.get('https://www.truecar.com/used-cars-for-sale/listings/?page=' + str(website_number))
    return BeautifulSoup(get_url.content, 'lxml')


soups = list(map(get_soups, list(range(1, 600))))

# 'Function to scrape the vehicles prices for each web page'


def prices_scraper(soup):
    nth_page_prices_soup = soup.find_all('h4', {'data-test': 'vehicleCardPricingBlockPrice'})
    nth_page_prices = re.findall('[0-9]+,[0-9]+', str(nth_page_prices_soup))
    return nth_page_prices


prices = list(map(prices_scraper, soups))
prices = str(prices).replace('[', '').replace(']', '').split(', ')
prices = list(map(lambda x: x[1:-1], prices))


# 'CARS YEARS SCRAPING FROM WEB PAGE LISTINGS'

# Function to scrape a feature from each soup and return the features list


def scraper(tag, element, element_description, regex):
    def featuresscraper(soup):
        nth_page_features_soup = soup.find_all(tag, {element: element_description})
        nth_page_features = re.findall(regex, str(nth_page_features_soup))
        return nth_page_features
    features = list(map(featuresscraper, soups))
    features = str(features).replace('[', '').replace(']', '').split(', ')
    features = list(map(lambda x: x[1: -1], features))
    return features

years = scraper('span', 'class', 'vehicle-card-year', '[12][0-9]{3}')

# 'CARS MILEAGES SCRAPING FROM WEB PAGES LISTINGS'

mileages_unf = scraper('div', 'class', 'font-size-1 text-truncate', 'g>[0-9]*,[0-9]+')
mileages = list(map(lambda mileage: mileage[2:], mileages_unf))

# 'CARS LOCATIONS STATES SCRAPING FROM WEB PAGE LISTINGS'

states = scraper('div', 'data-test', 'vehicleCardLocation', '[A-Z]{2}')

# 'CARS LOCATIONS CITIES SCRAPING FROM WEB PAGE LISTINGS'

cities_unf = scraper('div', 'data-test', 'vehicleCardLocation', '[A-Z][a-z]+[. ]*[A-Z]*[a-z]*[. ]*[A-Z]*[a-z]*')
cities = [city for city in cities_unf if cities_unf.index(city) in list(range(3, len(cities_unf), 4))]

# 'CARS EXTERIOR COLORS SCRAPING FROM WEB PAGE LISTINGS'

exterior_colors_unf = scraper('div', 'data-test', 'vehicleCardColors', 'g>[A-Z][a-z]+')
exterior_colors = list(map(lambda color: color[2:], exterior_colors_unf))

# 'CARS INTERIOR COLORS SCRAPING FROM WEB PAGE LISTINGS'

interior_colors_unf = scraper('div', 'data-test', 'vehicleCardColors', '->[A-Z][a-z]+')
interior_colors = list(map(lambda color: color[2:], interior_colors_unf))

# 'CARS CONDITION (NUMBER OF ACCIDENTS) SCRAPING FROM WEB PAGE LISTINGS'

accidents = scraper('div', 'data-test', 'vehicleCardCondition', '[0-9]*[A-z]* accident[s]*')
