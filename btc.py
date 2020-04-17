import requests
import pandas as pd
import matplotlib.pyplot as plt

#get price from set date to current date in df
def get_historic_price(symbol, exchange='bitfinex', after='2020-03-01'):
	url = 'https://api.cryptowat.ch/markets/{exchange}/{symbol}usd/ohlc'.format(
		symbol=symbol, exchange=exchange)
	# extract data from api
	resp = requests.get(url, params={
		'periods' : '3600',
		'after' : str(int(pd.Timestamp(after).timestamp()))
		})
	# raise http error
	resp.raise_for_status()
	data = resp.json()
	# dataframe for cryptocurrency
	df = pd.DataFrame(data['result']['3600'], columns=['CloseTime', 'OpenPrice', 'HighPrice', 'LowPrice','ClosePrice','Volume', 'NA'])
	df['CloseTime'] = pd.to_datetime(df['CloseTime'], unit='s')
	df.set_index('CloseTime', inplace=True)
	return df

#set day for records
last_week = (pd.Timestamp.now() - pd.offsets.Day(7))

btc = get_historic_price('btc', 'bitstamp', after=last_week)
eth = get_historic_price('eth', 'bitstamp', after=last_week)

print(btc.head())
btc['ClosePrice'].plot(figsize=(15, 7))
plt.show()
print(eth.head())
eth['ClosePrice'].plot(figsize=(15, 7))
plt.show()