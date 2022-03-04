import requests
import json
import simplejson
import pandas as pd
import time
requests.packages.urllib3.disable_warnings()

# get address from district and OKS by lat long
def rosgeo(coords):
    dist_oks = []

    for i in range(1,6,4):
        url = 'https://pkk.rosreestr.ru/api/features/'+str(i)+'?text='+coords   
        try:
            res = requests.get(url, verify=False)
            dist_oks.append(res.json()['features'][0]['attrs']['address'])
        except (TimeoutError, IndexError, simplejson.errors.JSONDecodeError, requests.exceptions.ConnectionError):
            pass
    return dist_oks

# CSV file with latitude and longitude as an input
df = pd.read_csv('PA_sample.csv', sep=',')
df['Coords'] = df[['Latitude', 'Longitude']].astype(str).agg(','.join, axis=1)
df['District'] = ''
df['OKS'] = ''

for i in df.iterrows():
	adr = rosgeo(i[1]['Coords'])
	df.at[i[0], 'District'] = adr[0]
	df.at[i[0], 'OKS'] = adr[1]
	print(i[0], df.iloc[i[0]]['District'], df.iloc[i[0]]['OKS'])
	time.sleep(1)
df.to_csv('result.csv', sep=',')
