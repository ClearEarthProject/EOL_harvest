#!/usr/bin/env python
# coding: utf-8

import urllib.request
import json
import pickle
from bs4 import BeautifulSoup
import os

def data_object_url(line):
	return 'http://eol.org/api/pages/1.0/{}.json?images=0&videos=0&sounds=0&maps=0&text=75&iucn=false&subjects=ecology&licenses=all&details=true&com'.format(line)
#This function generates the URL to call the EOL API to get all text data objects for a taxon under a specific 
#chapter in json format. In URL above, text is retrieved from under the 'associations', 
#'trophicstrategy', 'habitat', 'ecology' chapter.

def replace_problem_characters(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text
#This function calls a dictionary to find and replace characters in html that 
#interfere with GNRD ability to find names

def translate_id_to_text(eol_id, replace_dict):
	results = urllib.request.urlopen(data_object_url(eol_id)).read()
	dict = {}
	if results [3:8] == 'error':
		dict = {}
	data = json.loads(results)
	for info in data['dataObjects']:
		language = info.get('language')
		if language != 'en':
			continue
		else:
			dict = {}
			text = info['description']
			id = info['dataObjectVersionID']
			print(id)
			license = info.get('license')
			rightsholder = info.get('rightsHolder')
			source = info.get('source')
			agents = info.get('agents')
			if agents != None:
				agents1 = []
				for agent in agents:
					role = agent['role']
					if role == None:
						role = ''
					name = agent['full_name']
					agents1.append(role + '|' + name)
			soup = BeautifulSoup(replace_problem_characters(text, replace_dict), 'lxml')
			clean = soup.get_text()
			mini = {}
			h = []
			mini['id'] = id
			mini['license'] = license
			mini['rightsholder'] = rightsholder
			mini['source'] = source
			mini['agents'] = agents1
			mini['text'] = clean
		h.append(mini)
		dict[eol_id] = h
	return dict
#Given an EOL Taxon ID, this function returns the text data objects (from the json API 
#output) as a list. Returns empty list if the server does not give a proper response. 
#Beautiful Soup is used to clean the html tags from the text.


replace_dict = eval(open('replace_dict.txt').read())
f = range(1,41,1)
counter = 1
for n in f:
	print(n)
	print('new file')
	file = 'id_' + str(n) + '.p'
	ids = pickle.load(open(file, 'rb'))
	for id in ids:
		texts = translate_id_to_text(id, replace_dict)
		if len(texts) > 0:
			with open('ecology_text_' + str(counter) + '.json', 'a') as f:
				f.write('[')
				json.dump(texts, f)
				if os.stat('ecology_text_' + str(counter) + '.json').st_size > 100000:
					f.write(']')
					counter = counter + 1
				else:
					f.write(',')
		