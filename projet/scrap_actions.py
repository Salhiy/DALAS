import bs4
import lxml
import pandas as pd
import urllib
from urllib import request
import numpy as np 
import re


#pour recuperer les liens de toutes les pages, car les données peuvent etre sur plusieurs pages
def liens_pages():
	cotations = 'https://www.boursorama.com/bourse/actions/cotations/'

	request_data = request.urlopen(cotations).read()
	page = bs4.BeautifulSoup(request_data, "lxml")

	liens_pages = page.find('div', attrs={'role':'navigation'}).find_all('a')
	
	res = []

	for lien in liens_pages:
		res.append("https://www.boursorama.com" + (lien.get('href')))

	return res

#lit la page des action et recupere les informations dans un dataframe
def lire_page_actions(lien):
	request_data = request.urlopen(lien).read()
	page = bs4.BeautifulSoup(request_data, "lxml")

	#recuperations des differentes actions du marché francais les plus recentes
	actions = page.find('div', class_='u-relative').find('table')

	#recuperer toutes les lignes de la table
	lignes = actions.find_all('tr')

	#recuperation du titre de la table
	columns = [titre.get_text().strip() for titre in lignes[0].find_all('th')]

	#np array pour sauvgarder les valeurs temporerement
	arr = np.empty(shape=(0, 8), dtype=object) 

	for ligne in lignes[1:]:
		#recuperations des colones
		colones = ligne.find_all('td')
		colone_list = []
		for index, colone in enumerate(colones):
			if (index == 0):
				colone = colone.find('a')
				colone_list.append(colone.get_text().strip())
			else:
				formated_string = re.sub(r"[^\d.-]", "", colone.get_text().strip())
				formated_string = re.sub(r"\s", "", formated_string)
				colone_list.append(float(formated_string))
		arr = np.append(arr, np.array([colone_list]), axis=0)

	#data frame des actions et leurs valeurs
	return pd.DataFrame(arr, columns=columns)

def scrap_page_action():
	liens = liens_pages()
	df = pd.DataFrame()
	for lien in liens:
		print(lien)
		df = pd.concat([df, lire_page_actions(lien)])
	return df