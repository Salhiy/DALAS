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

MAX_DURATION = 10

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
def load_data():
	#on recupere les données des plus grandes entreprise francaise d'abord
	cotations = get_cotations()

	#normalisation des colones
	cotations = normalize(cotations, 
		{'Ouv':'Open', '+Haut':'High', '+Bas':'Low', 'Vol.':'Volume', 'Dernier':'Close'}, 
		['Libellé', 'Var.', 'Var/1Janv']
	)


	#recuparion de l'historique de chaque entreprise sur les 10 derniers mois
	history = pd.DataFrame()
	for code in cotations['code']:
		tmp = normalize(get_history(code, MAX_DURATION), 
			{'Dernier':'Close', '+ haut':'High', '+ bas':'Low', 'Ouverture':'Open'}, 
			['Var. %'])
		print(tmp)

		#pd.concat([history, normalize(tmp)])
	print(cotations)

load_data()