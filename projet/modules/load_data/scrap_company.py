import bs4
import lxml
import pandas as pd
import urllib
from urllib import request
import numpy as np 
from utils import *


#get the history of a compagny (code) with in the duration
def get_history_per_page(code, duration, page=1):
	link = f'https://www.boursorama.com/_formulaire-periode/page-{page}?symbol={code}&historic_search%5BstartDate%5D=&historic_search%5Bduration%5D={duration}M&historic_search%5Bperiod%5D=2'
	request_data = request.urlopen(link).read()
	page = bs4.BeautifulSoup(request_data, "lxml")
	
	history_table = page.find('table') 

	columns = [title.get_text().strip() for title in history_table.find('thead').find_all("th")]
	
	arr = np.empty(shape=(0, len(columns)), dtype=object)

	body = history_table.find('tbody').find_all('tr')

	for ligne in body:
		column_list = []
		for column in ligne.find_all('td'):
			column_list.append(format_string(column.get_text()))
		arr = np.append(arr, np.array([column_list]), axis=0)

	return pd.DataFrame(arr, columns=columns)

#recupere l'historique de l'entreprise sur la duree en mois
def get_history(code, duration):
	if (duration <= 1):
		return get_history_per_page(code, duration, 1)

	#on recupere le nombre de page
	link = f'https://www.boursorama.com/_formulaire-periode/?symbol={code}&historic_search%5BstartDate%5D=&historic_search%5Bduration%5D={duration}M&historic_search%5Bperiod%5D=2'
	request_data = request.urlopen(link).read()
	p = bs4.BeautifulSoup(request_data, "lxml")

	pages = [a.find("span").get_text() for a in p.find('div', attrs={'role':'navigation'}).find_all('a')]
	df = pd.DataFrame()

	for page in pages:
		df = pd.concat([df, get_history_per_page(code, duration, int(page))])

	return df