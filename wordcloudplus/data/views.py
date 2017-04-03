from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import mining
from lxml import html, etree
from lxml.html.clean import clean_html
from data.models import Docs
import textract

@csrf_exempt
def index(request):
	site_content_keys = []
	site_content_values = []
	wordcloud_object_dict = {}
	
	if request.method == 'POST':
		print request.POST		#for testing / error handling
		
		#Stores file in database
		#then reads file
		#then deletes file
		if request.POST['file_upload']:
			file=request.FILES['doc']
		# 	print file.name
			
			instance = Docs(	file=request.FILES['doc'],
								title = 'temp',
							)
			instance.save()

			file_name = file.name
			file_name = file_name.replace(" ", "_")
			path = 'uploads/' + file_name
			
			text = textract.process(path)
			print text
			instance.delete()
			
		else:
			#site_content, site1_percentage, site2_percentage
			wordcloud_object_dict = mining.get_data_set(request.POST.getlist('addresses'))
			
		
		'''
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
		'''

	#output testing
	# print 'site_content' + str(wordcloud_object_dict['site_content'])
	# print 'site1_percentage' + str(wordcloud_object_dict['site1_percentage'])
	# print 'site2_percentage' + str(wordcloud_object_dict['site2_percentage'])

	return render(request, 'data/index.html', wordcloud_object_dict)
