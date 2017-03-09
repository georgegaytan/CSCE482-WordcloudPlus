from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import mining
from lxml import html, etree
from lxml.html.clean import clean_html

@csrf_exempt
def index(request):
	site_content_keys = []
	site_content_values = []
	
	
	
	if request.method == 'POST':
		print request.POST		#for testing / error handling
		
		try:
			site_content = mining.get_data_set(request.POST['address'])
			
			for i in site_content:
				site_content_keys.append(i[0])
				site_content_values.append(i[1])
		except:
			try:
				print "reading file...:"
				m = request.FILES['doc']
				print m
				f = open(m, 'r')
				print f.readline()
				
				site_content = ''
			except:
				site_content = ''
	else:
		site_content = ''
		
	zipped_counter = zip(site_content_keys, site_content_values)
	
	c = {
			'mined_data': site_content,
			'zipped_counter': zipped_counter
		}
	
	return render(request, 'data/index.html', c)