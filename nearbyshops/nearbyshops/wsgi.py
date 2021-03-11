import os
from django.core.wsgi import get_wsgi_application

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yoursbook.settings')
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yoursbook.settings.development")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nearbyshops.settings.production")


application = get_wsgi_application()

from whitenoise import WhiteNoise
application = WhiteNoise(application)

