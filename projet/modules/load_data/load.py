"""
fichier qui permet de charger les données : 
	- par du scrapping, principalement via le site de boursorama
	- par l'API de yahoo
	- par des données CSV 
	les données proviennent de la bourse francaise : cac40..
	et de la bourse americaine : apple, google....
"""
from datetime import datetime
from scrap_cotations import *
from load_with_api import *
from scrap_company import *
import pandas as pd
import threading
import queue

#nombre de mois max a scrappé
MAX_DURATION = 1

#pretraimemnt sur les données de bourse francaise pour macher avec les données
#de bourse amercaine
def normalize(df, columns, drop):
	df = df.drop(drop, axis=1)
	if (not 'Date' in df.columns):
		df['Date'] = datetime.now().strftime('%Y-%m-%d')
	#renomage des colones
	df = df.rename(columns=columns)
	return df

#retourne le dataframe qui fusionne entre toutes les sources
def load_data(verbose):

	def run(Q, libelle, code, verbose):
		Q.put(normalize(get_history(libelle, code, MAX_DURATION, verbose=verbose), 
			{'Dernier':'Adj Close', '+ haut':'High', '+ bas':'Low', 'Ouverture':'Open'}, 
			['Var. %']
		))

	#on recupere les données des plus grandes entreprise francaise d'abord
	cotations = get_cotations(verbose)

	#normalisation des colones
	cotations = normalize(cotations, 
		{'Ouv':'Open', '+Haut':'High', '+Bas':'Low', 'Vol.':'Volume', 'Dernier':'Adj Close'}, 
		['Var.', 'Var/1Janv']
	)

	#recuparion de l'historique de chaque entreprise sur les 10 derniers mois
	history = pd.DataFrame()
	threads = []
	Q = queue.Queue()

	for index, c in cotations.iterrows():
		if (verbose):
			print(f"Getting history of {c['code']}")
		thread = threading.Thread(target=run, args=(Q, c['Libellé'], c['code'], verbose))
		thread.start()
		threads.append(thread)
	
	for thread in threads:
		thread.join()

	while not Q.empty():
		history = pd.concat([history, Q.get()])
	
	api_data = load_from_api(verbose)
	csv = pd.read_csv("../../csv/bourse.csv")
	csv['Libellé'] = 'BTC'
	df = pd.concat([cotations, history])#merge history and cotations
	df = pd.concat([df, csv])#merge with csv data
	df = pd.concat([df, api_data])#merge with api data
	df['Volume'] = df['Volume'].astype(np.float64)
	df['Open'] = df['Open'].astype(np.float64)
	df['High'] = df['High'].astype(np.float64)
	df['Low'] = df['Low'].astype(np.float64)
	df['Adj Close'] = df['Adj Close'].astype(np.float64)
	df = df.drop(['Close', 'code'], axis=1)
	return df

#load data 
df = load_data(verbose=True)
df.to_excel("../../data.xlsx", index=False)