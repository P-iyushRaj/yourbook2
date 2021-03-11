#helper function
from django.contrib.gis.geoip2 import GeoIP2
from geopy.geocoders import Nominatim
from ipware import get_client_ip

def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    return country, city, lat, lon

def get_destination(request):

    ip, is_routable = get_client_ip(request)
    if ip is None:
        ip_ = '2401:4900:36bf:e76b:b5bf:e254:883:ccac'
    else:
        if is_routable:
            ip_ = ip
        else:
            ip_ = '2401:4900:36bf:e76b:b5bf:e254:883:ccac'
    country, city, lat1, lon1= get_geo(ip_)
    lat1 = int(lat1)
    lon1 = int(lon1)
    #print( city )
    for key,value in city.items():
        if key == "postal_code":
            try:
                postal_code=value
                break
            except:
                break
    
    #print(postal_code)
    try:
        geolocator = Nominatim(user_agent= 'app' )

        destination = geolocator.geocode(postal_code)
        #print(destination)
    except:
        destination="Not Found"

    return destination, lat1, lon1


def unique_key_generator(instance):
  
    size = random.randint(30, 45)
    key = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_key_generator(instance)
    return key


def unique_otp_generator(instance):

    key = random.randint(1, 999999)
    print(key)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_otp_generator(instance)
    return key

import re
import random

def phone_validator(phone_number):
    """
    Returns true if phone number is correct else false
    """
    regix = r'^\+?1?\d{10}$'
    com = re.compile(regix)
    find = len(com.findall(phone_number))
    if find == 1:
        return True
    else:
        return False

def otp_generator():
    otp = random.randint(999, 9999)
    return otp
