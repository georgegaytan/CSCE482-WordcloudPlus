from stop_words import get_stop_words
from lxml import html, etree
import requests
from lxml.html.clean import clean_html
from ast import literal_eval
import collections
import string
from nltk.stem import WordNetLemmatizer
import json
from django.core.serializers.json import DjangoJSONEncoder
#import nltk (for after CDR is complete to not mess with workflow)

#init stopwords list
stopwords = get_stop_words('english')
#print stopwords

#init lemmatizer
lemmatizer = WordNetLemmatizer()

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
def get_data_set(addresses = [], *args):
	first_iteration = True
	data_list_postprocessing = []
	site1_percentage = {}
	site2_percentage = {}

	#iterates through each site in ddresses[]
	for site in addresses:
		current_site_list = []
		#if nonempty entry
		if site:
		#	print 'site addresses[] = ' + site
			data_string = scrape(site)
			data_list = data_string.split(' ')
			
			# the following removes new lines and punctionation from the data in the set 
			temp = ""
			for i in data_list:
				#remove all whitespace
				temp = ''.join(i.split())	#remove all whitespace
				#enforces utf-8
				temp = temp.encode('utf-8')
				#removes punctuation
				temp = temp.translate(None, string.punctuation)
				temp = temp.lower()	#lowercase
				#remove stop words
				temp = ''.join([word for word in temp.split() if word not in stopwords])
		
				#if nonempty str
				if temp and (len(temp) > 2) and (not temp.isdigit()):#if nonempty str
					current_site_list.append((lemmatizer.lemmatize(temp.decode('utf-8'))))
					data_list_postprocessing.append((lemmatizer.lemmatize(temp.decode('utf-8'))))

		#track word freq from first site
		#TODO: automate for n>2 sources
		if first_iteration:
			site1_count = collections.Counter(data_list_postprocessing)
			first_iteration = False
		else:
			site2_count = collections.Counter(current_site_list)
	
	#data_set_postprocessing = set(data_list_postprocessing)	#converts list into set which
												#removes duplicates
	counter = collections.Counter(data_list_postprocessing)
	
	#assert how much % of the frequency the sites contribute
	for i in site1_count:
		both_contain_word = False
		for j in site2_count:
			#on same word (key) calculate actual percent
			if i == j:
				both_contain_word = True
				sum = site1_count[i] + site2_count[j]
				site1_percentage[i] = (site1_count[i]/(sum + 0.00)) * 100
				site1_percentage[i] = round(site1_percentage[i], 2)
				site2_percentage[j] = (100.00 - site1_percentage[i])
		#in absence of same word, denote 100%
		if not both_contain_word:
			site1_percentage[i] = 100.00

	#horrible innefficient check for site2 words not in site1
	#guys it's 5am and i have 2 exams today i havent studied for lol
	for j in site2_count:
		both_contain_word = False
		for i in site1_count:
			if j == i:
				both_contain_word = True
		#in absence of same word, denote 100%
		if not both_contain_word:
			site2_percentage[j] = 100.00

	#convert site percents to django friendly JSON
	site1_percentage_json = json.dumps(dict(site1_percentage), cls=DjangoJSONEncoder)
	site2_percentage_json = json.dumps(dict(site2_percentage), cls=DjangoJSONEncoder)

	#wordcloud dictionary of objects
	w = {
			'site_content' : counter.most_common(),
			'site1_percentage_json' : site1_percentage_json,
			'site2_percentage_json' : site2_percentage_json
		}

	return w