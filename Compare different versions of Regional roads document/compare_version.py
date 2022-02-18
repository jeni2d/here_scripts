# This script compares the different version of government resolution document regarding regional roads
# The script can identify new roads, excluded roads and changes in the length
# the script supports batch comparison, any number of regions but only two versions for each region

import pandas as pd
from docx.api import Document
import re
import os

os.chdir('') # put your work directory here

def parsing_tables():
	dfs = {}
  # process all the documents in the folder and extract particular tables from them
	for ind, file in enumerate(os.listdir()):
		if file[-4:] == 'docx':
			print(file)
			document = Document(file)
			data = []
			keys = None
			for i in document.tables:
				text_first_row = (cell.text for cell in i.rows[0].cells)
				f_row = ' '.join(tuple(text_first_row)).lower()
				if re.search(r'идентификационны\w\sномер', f_row):
					for j, row in enumerate(i.rows):
						text = (cell.text.strip() for cell in row.cells)
						if j == 0:
							keys = list(text)
							for index, i in enumerate(keys):
								if index < 10:
									keys[index] = str(index) + i
							keys = tuple(keys)
							continue
						row_data = dict(zip(keys, text))
						data.append(row_data)
      
      # create pandas data frame
			df = pd.DataFrame(data)
      
      # in this block, all not necessary data will be deleted and some columns will be renamed
			for i in df.columns:
				if 'Vladimirskaya' in file:
					if not re.search(r'(идентификационны\w\sномер|\sпротяжен)', i.lower()):
						df = df.drop([i], axis='columns')
					elif re.search(r'идентификационны\w\sномер', i.lower()):
						df = df.rename(columns={i: 'ID'})
					elif re.search(r'\sпротяжен', i.lower()) and not 'Length' in df:
						df = df.rename(columns={i: 'Length'})
				else:
					if not re.search(r'(идентификационны\w\sномер|(протяж[её]н(ность|ие))|всего)', i.lower()):
						df = df.drop([i], axis='columns')
					elif re.search(r'идентификационны\w\sномер', i.lower()):
						df = df.rename(columns={i: 'ID'})
					elif re.search(r'((протяж[её]н(ность|ие))|всего)', i.lower()) and not 'Length' in df:
						df = df.rename(columns={i: 'Length'})

			for i in df.columns:
				if not re.search(r'(Length|ID)', i):
					df = df.drop([i], axis='columns')

      # in this block, all the roads with the same ID will be grouped and the length will be summed
			df['Length'] = df['Length'].str.replace(',','.')
			select = df[df['ID'].str.match(r'\d\d(\s|-|\.)?[\d|О|К]', na=False)]
			# select = df[df['ID'].str.match(r'\d\d(\s|-|\.)?[\d|О].+[ПпРЗКНАВ]', na=False)]
			for i in select.iterrows():
				if re.search(r'[абвгдежзиклмнопрстуфкч]', i[1]['Length']):
					select.at[i[0], 'Length'] = '0'
				elif i[1]['Length'] == '':
					select = select.drop([i[0]])
			select = select.astype({'Length': float})
			select = select[['ID','Length']].loc[(select[['ID', 'Length']].shift(-1) != select[['ID', 'Length']]).any(axis=1)]
			df2 = select.groupby(['ID'])['Length'].sum().reset_index()
      
      # grouping versions of each region into dictionary
			if dfs.get(file[:-6]):
				dfs[file[:-6]].append(df2)
			else:
				dfs[file[:-6]] = [df2]
	return dfs

def compare_version(dfs):
  # compare versions of each region
	for key, value in dfs.items():
		
		df = value[0]
		df2 = value[1]
		merged = pd.merge(df, df2, on=['ID'])
		
    # if only length changed more than 500m it will be in the output
		dif_len = merged[abs(merged['Length_x'] - merged['Length_y']) >= 0.5]
		dif_len['Comment'] = 'Different length'
		
    for i in dif_len.iterrows():
			if i[1]['Length_y'] == 0:
				dif_len.at[i[0], 'Comment'] = 'Excluded road'

		new_roads = df2[~df2['ID'].isin(merged['ID'])]
		new_roads['Comment'] = 'New road'
		for i in new_roads.iterrows():
			if i[1]['Length'] == 0:
				new_roads.at[i[0], 'Comment'] = 'Excluded road'
		
		reduced_roads = df[~df['ID'].isin(merged['ID'])]
		reduced_roads['Comment'] = 'Excluded road'
		
		fin_list = dif_len.append(new_roads).append(reduced_roads) 
		
		fin_list.to_csv('Put path to output file here/{}_diff.csv'.format(key), sep=',', index=False, encoding='utf-8-sig')

# get_table = parsing_tables()
# compare_version(get_table)	
# print('Finish')






