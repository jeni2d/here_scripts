import grequests
import requests
from bs4 import BeautifulSoup
import sqlite3

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'}


sqlite_connection = sqlite3.connect('ebay_review.db')
cursor = sqlite_connection.cursor()

# filling products ito DB
def get_products(response, link):
	product_soup = BeautifulSoup(response, 'html5lib')
	products_links = product_soup.find_all('a', {'class': 's-item__link'})
	for j in products_links:
		cursor.execute("""INSERT INTO products(caturl, produrl) VALUES(?, ?) ON CONFLICT (produrl) DO NOTHING;""", [link, j['href']])
		sqlite_connection.commit()
		# print(j['href'])
	try:
		next_link = product_soup.find('a', {'rel': 'next', 'class': 'ebayui-pagination__control'})['href']
		if len(products_links) > 0 and len(next_link) > 1:
			return next_link
	except TypeError:
		pass
    
# request the list of categories
def requester(list):
	next_link_list = []
	request_sub_categories = (grequests.get(u, headers=headers) for u in list)
	responses_list_sub_cat = grequests.map(request_sub_categories, size=16)
	for i in responses_list_sub_cat:
		next_link = get_products(i.text, i.url)
		if next_link != None:
			next_link_list.append(next_link)
		print(next_link)
		print(i.status_code)
	print('page ready')
	if len(next_link_list) > 0:
		requester(next_link_list)

list_cat = []
cursor.execute("SELECT caturl FROM categories;")
res = cursor.fetchall()
for i in res:
	list_cat.append(i[0])


requester(list_cat)

cursor.close()
if (sqlite_connection):
	sqlite_connection.close()
	print("Соединение с SQLite закрыто")
