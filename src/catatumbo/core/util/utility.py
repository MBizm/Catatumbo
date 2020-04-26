'''
Created on 28.12.2019

@author: D040447
'''
import re
import requests
import pytz

from datetime import datetime

"""
    converts a number to the representation in a defined base
""" 
def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

"""
    resolves the external IP address of local machine
    we rely on an external service to reflect the IP
    
    https://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address-with-python
"""
def getExternalIPAddress():
    site = requests.get("http://checkip.dyndns.org/")
    grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site.text)
    return grab[0]

"""
    returns whether a given date is in daylight saving time
    
    https://stackoverflow.com/questions/2881025/python-daylight-savings-time
"""
def is_dst(dt=None, timezone="UTC"):
    if dt is None:
        dt = datetime.utcnow()
    timezone = pytz.timezone(timezone)
    timezone_aware_date = timezone.localize(dt, is_dst=None)
    return timezone_aware_date.tzinfo._dst.seconds != 0