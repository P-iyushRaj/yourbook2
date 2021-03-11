from .base import *

import os
import psycopg2

SECRET_KEY = os.environ['SECRET_KEY']
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

#DEBUG = config('DEBUG', cast=bool)
DEBUG = False

ALLOWED_HOSTS = ['ip-address', 'www.your-website.com', 'yourbook4.herokuapp.com']
'''
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]
'''
#add config 
# cloudinary.config(
#   cloud_name = os.environ.get('dabxcx1wl'),
#   api_key = os.environ.get('496189617496236'),
#   api_secret = os.environ.get('04_oCzmd_qDfyTm2bp4jRgmXdyc'),
#   secure = True
# )


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'dfuefqg06k2g52',
        'USER': 'banazbzwjdhfbx',
        'PASSWORD': '4c1aa182116134b6583c7bbcf3e5d2703e2ff672e77da29177d446119a83782f',
        'HOST': 'ec2-100-25-231-126.compute-1.amazonaws.com',
        'PORT': '5432'
    }
}

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': ''
    }
}
'''

#STRIPE_PUBLIC_KEY = config('STRIPE_LIVE_PUBLIC_KEY')
STRIPE_SECRET_KEY = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
