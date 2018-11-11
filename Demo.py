import requests


def add(a, b):
    return a+b


def minus(a, b):
    return a-b


def multi(a, b):
    return a*b


def divide(a, b):
    return a/b

sckey='SCU24427Ta543f1d5bec4681a4e437877374ae1605ac9a9f0e79d0'

def get_out_ip():
    url = r'http://www.trackip.net/'
    r = requests.get(url)
    txt = r.text
    ip = txt[txt.find('title')+6:txt.find('/title')-1]
    return (ip)

print(get_out_ip())



