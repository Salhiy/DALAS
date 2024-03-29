"""
	scraper l'historique de chaque entreprise, pour voir l'eveololution des actions
"""
import bs4
import lxml
import pandas as pd
import urllib
from urllib import request
import numpy as np 
from utils import *

#pour recuperer le volume d'echange de cette entreprise a une certaine date
def get_volume_per_date(code, date, verbose=False):
	link = f'https://www.boursorama.com/_formulaire-date?symbol={code}&dateHistoric={date}'
	if (verbose) :
		print(f'lecture du lien {link}')
	request_data = request.urlopen(link).read()
	page = bs4.BeautifulSoup(request_data, "lxml")
	try:
		return int(format_string(page.find("tbody").find_all("td")[2].get_text()))
	except Exception:
		return 0 #pas de volume
		

#get the history of a compagny (code) with in the duration
def get_history_per_page(code, duration, page=1, verbose=False):
	link = f'https://www.boursorama.com/_formulaire-periode/page-{page}?symbol={code}&historic_search%5BstartDate%5D=&historic_search%5Bduration%5D={duration}M&historic_search%5Bperiod%5D=2'
	if (verbose):
		print(f'lecture du lien {link}')
	request_data = request.urlopen(link).read()
	page = bs4.BeautifulSoup(request_data, "lxml")
	
	history_table = page.find('table')

	columns = [title.get_text().strip() for title in history_table.find('thead').find_all("th")]
	columns.append("Volume")

	arr = np.empty(shape=(0, len(columns)), dtype=object)

	body = history_table.find('tbody').find_all('tr')

	for ligne in body:
		column_list = []
		for column in ligne.find_all('td'):
			column_list.append(format_string(column.get_text()))
		column_list.append(get_volume_per_date(code, format_date(column_list[0]), verbose))
		arr = np.append(arr, np.array([column_list]), axis=0)

	return pd.DataFrame(arr, columns=columns)

#recupere l'historique de l'entreprise sur la duree en mois
def get_history(code, duration, verbose=False):
	if (duration <= 1):
		return get_history_per_page(code, duration, 1)

	#on recupere le nombre de page
	link = f'https://www.boursorama.com/_formulaire-periode/?symbol={code}&historic_search%5BstartDate%5D=&historic_search%5Bduration%5D={duration}M&historic_search%5Bperiod%5D=2'
	request_data = request.urlopen(link).read()
	p = bs4.BeautifulSoup(request_data, "lxml")

	pages = [a.find("span").get_text() for a in p.find('div', attrs={'role':'navigation'}).find_all('a')]
	df = pd.DataFrame()

	for page in pages:
		df = pd.concat([df, get_history_per_page(code, duration, int(page), verbose)])

	return df