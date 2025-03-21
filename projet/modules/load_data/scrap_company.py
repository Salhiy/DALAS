"""
	scraper l'historique de chaque entreprise, pour voir l'eveololution des actions
	cela prends en moyenne 43 secondes sur ma machine
"""
import bs4
import lxml
import pandas as pd
import urllib
from urllib import request
import numpy as np 
from utils import *
import threading
import queue


#pour recuperer le volume d'echange de cette entreprise a une certaine date
def get_volume_per_date(code, date, verbose=False, L=[]):
	link = f'https://www.boursorama.com/_formulaire-date?symbol={code}&dateHistoric={date}'
	if (verbose) :
		print(f'lecture du lien {link}')
	request_data = request.urlopen(link).read()
	page = bs4.BeautifulSoup(request_data, "lxml")
	try:
		L.append(float(format_string(page.find("tbody").find_all("td")[2].get_text())))
	except Exception:
		L.append(np.nan)
	
def run(libelle, code, date, verbose, L, Q):
	get_volume_per_date(code, date, verbose, L)
	L.append(libelle)#ajout de la libellé de l'entreprise pour ensuite faire des tests
	Q.put(np.array([L]))

#get the history of a compagny (code) with in the duration
def get_history_per_page(libelle, code, duration, Q_, page=1, verbose=False):
	link = f'https://www.boursorama.com/_formulaire-periode/page-{page}?symbol={code}&historic_search%5BstartDate%5D=&historic_search%5Bduration%5D={duration}M&historic_search%5Bperiod%5D=2'
	if (verbose):
		print(f'lecture du lien {link}')
	request_data = request.urlopen(link).read()
	page = bs4.BeautifulSoup(request_data, "lxml")
	
	history_table = page.find('table')

	columns = [title.get_text().strip() for title in history_table.find('thead').find_all("th")]
	columns.append("Volume")
	columns.append("Libellé")

	arr = np.empty(shape=(0, len(columns)), dtype=object)

	body = history_table.find('tbody').find_all('tr')

	threads = []
	Q = queue.Queue()

	#envoie des requetes en parallele
	for ligne in body:
		column_list = []
		for column in ligne.find_all('td'):
			column_list.append(format_string(column.get_text()))
		date = column_list[0]
		column_list[0] = format_date(column_list[0])
		thread = threading.Thread(target=run, args=(libelle, code, url_date(date), verbose, column_list, Q))
		thread.start()
		threads.append(thread)

	for thread in threads:
		thread.join()

	while not Q.empty():
		arr = np.append(arr, Q.get(), axis=0)

	Q_.put(pd.DataFrame(arr, columns=columns))

#recupere l'historique de l'entreprise sur la duree en mois
def get_history(libelle, code, duration, verbose=False):
	if (duration > 1):
		#on recupere le nombre de page
		link = f'https://www.boursorama.com/_formulaire-periode/?symbol={code}&historic_search%5BstartDate%5D=&historic_search%5Bduration%5D={duration}M&historic_search%5Bperiod%5D=2'
		request_data = request.urlopen(link).read()
		p = bs4.BeautifulSoup(request_data, "lxml")

		pages = [a.find("span").get_text() for a in p.find('div', attrs={'role':'navigation'}).find_all('a')]
	else:
		pages = [1]

	df = pd.DataFrame()
	threads = []
	Q = queue.Queue()

	for page in pages:
		thread = threading.Thread(target=get_history_per_page, args=(libelle, code, duration, Q, int(page), verbose))
		thread.start()
		threads.append(thread)
		
	for thread in threads:
		thread.join()

	while not Q.empty():
		df = pd.concat([df, Q.get()])

	return df