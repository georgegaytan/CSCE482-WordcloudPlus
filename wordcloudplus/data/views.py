from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import mining
import simplejson as json

@csrf_exempt
def index(request):
	site_content_keys = []
	site_content_values = []
	json_string = '['
	
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