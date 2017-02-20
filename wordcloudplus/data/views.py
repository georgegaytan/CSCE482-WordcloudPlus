from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import mining

@csrf_exempt
def index(request):
	if request.method == 'POST':
		#print request.POST		#for testing / error handling
		site_content = mining.get_data_set(request.POST['address'])
	
	else:
		site_content = ''
		
	c = {'mined_data': site_content}
	
	return render(request, 'data/index.html', c)