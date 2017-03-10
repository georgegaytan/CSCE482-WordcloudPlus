from stop_words import get_stop_words
from lxml import html, etree
import requests
from lxml.html.clean import clean_html
from ast import literal_eval
import collections
import string
#from nltk.stem import WordNetLemmatizer
#import nltk (for after CDR is complete to not mess with workflow)

#init stopwords list
stopwords = get_stop_words('english')

#init lemmatizer
#lemmatizer = WordNetLemmatizer()

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
def get_data_set(site_addresses = [], *args):
	data_list_postprocessing = []
	#iterates through each site in site_addresses[]
	for site in site_addresses:
		#if nonempty entry
		if site:
			print 'site addresses[] = ' + site
			data_string = scrape(site)
			data_list = data_string.split(' ')
			
			# the following removes new lines and punctionation from the data in the set 
			temp = ""
			for i in data_list:
				#remove all whitespace
				temp = ''.join(i.split())	#remove all whitespace
				#remove stop words
				temp = ''.join([word for word in temp.split() if word not in stopwords])
				#enforces utf-8
				temp = temp.encode('utf-8')
				#removes punctuation
				temp = temp.translate(None, string.punctuation)
				temp = temp.lower()	#lowercase
		
				#enforces lemmatization
				#temp = lemmatizer.lemmatize(word)
		
				#if nonempty str
				if temp and (len(temp) > 2) and (not temp.isdigit()):#if nonempty str
					data_list_postprocessing.append(temp)
	
	#data_set_postprocessing = set(data_list_postprocessing)	#converts list into set which
												#removes duplicates
	counter = collections.Counter(data_list_postprocessing)
		
	return counter.most_common()
	
