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
import time
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, LabelBinarizer
from sklearn.metrics import roc_curve, roc_auc_score

# Function to get the raw HTML soups from all 500 web pages


def get_soups(website_number):
    get_url = requests.get('https://www.truecar.com/used-cars-for-sale/listings/?page=' + str(website_number))
    return BeautifulSoup(get_url.content, 'lxml')


soups = list(map(get_soups, list(range(1, 501))))

# URLs scraping
fst_page_urls = np.array([])


for ind in range(33):
    finding = soups[0].find_all('a', {'data-test': 'usedListing'})[ind]
    fst_page_urls = np.append(fst_page_urls, re.findall('href=".+" style', str(finding)[:280]))


def urls_scraper(soup):

    def urlsxpage(nth):
        finding = soup.find_all('a', {'data-test': 'usedListing'})[nth]
        return re.findall('href="/.+" style', str(finding)[:280])[0]
    nth_urls = list(map(urlsxpage, list(range(30))))
    return nth_urls


rest_urls_list = list(map(urls_scraper, soups[1:]))
rest_pages_urls = np.array(rest_urls_list).flatten()
all_urls = np.append(fst_page_urls, rest_pages_urls)
url_formatter = np.vectorize(lambda url: 'https://truecar.com' + url[6: -7])
urls = url_formatter(all_urls)

# Main part of vehicles features scraping


def scraper(feature_as_argument):
    def feature_from_url(url):
        nth_request = requests.get(url)
        nth_soup = BeautifulSoup(nth_request.content, 'lxml')
        nth_search = re.search(feature_as_argument + '</h4><ul><li>.+</li', str(nth_soup))
        try:
            return re.findall('li>.+</l', str(nth_search))[0][3: -3]
        except:
            return np.NaN

    return list(map(feature_from_url, urls))


drive_types = scraper('Drive Type')
fuel_types = scraper('Fuel Type')
mileages = scraper('Mileage')
transmissions = scraper('Transmission')
MPGs = scraper('MPG')
styles = scraper('Style')
options_levels = scraper('Options Level')
bed_lengths = scraper('Bed Length')
engines = scraper('Engine')
exterior_colors = scraper('Exterior Color')
interior_colors = scraper('Interior Color')

# Vehicles years, makes and models scraping


def ymm_scraper(index):
    def feature_from_url(url):
        nth_request = requests.get(url)
        nth_soup = BeautifulSoup(nth_request.content, 'lxml')
        nth_finding = nth_soup.find_all('div', {'class': 'text-truncate heading-3 margin-right-2 margin-right-sm-3'})
        try:
            if index == 2:
                return re.findall('>.+<', str(nth_finding))[0][1: -1].split()[2:]
            else:
                return re.findall('>.+<', str(nth_finding))[0][1: -1].split()[index]
        except:
            return np.NaN

    return list(map(feature_from_url, urls))


years = ymm_scraper(0)
makes = ymm_scraper(1)
models = ymm_scraper(2)

# Vehicles prices scraping


def prices_scraper(url):
    nth_request = requests.get(url).content
    nth_soup = BeautifulSoup(nth_request, 'lxml').find_all('div', {'data-qa': 'LabelBlock-text'})
    try:
        return re.findall('[0-9]+,[0-9]+', str(nth_soup))[0]
    except:
        return np.NaN


prices = list(map(prices_scraper, urls))

# Vehicles locations (cities and states) scraping


def cities_scraper(url):
    nth_request = requests.get(url).content
    nth_soup = BeautifulSoup(nth_request, 'lxml').find_all('span', {'data-qa': 'used-vdp-header-location'})
    try:
        return re.findall('">.+<!', str(nth_soup))[0][2: -12]
    except:
        return np.NaN


def states_scraper(url):
    nth_request = requests.get(url).content
    nth_soup = BeautifulSoup(nth_request, 'lxml').find_all('span', {'data-qa': 'used-vdp-header-location'})
    try:
        return re.findall('[A-W][A-Z]', str(nth_soup))[0]
    except:
        return np.NaN


cities = list(map(cities_scraper, urls))
states = list(map(states_scraper, urls))

# Vehicles conditions scraping


def conditions_scraper(url):
    nth_request = requests.get(url).content
    nth_soup = BeautifulSoup(nth_request, 'lxml').find_all('li', {'class': '_h9wfdq'})
    try:
        return re.findall('">[0-9]<!', str(nth_soup[0]))[0][2: -2] + re.findall('->.+</l', str(nth_soup[0]))[0][2: -3]
    except:
        return np.NaN


conditions = list(map(conditions_scraper, urls))

# Building the dataset
features = {
    'Make': makes, 'Model': models, 'Year': years, 'Mileage': mileages, 'Transmission': transmissions,
    'Engine': engines, 'Exterior Color': exterior_colors, 'Interior Color': interior_colors,
    'MPG': MPGs, 'Fuel Type': fuel_types, 'Drive Type': drive_types, 'Location (City)': cities,
    'Location (State)': states, 'Style': styles, 'Condition (Accidents)': conditions,
    'Options Level': options_levels, 'Bed Length': bed_lengths, 'Price': prices
}
vehicles_data = pd.DataFrame(features)
