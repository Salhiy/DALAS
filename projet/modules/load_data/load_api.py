import requests
import pandas as pd
from io import StringIO
from utils import *

"""
	les id des 30 entreprise qui vont 
	nous permettre de charger les données bouriseres
"""
dow_30_tickers = [
    "MMM", "AXP", "AMGN", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DOW",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK", "MSFT",
    "NKE", "PG", "CRM", "TRV", "UNH", "VZ", "V", "WBA", "WMT", "DIS"
]

start_date = '01-01-2022'
end_date = '01-01-2023'

def load_from_api():
	df = pd.DataFrame()
	for ticker in dow_30_tickers:
		url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={convert_to_unix(start_date)}&period2={convert_to_unix(end_date)}&interval=1d&events=history"
		response = requests.get(url, headers = {'User-agent': 'your bot 0.1'})
		df_csv = pd.read_csv(StringIO(response.text))
		df_csv['LIBELLÉ'] = ticker
		df = pd.concat([df_csv, df])
	return df.sample(frac=1)