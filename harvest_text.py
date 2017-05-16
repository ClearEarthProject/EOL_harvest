#!/usr/bin/env python
# coding: utf-8

import urllib
import urllib2
import json
import pickle
from bs4 import BeautifulSoup

def data_object_url(line):
	return 'http://eol.org/api/pages/1.0/{}.json?images=0&videos=0&sounds=0&maps=0&text=75&iucn=false&subjects=ecology&licenses=all&details=true&com'.format(line)
#This function generates the URL to call the EOL API to get all text data objects for a taxon under a specific 
#chapter in json format. In URL above, text is retrieved from under the 'associations', 
#'trophicstrategy', 'habitat', 'ecology' chapter.

def replace_problem_characters(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text
#This function calls a dictionary to find and replace characters in html that 
#interfere with GNRD ability to find names

def translate_id_to_text(eol_id, replace_dict):
	results = urllib.urlopen(data_object_url(eol_id)).read()
	dict = {}
	if results [3:8] == 'error':
		dict = {}
	data = json.loads(results)
	#print data['dataObjects']
	texts = []
	for info in data['dataObjects']:
		language = info.get('language')
		if language != 'en':
			continue
		else:
			#print info
			dict = {}
			text = info['description']
			id = info['dataObjectVersionID']
			print id
			license = info.get('license')
			#print license
			rightsholder = info.get('rightsHolder')
			#print rightsholder
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
			#print agents1
			soup = BeautifulSoup(replace_problem_characters(text, replace_dict), 'lxml')
			clean = soup.get_text()
			#print clean
			dict['id'] = id
			dict['license'] = license
			dict['rightsholder'] = rightsholder
			dict['source'] = source
			dict['agents'] = agents1
			dict['text'] = clean
			texts.append(dict)
			#texts.append(clean)
	return texts
#Given an EOL Taxon ID, this function returns the text data objects (from the json API 
#output) as a list. Returns empty list if the server does not give a proper response. 
#Beautiful Soup is used to clean the html tags from the text.

out_file = open('ecology_text.txt', 'w')

replace_dict = eval(open('replace_dict.txt').read())
f = range(1,41,1)
#x = []
counter = 0
for n in f:
	print n
	counter = counter + 1
	file = 'id_' + str(n) + '.p'
	ids = pickle.load(open(file, 'rb'))
	for id in ids:
		#print id
		#texts = []
		texts = translate_id_to_text(id, replace_dict)
		#print len(texts)
		#print texts
		if len(texts) > 0:
			#x.append(texts)
			#out_file.write(str(x))
		#print x
			with open('ecology_text_' + str(counter) + '.json', 'a') as f:
				 json.dump(texts, f)
		