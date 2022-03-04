# Creating sqlite db with three tables: Categories, Products, Reviews
import sqlite3

try:
	sqlite_connection = sqlite3.connect('ebay_review.db')
	cursor = sqlite_connection.cursor()
	print("База данных создана и успешно подключена к SQLite")
	cursor.execute("""CREATE TABLE IF NOT EXISTS categories(
					catid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
					caturl TEXT);
					""")
	
	cursor.execute("""CREATE TABLE IF NOT EXISTS products(
					prodid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
					caturl TEXT,
					produrl TEXT UNIQUE,
					checker INT);
					""")
					
	cursor.execute("""CREATE TABLE IF NOT EXISTS reviews(
					rewid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
					produrl TEXT,
					url TEXT,
					author TEXT,
					date TEXT,
					stars INT,
					title TEXT,
					content TEXT);
					""")
	sqlite_connection.commit()
	cursor.close()
	
except sqlite3.Error as error:
	print("Ошибка при подключении к sqlite", error)
finally:
	if (sqlite_connection):
		sqlite_connection.close()
		print("Соединение с SQLite закрыто")
