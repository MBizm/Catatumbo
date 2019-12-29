'''
Created on 28.12.2019

@author: D040447
'''
import urllib
import re
import urllib3
import requests

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