# EOL_harvest
code to harvest and work with data objects from EOL

Python 2.7

All the code is in harvest_text.py
The "id" files are a deduped list of all the unique EOL taxon ID numbers that can be used
to look up information with the API. There are over 4 million IDs.
The replacedict.txt is a dictionary used in the code to replace some troublesome 
characters in the harvested text.

The output is a list of dictionaries for each taxon id. Every element of the list is one
text data object with the attribution and licensing information in the dictionary. The agents 
are also a list formatted as role|name.