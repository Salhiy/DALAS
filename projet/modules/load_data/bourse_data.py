"""
	fichier qui permet de faire la fusion entre toute les sources de données :
		API, Site web, CSV
	fusion entre toutes les sources de données.
"""

import pandas as pd
from utils import *

def load_df():
	#load the csv
	df = pd.read_csv('/'.join([get_abs_path("../.."), 'csv/bourse.csv']))

	print(df)

load_df()