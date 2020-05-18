import itertools
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


# VEHICLES PRICES SCRAPING FROM WEB PAGE LISTINGS

# Function to get the raw HTML soups from all 600 web pages


def get_soups(website_number):
    get_url = requests.get('https://www.truecar.com/used-cars-for-sale/listings/?page=' + str(website_number))
    return BeautifulSoup(get_url.content, 'lxml')


soups = list(map(get_soups, list(range(1, 600))))

# Function to scrape the vehicles prices for each web page


def prices_scraper(soup):
    nth_page_prices_soup = soup.find_all('h4', {'data-test': 'vehicleCardPricingBlockPrice'})
    nth_page_prices = re.findall('[0-9]+,[0-9]+', str(nth_page_prices_soup))
    return nth_page_prices


prices = list(map(prices_scraper, soups))
prices = str(prices).replace('[', '').replace(']', '').split(', ')
prices = list(map(lambda x: x[1:-1], prices))


# VEHICLES YEARS SCRAPING FROM WEB PAGE LISTINGS

# Function to scrape a feature from each soup and return the features list


def scraper(tag, element, element_description, regex):
    def features_scraper(soup):
        nth_page_features_soup = soup.find_all(tag, {element: element_description})
        nth_page_features = re.findall(regex, str(nth_page_features_soup))
        return nth_page_features
    features = list(map(features_scraper, soups))
    features = str(features).replace('[', '').replace(']', '').split(', ')
    features = list(map(lambda x: x[1: -1], features))
    return features


years = scraper('span', 'class', 'vehicle-card-year', '[12][0-9]{3}')


# VEHICLES LOCATIONS STATES SCRAPING FROM WEB PAGE LISTINGS

states = scraper('div', 'data-test', 'vehicleCardLocation', '[A-Z]{2}')

# VEHICLES LOCATIONS CITIES SCRAPING FROM WEB PAGE LISTINGS

cities_unf = scraper('div', 'data-test', 'vehicleCardLocation', '[A-Z][a-z]+[. ]*[A-Z]*[a-z]*[. ]*[A-Z]*[a-z]*')
cities = [city for city in cities_unf if cities_unf.index(city) in list(range(3, len(cities_unf), 4))]

# VEHICLES EXTERIOR COLORS SCRAPING FROM WEB PAGE LISTINGS

exterior_colors_unf = scraper('div', 'data-test', 'vehicleCardColors', 'g>[A-Z][a-z]+')
exterior_colors = list(map(lambda color: color[2:], exterior_colors_unf))

# VEHICLES INTERIOR COLORS SCRAPING FROM WEB PAGE LISTINGS

interior_colors_unf = scraper('div', 'data-test', 'vehicleCardColors', '->[A-Z][a-z]+')
interior_colors = list(map(lambda color: color[2:], interior_colors_unf))

# VEHICLES CONDITION (NUMBER OF ACCIDENTS) SCRAPING FROM WEB PAGE LISTINGS

accidents = scraper('div', 'data-test', 'vehicleCardCondition', '[0-9]*[A-z]* accident[s]*')

# VEHICLES MILEAGES SCRAPING FROM WEB PAGES LISTINGS

fst_page_urls = np.array([])


for ind in range(33):
    finding = soups[0].find_all('a', {'data-test': 'usedListing'})[ind]
    fst_page_urls = np.append(fst_page_urls, re.findall('href=".+" style', str(finding)[:280]))


def urls_scraper(soup):
    nth_urls = []

    for nth in range(30):
        finding = soup.find_all('a', {'data-test': 'usedListing'})[nth]
        nth_urls.append(re.findall('href="/.+" style', str(finding)[:280])[0])

    return nth_urls


rest_urls_list = list(map(urls_scraper, soups[1:]))
rest_pages_urls = np.array(rest_urls_list).flatten()
all_urls = np.append(fst_page_urls, rest_pages_urls)
url_formatter = np.vectorize(lambda url: 'https://truecar.com' + url[6: -7])
urls = url_formatter(all_urls)


# VEHICLES STYLES SCRAPING FROM WEB PAGES LISTINGS

def feature_scraper_from_url(feature_as_argument):
    def feature_from_url(url):
        nth_request = requests.get(url)
        nth_soup = BeautifulSoup(nth_request.content, 'lxml')
        nth_search = re.search(feature_as_argument + '</h4><ul><li>.+</li', str(nth_soup))
        return re.findall('li>.+</l', str(nth_search))
    features_unf = list(map(feature_from_url, urls[:10]))
    features = list(map(lambda f: str(f)[5: -5], features_unf))
    return features


styles = feature_scraper_from_url('Style')


# VEHICLE OPTIONS LEVELS SCRAPING FROM WEB PAGES LISTINGS

options_level = feature_scraper_from_url('Options Level')


# VEHICLE BED LENGTHS SCRAPING FROM WEB PAGES LISTINGS

bed_lengths = feature_scraper_from_url('Bed Length')


# VEHICLE MILEAGES PER GALLON SCRAPING FROM WEB PAGES LISTINGS

MPGs = feature_scraper_from_url('MPG')


# VEHICLES DRIVE TYPES SCRAPING FROM WEB PAGES LISTINGS

drive_types = feature_scraper_from_url('Drive Type')


# VEHICLE FUEL TYPES SCRAPING FROM WEB PAGES LISTINGS

fuel_types = feature_scraper_from_url('Fuel Type')


# VEHICLE TRANSMISSIONS SCRAPING FROM WEB PAGES LISTINGS

transmissions = feature_scraper_from_url('Transmission')


# VEHICLE MILEAGES SCRAPING FROM WEB PAGES LISTINGS

mileages = feature_scraper_from_url('Mileage')


# VEHICLE ENGINES SCRAPING FROM WEB PAGES LISTINGS

