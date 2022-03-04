import grequests
import requests
from bs4 import BeautifulSoup
import sqlite3

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'}

sqlite_connection = sqlite3.connect('ebay_review.db')
cursor = sqlite_connection.cursor()

def check_reviews_url(url):
	request_item_page = requests.get(url)
	soup = BeautifulSoup(request_item_page.text, 'html5lib')
	try:
		return soup.find('a', {'class': ['sar-btn right', 'see--all--reviews-link']})['href']
	except TypeError:
		return url

# parse reviews
def get_ebay_review(url, produrl):
	prod = produrl
	request_item_page = requests.get(url, headers=headers)
	soup = BeautifulSoup(request_item_page.text, 'html5lib')
	# review section can have at least three different format
	review = soup.find_all(['div', 'li'], {'class': ['ebay-review-section', 'review--section']})
	for i in review:
		dic = {}
		title = i.find(['p','h3', 'h4']).text
		author = i.find('a', {'class': ['review-item-author', 'review--author']}).text
		#review text can be empty
		try:
			content = i.find('p', {'class': ['review-item-content', 'review--content']}).text
		except AttributeError:
			content = ''
		stars = len(i.find_all('i', {'class': 'fullStar'}))
		date = i.find('span', {'class': ['review-item-date', 'review--date']}).text
		cursor.execute("SELECT url, author, date, stars, title, content FROM reviews WHERE url = ? AND author = ? AND date = ? AND stars= ? AND title= ? AND content = ?;", [url, author, date, stars, title, content])
		res = cursor.fetchone()
		if not res:
			cursor.execute("""INSERT INTO reviews(produrl, url, author, date, stars, title, content) VALUES(?, ?, ?, ?, ?, ?, ?)""", [prod, url, author, date, stars, title, content])
			sqlite_connection.commit()
	# checking and parsing next pages with reviews	
	try:
		next = soup.find('a', {'rel': 'next', 'class': 'spf-link'})['href']
		get_ebay_review(next, prod)
	except TypeError:
		pass

cursor.execute("SELECT produrl FROM products;")
res = cursor.fetchall()
for i in res:
	get_ebay_review(check_reviews_url(i[0]), i[0])
	print(i[0])

cursor.close()
if (sqlite_connection):
	sqlite_connection.close()
	print("Соединение с SQLite закрыто")
