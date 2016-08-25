#!/usr/bin/env python
# coding: utf-8

import urllib
import urllib2
import json
import pickle
from bs4 import BeautifulSoup

def data_object_url(line):
	return 'http://eol.org/api/pages/1.0/{}.json?images=0&videos=0&sounds=0&maps=0&text=75&iucn=false&subjects=associations|trophicstrategy|habitat|ecology&licenses=all&details=true&com'.format(line)
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
	texts = []
	results = urllib.urlopen(data_object_url(eol_id)).read()
	if results [3:8] == 'error':
		return []
	data = json.loads(results)
	for info in data['dataObjects']:
		text = info['description']
		soup = BeautifulSoup(replace_problem_characters(text, replace_dict))
		clean = soup.get_text()
		texts.append(clean)
	return texts
#Given an EOL Taxon ID, this function returns the text data objects (from the json API 
#output) as a list. Returns empty list if the server does not give a proper response. 
#Beautiful Soup is used to clean the html tags from the text.

replace_dict = eval(open('replace_dict.txt').read())
f = range(1,41,1)
for n in f:
	file = 'id_' + str(n) + '.p'
	ids = pickle.load(open(file, 'rb'))
	for id in ids:
		print id
		texts = []
		texts = translate_id_to_text(id, replace_dict)
		print texts
		