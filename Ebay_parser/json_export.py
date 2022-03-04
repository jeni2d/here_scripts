import sqlite3
import json

sqlite_connection = sqlite3.connect('ebay_review.db')
cursor = sqlite_connection.cursor()

list_reviews = []

cursor.execute("SELECT produrl, url, author, date, stars, title, content FROM reviews WHERE produrl <> 'NULL';")
res = cursor.fetchall()

dic_items = {}
for i in res:
	dic = {}
	dic['url'] = i[1]
	dic['author'] = i[2]
	dic['date'] = i[3]
	dic['stars'] = i[4]
	dic['title'] = i[5]
	dic['content'] = i[6]
	if dic_items.get(i[0]):
		dic_items[i[0]].append(dic)
	else:
		dic_items[i[0]] = [dic]
	
for index, value in enumerate(dic_items.values()):
	with open('{}.json'.format(index), 'w') as file:
		json.dump(value, file, indent=4, ensure_ascii=False)

cursor.close()
if (sqlite_connection):
	sqlite_connection.close()
	print("Соединение с SQLite закрыто")
