# Because all the government resolutions are in RTF format, it is needed to convert it to DOCX to extract tables


import win32com.client
import os
import re

dic_regions = {'Иван': 'Ivanovskaya', 'Рязан': 'Ryazanskaya', 'Тамбов': 'Tambovskaya', 'Алтайск': 'Altayskaya', 'Амурск': 'Amurskaya',
				'Арханг': 'Arhangelskaya', 'Астрах': 'Astrahanskaya', 'Белгор': 'Belgorodskaya', 'Брянск': 'Brayanskaya', 'ВЛАДИМ': 'Vladimirskaya', 
				'Волгогр': 'Volgogradskaya', 'Вологод': 'Vologodskaya', 'Воронеж': 'Voronezhskaya', 'ЕАО': 'Evreyskaya', 'Забайк': 'Zabaykalskiy', 'Иркутск': 'Irkutskaya', 
				'КБР': 'Kab_Bal_resp', 'Калинин': 'kaliningradskaya', 'Калужс': 'Kaluzhskaya', 'Камчат': 'Kamchatskiy', 'Карача': 'Kar_Cher_resp', 'Кемеров': 'Kemerovskaya', 
				'Кировск': 'Kemerovskaya', 'Костром': 'Kostromskaya', 'Краснод': 'Krasnodarskiy', 'Краснояр': 'Krasnoyarskiy', 'Курган': 'Kurganskaya', 
				'Курск': 'Kurskaya', 'Ленинг': 'Leningradskaya', 'Липецк': 'Lipitskaya', 'Магадан': 'Magadanskaya', 'Москв': 'Moskva', 'МO': 'Moskovskaya', 
				'Мурманс': 'Murmanskaya', 'Ненецк': 'Nenetskiy', 'Нижегор': 'Nizhegorodskaya', 'Новгор': 'Novgorodskaya', 'Новосиб': 'Novosibirskaya', 
				'Омская': 'Omsakaya', 'Оренбур': 'Orenburgskaya', 'Орловск': 'Orlovskaya', 'Пензенс': 'Penzenskaya', 'Пермск': 'Permskiy', 'Приморс': 'Primorskiy', 
				'Псковс': 'Pskovskaya', 'Ростов': 'Rostovskaya', 'Самарск': 'Samarskaya', 'Санкт': 'St_Peterburg', 'Саратов': 'Saratovskaya', 
				'Сахалин': 'Sahalinskaya', 'Свердл': 'Sverdlovskaya', 'Севастоп': 'Sevastopol', 'Смоленс': 'Smolenskaya', 'Ставроп': 'Stavropolskiy', 
				'Тверск': 'tverskaya', 'Томск': 'Tomskaya', 'Тульск': 'Tulskaya', 'Тюменск': 'Tumenskaya', 'УР': 'Udmurtskaya', 'Ульянов': 'Ulyanovskaya', 
				'РК': 'Kareliya', 'Хабаров': 'Habarovskiy', 'ХМАО': 'Hanti_mansiyskiy', 'Челябин': 'Chelyabinskaya', 'Чеченск': 'Chechnya', 
				'Чувашск': 'Chuvashiya', 'Чукотск': 'Chukotka', 'ЯНАО': 'Yamal_nen_okr', 'ЯО': 'yaroslavskaya', 'РТ': 'Tatarstan', 'РБ': 'Buryatia',
				'Республики Алтай': 'Altay_resp', 'Тыва': 'Tiva_resp', 'Хакас': 'Hakasiya', 'РС(Я)': 'Yakutiya', 'Крым': 'Krim_resp', 'Осетия': 'Osetiya', 'Мордов': 'Mordovia',
				'Калмык': 'kalmikiya', 'Марий': 'Mariy_El', 'Ингуш': 'Ingushetiya', 'Дагестан': 'Dagestan'
}
# I leave this variable as an example, unfortnately win32com can process only in this view
rootDir = 'c:\\job\\12T\\regional roads\\Seasonal_TAR\\111121_1'

def ConvertRtfToDocx(rootDir, file, index, newname):
    word = win32com.client.Dispatch("Word.Application")
    wdFormatDocumentDefault = 16
    doc = word.Documents.Open(rootDir + "\\" + file)
    doc.SaveAs(str(rootDir + "\\{}.docx".format(newname + str(index))), FileFormat=wdFormatDocumentDefault)
    doc.Close()
    word.Quit()
	
def bulk_convert():
	for i in os.listdir(rootDir):
		for j in dic_regions:
			if j in i:
        # for my purposes all the documents that were in use starts with '1', I decided to divide different versions by this feature 
				if i.startswith('1'):
					ConvertRtfToDocx(rootDir, i, 0, dic_regions[j])
				else:
					ConvertRtfToDocx(rootDir, i, 1, dic_regions[j])

bulk_convert()


