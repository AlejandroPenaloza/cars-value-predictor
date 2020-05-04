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




#YEARS SCRAPING

fst_page_listings_years = fst_page_listings_soup.find_all('span', {'class': 'vehicle-card-year'})
fst_page_years = list(re.findall('[12][0-9]{3}', str(fst_page_listings_years)))


def pageyears(number):
    nth_page_listings_soup = BeautifulSoup(requests.get('https://www.truecar.com/used-cars-for-sale/listings/?page=' + str(number)).content, 'lxml')
    nth_page_listings = nth_page_listings_soup.find_all('span', {'class': 'vehicle-card-year'})
    nth_page_years = list(re.findall('[12][0-9]{3}', str(nth_page_listings)))
    return nth_page_years


rest_page_years1 = []
rest_page_years2 = []
rest_page_years3 = []

#Splitting in three loops had to be done in order to speed up the process.
for number_of_page in range(2, 180):
    rest_page_years1 += pageyears(number_of_page)


for number_of_page in range(180, 360):
    rest_page_years2 += pageyears(number_of_page)


for number_of_page in range(360, 540):
    rest_page_years3 += pageyears(number_of_page)


years = fst_page_years + rest_page_years1 + rest_page_years2 + rest_page_years3



