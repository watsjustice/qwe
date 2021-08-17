import requests
import json
from bs4 import BeautifulSoup as bs


headers = {
	'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
	}
q = 'https://www.gurufocus.com/stock/AAPL/summary'

r = requests.get(url = q).text #, headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36')
data = bs(r , 'lxml').find_all('tr' , class_ = 'stock-indicators-table-row')



#собираем заголовки
data_1 , data_2 , data_3 , data_4 , data_5 = {} , {} , {} , {} , {}

item_barrel = ''
for x , item in enumerate(data):

	if x == 8: next  	
	#заголовок
	item_titles = f'{item.text}'.strip().replace('\n' , '').replace(' ' , '-').split('--')[0]

	#текущее значение
	item_current_values = f'{item.text}'.strip().replace('\n' , '').replace(' ' , '-').split('--')[1]

	#Barr №1
	if x != 8:
		try:
			item_persents_vsIndustry = item.find('div' , class_ = 'indicator-progress-bar').select('div')
			item_persents_vsIndustry = str(item_persents_vsIndustry)[str(item_persents_vsIndustry).index(':')+1:str(item_persents_vsIndustry).index(';')] 


		except:
			item_persents_vsIndustry = item.find('i' , class_ = 'bar-indicator gf-icon-caret-up')
			item_persents_vsIndustry = str(item_persents_vsIndustry)[str(item_persents_vsIndustry).index(':')+1:str(item_persents_vsIndustry).index(';')]


	#Barr №2	
	item_persents_vsHistory = item.select('div')[-1].get('style')
	item_persents_vsHistory = str(item_persents_vsHistory)[str(item_persents_vsHistory).index(':')+1:str(item_persents_vsHistory).index(';')]\
	#if str(item_persents_vsHistory)[str(item_persents_vsHistory).index(':')+1:str(item_persents_vsHistory).index(';')].isnumeric() else 'No data...'
	
	#Barr №3
	if x == 7:
		item_barrel = str(item.find('div' , class_ = 'bar-step').get('style')).split(':')[1][:-1].strip()
		item_index = str(item.find(class_ = 'bar-indicator gf-icon-caret-up').get('style')).split(':')[1][:-1].strip()
		data_1[7] = (item_titles , item_current_values , f'Not manipulator : {item_barrel}%' , f'Manipulator : {100-float(item_barrel[:-1])}%' ,\
			f'Index : {item_index}')

	#составление 5 словарей

	if x < 7:
		data_1[x] = (item_titles , f'Current value : {item_current_values}' , f'vsIndusrty {item_persents_vsIndustry}' , f'vsHistory {item_persents_vsHistory}')


	if x > 7 and x < 17:
		data_2[x] = (item_titles , f'Current value : {item_current_values}' , f'vsIndusrty {item_persents_vsIndustry}' , f'vsHistory {item_persents_vsHistory}')	

	if x > 16 and x < 35:
		data_3[x] = (item_titles , f'Current value : {item_current_values}' , f'vsIndusrty {item_persents_vsIndustry}' , f'vsHistory {item_persents_vsHistory}')	

	if x > 34 and x < 41:
		data_4[x] = (item_titles , f'Current value : {item_current_values}' , f'vsIndusrty {item_persents_vsIndustry}' , f'vsHistory {item_persents_vsHistory}')	

	if x > 41:
		data_5[x] = (item_titles , f'Current value : {item_current_values}' , f'vsIndusrty {item_persents_vsIndustry}' , f'vsHistory {item_persents_vsHistory}')	

thelist_of_barrels = [data_1 , data_2 , data_3 , data_4 , data_5] #список для перебора

thelist_of_titles = [

	'Financial Strength' , 'Profitability Rank' , 'Valuation Rank' ,
	'Dividend & Buy Back' , 'Valuation & Return'

	]#список для перебора

#ROI and WACC
item = str(data[8].find_all(class_ = 'bar-step')).split(';')

q1 = item[2].split(' ')[1][:6]
q2 = item[-1].split(' ')[1][:6].replace('\n' , '').strip()
data_1[8] = (f'WACC : {q1}' , f'ROIC : {q2}')


#создание 5 файлов
for i in range(5):
	with open(f'{thelist_of_titles[i]}.json' , 'w') as file:
		json.dump(thelist_of_barrels[i], file , indent = 4 , ensure_ascii = False)
