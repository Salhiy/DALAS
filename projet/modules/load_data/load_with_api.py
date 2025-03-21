import requests
import pandas as pd
from io import StringIO
from utils import *

"""
	les id des 30 entreprise qui vont 
	nous permettre de charger les données bouriseres
"""

'''
MMM: 3M Company
AXP: American Express Company
AMGN: Amgen Inc.
AAPL: Apple Inc.
BA: The Boeing Company
CAT: Caterpillar Inc.
CVX: Chevron Corporation
CSCO: Cisco Systems, Inc.
KO: The Coca-Cola Company
DOW: Dow Inc.
GS: The Goldman Sachs Group, Inc.
HD: The Home Depot, Inc.
HON: Honeywell International Inc.
IBM: International Business Machines Corporation
INTC: Intel Corporation
JNJ: Johnson & Johnson
JPM: JPMorgan Chase & Co.
MCD: McDonald's Corporation
MRK: Merck & Co., Inc.
MSFT: Microsoft Corporation
NKE: NIKE, Inc.
PG: The Procter & Gamble Company
CRM: salesforce.com, inc.
TRV: The Travelers Companies, Inc.
UNH: UnitedHealth Group Incorporated
VZ: Verizon Communications Inc.
V: Visa Inc.
WBA: Walgreens Boots Alliance, Inc.
WMT: Walmart Inc.
DIS: The Walt Disney Company
'''
dow_30_tickers = [
    "MMM", "AXP", "AMGN", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DOW",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK", "MSFT",
    "NKE", "PG", "CRM", "TRV", "UNH", "VZ", "V", "WBA", "WMT", "DIS"
]

name = {
	'MMM': '3M Company',
	'AXP': 'American Express Company',
	'AMGN': 'Amgen Inc.',
	'AAPL': 'Apple Inc.',
	'BA': 'The Boeing Company',
	'CAT': 'Caterpillar Inc.',
	'CVX': 'Chevron Corporation',
	'CSCO': 'Cisco Systems, Inc.',
	'KO': 'The Coca-Cola Company',
	'DOW': 'Dow Inc.',
	'GS': 'The Goldman Sachs Group, Inc.',
	'HD': 'The Home Depot, Inc.',
	'HON': 'Honeywell International Inc.',
	'IBM': 'International Business Machines Corporation',
	'INTC': 'Intel Corporation',
	'JNJ': 'Johnson & Johnson',
	'JPM': 'JPMorgan Chase & Co.',
	'MCD': 'McDonald\'s Corporation',
	'MRK': 'Merck & Co., Inc.',
	'MSFT': 'Microsoft Corporation',
	'NKE': 'NIKE, Inc.',
	'PG': 'The Procter & Gamble Company',
	'CRM': 'salesforce.com, inc.',
	'TRV': 'The Travelers Companies, Inc.',
	'UNH': 'UnitedHealth Group Incorporated',
	'VZ': 'Verizon Communications Inc.',
	'V': 'Visa Inc.',
	'WBA': 'Walgreens Boots Alliance, Inc.',
	'WMT': 'Walmart Inc.',
	'DIS': 'The Walt Disney Company'
}

start_date = '01-01-2010'
end_date = '01-01-2023'

def load_from_api(verbose=False):
	df = pd.DataFrame()
	for ticker in dow_30_tickers:
		url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={convert_to_unix(start_date)}&period2={convert_to_unix(end_date)}&interval=1d&events=history"
		if (verbose):
			print(f"Envoie d'une requete api sur le lien : {url}")
		response = requests.get(url, headers = {'User-agent': 'your bot 0.1'})
		df_csv = pd.read_csv(StringIO(response.text))
		df_csv['Libellé'] = name[ticker]
		df = pd.concat([df_csv, df])
	return df.sample(frac=1)