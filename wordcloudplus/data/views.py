from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import mining
import simplejson as json
from lxml import html, etree
from lxml.html.clean import clean_html
from data.models import Docs

@csrf_exempt
def index(request):
	site_content_keys1 = []
	site_content_values1 = []
	site_content_json1 = '['
	wordcloud_object_dict1 = {}
	site_content_keys2 = []
	site_content_values2 = []
	site_content_json2 = '['
	wordcloud_object_dict2 = {}
	site_content_keys3 = []
	site_content_values3 = []
	site_content_json3 = '['
	wordcloud_object_dict3 = {}
	"""
	if request.method == 'POST':
		#print request.POST		#for testing / error handling
		site_content = mining.get_data_set(request.POST['address'])
		
		for i in site_content:
			site_content_keys.append(i[0])
			site_content_values.append(i[1])
			json_string += (('' + i[0] + ', ') * i[1])
		json_string = json_string[:-2] + ']'
	else:
		site_content = ''
		
	zipped_counter = zip(site_content_keys, site_content_values)
	
	c = {
			'mined_data': site_content,
			'zipped_counter': zipped_counter,
			'json_string': json_string
		}
	
	return render(request, 'data/index.html', c)
	"""
	if request.method == 'POST':
		#print request.POST		#for testing / error handling
		
		# if request.POST['file_upload']:
		# 	file=request.FILES['doc']
		# 	print file
			
		# 	instance = Docs(	file=request.FILES['doc'],
		# 						title = 'temp',
		# 					)
		# 	instance.save()
		
		# else:
			#site_content, site1_percentage, site2_percentage
		
		years = request.POST.getlist('years')
		wordcloud_object_dict1 = mining.get_data_set(request.POST.getlist('firstAddresses'))
		wordcloud_object_dict2 = mining.get_data_set(request.POST.getlist('secondAddresses'))
		wordcloud_object_dict3 = mining.get_data_set(request.POST.getlist('thirdAddresses'))

		site_content1 = wordcloud_object_dict1['site_content']
		site1_percentage_json1 = wordcloud_object_dict1['site1_percentage_json']
		site2_percentage_json1 = wordcloud_object_dict1['site2_percentage_json']

		site_content2 = wordcloud_object_dict2['site_content']
		site1_percentage_json2 = wordcloud_object_dict2['site1_percentage_json']
		site2_percentage_json2 = wordcloud_object_dict2['site2_percentage_json']

		site_content3 = wordcloud_object_dict3['site_content']
		site1_percentage_json3 = wordcloud_object_dict3['site1_percentage_json']
		site2_percentage_json3 = wordcloud_object_dict3['site2_percentage_json']

		for i in site_content1:
			site_content_keys1.append(i[0])
			site_content_values1.append(i[1])
			site_content_json1 += (('' + i[0] + ', ') * i[1])
		site_content_json1 = site_content_json1[:-2] + ']'

		for i in site_content2:
			site_content_keys2.append(i[0])
			site_content_values2.append(i[1])
			site_content_json2 += (('' + i[0] + ', ') * i[1])
		site_content_json2 = site_content_json2[:-2] + ']'

		for i in site_content3:
			site_content_keys3.append(i[0])
			site_content_values3.append(i[1])
			site_content_json3 += (('' + i[0] + ', ') * i[1])
		site_content_json3 = site_content_json3[:-2] + ']'

	else:
		years = ''
		site_content1 = ''
		site1_percentage_json1 = ''
		site2_percentage_json1 = ''

		site_content2 = ''
		site1_percentage_json2 = ''
		site2_percentage_json2 = ''

		site_content3 = ''
		site1_percentage_json3 = ''
		site2_percentage_json3 = ''

	c = {
			'site_content_json1':site_content_json1,
			'site1_percentage_json1':site1_percentage_json1,
			'site2_percentage_json1':site2_percentage_json1,
			'site_content_json2':site_content_json2,
			'site1_percentage_json2':site1_percentage_json2,
			'site2_percentage_json2':site2_percentage_json2,
			'site_content_json3':site_content_json3,
			'site1_percentage_json3':site1_percentage_json3,
			'site2_percentage_json3':site2_percentage_json3,			
			'years':years
		}

	return render(request, 'data/index.html', c)
