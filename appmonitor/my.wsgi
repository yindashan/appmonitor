import os, sys
#sys.path.append('d:\wamp\www\mypthon')
import newrelic.agent
newrelic.agent.initialize('/var/backup/newrelic.ini')

sys.path.append('/var/www/html/appmonitor')
os.environ['DJANGO_SETTINGS_MODULE'] = 'appmonitor.settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
application = newrelic.agent.wsgi_application()(application)

