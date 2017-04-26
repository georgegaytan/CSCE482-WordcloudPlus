from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import mining
import simplejson as json
from lxml import html, etree
from lxml.html.clean import clean_html
from data.models import Docs

@csrf_exempt
def index(request):
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
		area1addr = request.POST.getlist('firstAddresses')
		area2addr = request.POST.getlist('secondAddresses')
		area3addr = request.POST.getlist('thirdAddresses')

		wordcloud_object = mining.get_data_set(area1addr, area2addr, area3addr, years)
		post_processed_storage = wordcloud_object['post_processed_storage']
		timeslot_word_counts = wordcloud_object['timeslot_word_counts']
		timeslot_word_frequency = wordcloud_object['timeslot_word_frequency']
		post_processed_storage = json.dumps(post_processed_storage, ensure_ascii=False)
		timeslot_word_counts = json.dumps(timeslot_word_counts, ensure_ascii=False)
		timeslot_word_frequency = json.dumps(timeslot_word_frequency, ensure_ascii=False)

		# print timeslot_word_counts
		# print timeslot_word_frequency

	else:
		years = ''
		post_processed_storage = ''
		timeslot_word_counts = ''
		timeslot_word_frequency = ''

	c = {
		'post_processed_storage' : post_processed_storage,
		'timeslot_word_counts' : timeslot_word_counts,
		'timeslot_word_frequency' : timeslot_word_frequency,
		'years' : years
	}

	return render(request, 'data/index.html', c)