import grequests
import requests
from bs4 import BeautifulSoup
import sqlite3

url = 'https://www.ebay.com/'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'}

sqlite_connection = sqlite3.connect('ebay_review.db')
cursor = sqlite_connection.cursor()

# getting the main categories link
request_ebay_main_page = requests.get(url)
soup_main = BeautifulSoup(request_ebay_main_page.text, 'html5lib')
main_categories_link = soup_main.find('h3', {'class': 'gf-bttl'}).a['href']

# getting the main categories
def get_main_categories(url):
	main_categories_links = []
	request_categories = requests.get(main_categories_link)
	soup = BeautifulSoup(request_categories.text, 'html5lib')
	top_cat = soup.find_all('a', {'class': 'top-cat'})
	for i in top_cat:
		main_categories_links.append(i['href'])
	# I remove and parse these two pages additionally because they have one more layer of subcategories 
	main_categories_links.remove('https://www.ebay.com/b/Books-Movies-Music/bn_7000259849')
	main_categories_links.remove('https://www.ebay.com/b/Collectibles-Art/bn_7000259855')
	for i in ['https://www.ebay.com/b/Books-Movies-Music/bn_7000259849', 'https://www.ebay.com/b/Collectibles-Art/bn_7000259855']:
		request_additional_cat = requests.get(i)
		soup_cat = BeautifulSoup(request_additional_cat.text, 'html5lib')
		links_sub = soup_cat.find_all('a', {'class': 'b-textlink b-textlink--parent'})
		for j in links_sub:
			main_categories_links.append(j['href'])
	return main_categories_links

# getting all the categories on ebay
def get_all_sub_categories(main_cat_list):
		all_sub_cat_list = []
		request_categories = (grequests.get(u) for u in main_cat_list)
		responses_list_sub_cat = grequests.map(request_categories, size=16)
		# print(responses_list_sub_cat)
		for i in responses_list_sub_cat:
			# print(i.url)
			soup = BeautifulSoup(i.text, 'html5lib')
			links = soup.find_all('a', {'class': ['b-textlink b-textlink--parent', 'b-textlink b-textlink--sibling']})
			for j in links:
				all_sub_cat_list.append(j['href'])
		return all_sub_cat_list

# filling categories into DB
def fill_cat(mid):
	request_categories = (grequests.get(u) for u in mid)
	responses_list_sub_cat = grequests.map(request_categories, size=16)
	for i in responses_list_sub_cat:
		if BeautifulSoup(i.text, 'html5lib').find_all('a', {'class': 's-item__link'}):
			cursor.execute("""INSERT INTO categories(caturl) VALUES(?);""", [i.url])
			sqlite_connection.commit()

	
	
main_cat_list = get_main_categories(main_categories_link)
all_cat_list = get_all_sub_categories(main_cat_list)
final_cat = fill_cat(all_cat_list)

cursor.close()
if (sqlite_connection):
	sqlite_connection.close()
	print("Соединение с SQLite закрыто")




