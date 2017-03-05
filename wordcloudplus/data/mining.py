from lxml import html, etree
import requests
from lxml.html.clean import clean_html
from ast import literal_eval
import collections
import string

def get_all_texts(el, class_name):
	return [e.text_content() for e in els.find_class(class_name)]

# takes a url as a string and returns a string of all of the words
# that are used on that webpage
def scrape(site_address):
	page = requests.get(site_address)			#returns raw html
	page = clean_html(page.content)	#removes <script> tags and their contents
	document = html.document_fromstring(page)	#removes all other tags

	return document.text_content()
	
# takes a url as a string and returns a STRING of all of the words
# that are used on that webpage
def get_data_string(site_address):
	return scrape(site_address)
	
# takes a url as a string and returns a SET of TOUPLES of all of the words
# that are used on that webpage in order of frequency
def get_data_set(site_address):
	data_string = scrape(site_address)
	data_list = data_string.split(' ')
	
	# the following removes new lines and punctionation from the data in the set 
	data_list_cleaned = []
	temp = ""
	for i in data_list:
		temp = ''.join(i.split())	#remove all whitespace
		temp = temp.encode('utf-8')	#enforces utf-8
		temp = temp.translate(None, string.punctuation)	#remove punct
		temp = temp.lower()			#converts to lowercase
		temp = temp.strip()
		if temp:
			data_list_cleaned.append(temp)

	#data_set_cleaned = set(data_list_cleaned)	#converts list into set which
												#removes duplicates
	counter = collections.Counter(data_list_cleaned)
	
	return counter.most_common()
	
