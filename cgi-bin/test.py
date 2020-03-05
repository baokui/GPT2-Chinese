import re

import os

import codecs

def application(environ, start_response):

    start_response('200 OK', [('Content-Type', 'text/html')])

    f = open("text.html","r",encoding="utf-8")

    b = f.read()

    body = re.sub("{tittle}",'python Web',b)

    body1 = re.sub("{content}",'hello pyweb!',body)

    f.close()

    return [body1.encode()]