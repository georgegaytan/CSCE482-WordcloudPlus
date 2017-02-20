"""
WSGI config for wordcloudplus project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#from dj_static import Cling						#added for heroku

#application = Cling(get_wsgi_application())		#added for heroku

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wordcloudplus.settings")

application = get_wsgi_application()
