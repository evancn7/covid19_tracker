#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime
import pandas as pd
import sys


# set up the variables
src = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_Republic_of_Ireland'
filename = 'data/covid_data.csv'

# scrape content from the wikipedia website
def get_soup(url):
	request = requests.get(url)
	soup = BeautifulSoup(request.content, 'html.parser')
	return soup


# create a function to remove unwanted chars from figures
def process_data(figure):
	bad_chars = {10: '', 44: ''}
	translate = figure.translate(bad_chars)
	result = translate.strip()
	return result


#get the data from the wikipedia soup
def get_data(soup):
	infobox = soup.find(attrs='infobox')
	data = infobox.find_all('tr')[8:12]
	cases, active_cases, recovered, deaths = data
	data_list = [str(datetime.now())[:19], process_data(cases.find('td').text.split()[0]),
		process_data(recovered.find('td').text.split()[0]),
		process_data(deaths.find('td').text.split()[0])]
	headers = ['run_date', cases.find('th').text, recovered.find('th').text, deaths.find('th').text]
	return data_list, headers


# store the data in a csv file
def to_csv(data, filename):
	with open(filename,'a', newline='') as file:
		writer = csv.writer(file)
		if os.path.getsize(filename) == 0:
			writer.writerow(data[1])
		writer.writerow(data[0])


def present_data(filename):
	data = pd.read_csv(filename)
	prev_data = data.iloc[-2]
	current_data = data.iloc[-1]

	print(
		f"""\nInformation gathered on {str(datetime.now())[:-7]}\n
Total Cases: {current_data['Confirmed cases']} +{int(current_data['Confirmed cases']) - int(prev_data['Confirmed cases'])}
Total Recovered: {current_data['Recovered']} +{int(current_data['Recovered']) - int(prev_data['Recovered'])}
Total Deaths: {current_data['Deaths']} +{int(current_data['Deaths']) - int(prev_data['Deaths'])}"""
)

to_csv(get_data(get_soup(src)), filename)

try:
	if sys.argv[1] == '-s':
		present_data(filename)
except:
	print('finished')
