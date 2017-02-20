from lxml import html, etree
import requests
from lxml.html.clean import clean_html
from ast import literal_eval
import collections

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
	
# takes a url as a string and returns a SET of all of the words
# that are used on that webpage
def get_data_set(site_address):
	data_string = scrape(site_address)
	#data_set = data_string.split(' ')
	data_list = data_string.split(' ')
	
	#hap = data_list
	
	# the following removes new lines from the data in the set
	data_list_cleaned = []
	temp = ""
	for i in data_list:
		temp = i.strip('\n')
		temp = temp.strip(',')
		temp = temp.strip('.')
		temp = temp.lower()			#converts to lowercase
		data_list_cleaned.append(temp)

	data_set_cleaned = set(data_list_cleaned)
	
	counter = collections.Counter(data_list_cleaned)
	print counter
	
	#print data_set_cleaned
	
	return data_set_cleaned
	