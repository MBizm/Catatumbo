'''
Created on 28.12.2019

@author: D040447
'''

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