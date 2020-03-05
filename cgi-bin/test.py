import re
import html
import os
import urllib.parse
from html import escape
import codecs
from urllib.parse import unquote

def application(environ, start_response):

    start_response('200 OK', [('Content-Type', 'text/html')])

    f = open("text1.html","r",encoding="utf-8")

    b = f.read()

    # the environment variable CONTENT_LENGTH may be empty or missing
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    # When the method is POST the query string will be sent
    # in the HTTP request body which is passed by the WSGI server
    # in the file like wsgi.input environment variable.
    request_body = environ['wsgi.input'].read(request_body_size)
    request_body = str(request_body, encoding="utf-8")
    request_body = unquote(request_body, encoding="GBK")
    d = urllib.parse.parse_qs(request_body,encoding='utf-8')
    if len(d)>=1:
        inputStr = d.get('inputStr', [''])[0]  # Returns the first age value.
        #inputStr = str(inputStr, encoding="utf-8")
        inputStr = html.unescape(inputStr)
        print(inputStr)
    else:
        inputStr = "null"
    #hobbies = d.get('hobbies', [])  # Returns a list of hobbies.
    # Always escape user input to avoid script injection

    hobbies = ['a','b']
    print('before:',inputStr)
    inputStr = escape(inputStr)
    print('after:',inputStr)
    print('type:',type(inputStr))
    hobbies = [escape(hobby) for hobby in hobbies]

    body = re.sub("{tittle}",'python Web',b)

    body1 = re.sub("{content}",'hello pyweb!',body)

    #age = "33"
    #hobbies = ['a', 'b']
    #inputStr = bytes(inputStr, encoding="utf8")
    body1 = body1 % (inputStr or 'Empty',
                            '<br>'.join(hobbies or ['No Hobbies']))
    print('bodyType',type(body1))
    print(body1)
    f.close()

    return [body1.encode()]