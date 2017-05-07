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
import copy
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

def calc_frequency(areaNum, word_counts, curr_timeslot_word_counts):
	timeslot_area_percentage = {}

	for i in word_counts:
		for j in curr_timeslot_word_counts:
			#on same word (key) calculate actual percent
			if i == j:
				timeslot_area_percentage[i] = (word_counts[i]/(curr_timeslot_word_counts[j] + 0.00)) * 100
				timeslot_area_percentage[i] = round(timeslot_area_percentage[i], 2)

	return timeslot_area_percentage
	# if areaNum == 1:
	# 	return {"area1" : timeslot_area_percentage} # TODO: convert to django friendly using below??
	# elif areaNum == 2:
	# 	return {"area2" : timeslot_area_percentage}
	# elif areaNum == 3:
	# 	return {"area3" : timeslot_area_percentage}

	#convert site percents to django friendly JSON
	# site1_percentage_json = json.dumps(dict(site1_percentage), cls=DjangoJSONEncoder)
	# site2_percentage_json = json.dumps(dict(site2_percentage), cls=DjangoJSONEncoder)

# takes a url as a string and returns a SET of TUPLES of all of the words
# that are used on that webpage in order of frequency
def get_data_set(area1addr = [], area2addr = [], area3addr = [], years = [], *args):
	index_counter = 0
	#FOR SIZE: Total word counts per year { 1995 : {blah : 50, hey : 23, etc} }
	timeslot_word_counts = {}
	#FOR FREQUENCY: percentages of each word per source in each timeslot
	#i.e. { 1995 : {"area1" : {'word' : 33.33%, 'lol' : 69%, etc}, "area2" : {'word' : 66.67%, 'lol' : 31%, etc}} }
	timeslot_word_frequency = {}

	#dictionary sorting stored objects by year
	# { 1995 : {"area1" : Data, "area2" : Data}, 2013 : {"area3" : Data} }
	# WHERE Data = ["wrod", "hi", "adsf"]
	post_processed_storage = {}

	while index_counter < len(area1addr):
		site = area1addr[index_counter]
		current_site_list = []
		#if nonemtpy entry
		if site:
			data_string = scrape(site)
			data_list = data_string.split(' ')

			#preprocessing the scraped dataset
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
					#data_list_postprocessing.append((lemmatizer.lemmatize(temp.decode('utf-8'))))

			area1Data = {"area1" : current_site_list}

			#if year exists in storage, extend onto processed data to list at that year
			if years[index_counter] in post_processed_storage:
				#if data from area exists in storage, extend that data
				if "area1" in post_processed_storage[years[index_counter]]:
					post_processed_storage[years[index_counter]]["area1"].extend(area1Data.values()[0])
				#else create new data entry
				else:
					post_processed_storage[years[index_counter]]["area1"] = (area1Data.values()[0])
			#else, create new year in storage, add list w/ 1 value (processed data)
			else:
				post_processed_storage[years[index_counter]] = area1Data

		index_counter+= 1

	while index_counter < (len(area1addr) + len(area2addr)):
		site = area2addr[index_counter - len(area1addr)]
		current_site_list = []
		#if nonemtpy entry
		if site:
			data_string = scrape(site)
			data_list = data_string.split(' ')

			#preprocessing the scraped dataset
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
					#data_list_postprocessing.append((lemmatizer.lemmatize(temp.decode('utf-8'))))

			area2Data = {"area2" : current_site_list}

			#if year exists in storage, extend onto processed data to list at that year
			if years[index_counter - len(area1addr)] in post_processed_storage:
				#if data from area exists in storage, extend that data
				if "area2" in post_processed_storage[years[index_counter - len(area1addr)]]:
					post_processed_storage[years[index_counter - len(area1addr)]]["area2"].extend(area2Data.values()[0])
				#else create new data entry
				else:
					post_processed_storage[years[index_counter - len(area1addr)]]["area2"] = (area2Data.values()[0])
			#else, create new year in storage, add list w/ 1 value (processed data)
			else:
				post_processed_storage[years[index_counter - len(area1addr)]] = area2Data

		index_counter+= 1

	while index_counter < (len(area1addr) + len(area2addr) + len(area3addr)):
		site = area3addr[index_counter - (len(area1addr) + len(area2addr))]
		current_site_list = []
		#if nonemtpy entry
		if site:
			data_string = scrape(site)
			data_list = data_string.split(' ')

			#preprocessing the scraped dataset
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
					#data_list_postprocessing.append((lemmatizer.lemmatize(temp.decode('utf-8'))))

			area3Data = {"area3" : current_site_list}

			#if year exists in storage, extend processed data onto list at that year
			if years[index_counter - (len(area1addr) + len(area2addr))] in post_processed_storage:
				#if data from area exists in storage, extend that data
				if "area3" in post_processed_storage[years[index_counter - (len(area1addr) + len(area2addr))]]:
					post_processed_storage[years[index_counter - (len(area1addr) + len(area2addr))]]["area3"].extend(area3Data.values()[0])
				#else create new data entry
				else:
					post_processed_storage[years[index_counter - (len(area1addr) + len(area2addr))]]["area3"] = (area3Data.values()[0])
			#else, create new year in storage, add list w/ 1 value (processed data)
			else:
				post_processed_storage[years[index_counter - (len(area1addr) + len(area2addr))]] = area3Data

		index_counter+= 1
	
	#TODO: in testing check word_counts, make sure it doesn't get weird
	#FOR FONT SIZE: Accesses each timeslot and creates total count
	for timeslot in post_processed_storage:
		complete_word_list = []
		dict_of_data = post_processed_storage[timeslot]
		first_index = True

		#print dict_of_data
		for areatype, word_list in dict_of_data.iteritems():
			word_list_var = copy.deepcopy(word_list)
			if first_index:
				complete_word_list = word_list_var
				first_index = False
			else:
				complete_word_list.extend(word_list_var)

		#comp_word_list_dict = dict(collections.Counter(complete_word_list))
		# Creates list of tuples of words,freq at that timeslot, sorted descending
		timeslot_word_counts[timeslot] = (collections.Counter(complete_word_list)).most_common()
		# Converts tuples into dictionary format to not be shit
		timeslot_word_counts[timeslot] = dict(timeslot_word_counts[timeslot])

	#FOR FREQUENCY: 
	for timeslot in post_processed_storage:
		dict_of_data = post_processed_storage[timeslot]
		timeslot_word_frequency[timeslot] = {}

		for areatype, word_list in dict_of_data.iteritems():
			if (areatype == "area1"):
				word_counts = collections.Counter(word_list)
				freq = (calc_frequency(1, word_counts, timeslot_word_counts[timeslot]))
				timeslot_word_frequency[timeslot]["area1"] = freq
			elif (areatype == "area2"):
				word_counts = collections.Counter(word_list)
				freq = (calc_frequency(2, word_counts, timeslot_word_counts[timeslot]))
				timeslot_word_frequency[timeslot]["area2"] = freq
			elif (areatype == "area3"):
				word_counts = collections.Counter(word_list)
				freq = (calc_frequency(3, word_counts, timeslot_word_counts[timeslot]))
				timeslot_word_frequency[timeslot]["area3"] = freq

	#wordcloud object of dictionaries
	w = {
		'post_processed_storage' : post_processed_storage,
		'timeslot_word_counts' : timeslot_word_counts,
		'timeslot_word_frequency' : timeslot_word_frequency
	}

	return w
