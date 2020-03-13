from maker_server_test import make_server
#from wsgiref.simple_server import make_server
import sys
import re
# 导入我们自己编写的application函数:
def application(env, start_response):
    s = env['PATH_INFO']
    #s = 'hh'
    start_response('200 OK', [('Content-Type', 'text/html'), ('X-Coder', 'Cooffeeli')])
    return ['<h1>'+s+'你好！！世界</h1>']
def application_post(environ, start_response):

    start_response('200 OK', [('Content-Type', 'text/html')])

    f = open("generating_post.html","r",encoding="utf-8")

    b = f.read()

    # the environment variable CONTENT_LENGTH may be empty or missing
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
        #modelidex, inputStr, nsamples = 0,"祝你",2

    body = re.sub("{tittle}",'python Web',b)

    body1 = re.sub("{content}",'hello pyweb!',body)
    print(environ)
    R = 'abc'
    R = environ['PATH_INFO']
    if "HTTP_REFERER" in environ:
        R += environ["HTTP_REFERER"]
    #age = "33"
    #hobbies = ['a', 'b']
    #inputStr = bytes(inputStr, encoding="utf8")
    body2 = body1 % R

    f.close()

    return [body2.encode()]

# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
if __name__=="__main__":
    port = 8001
    httpd = make_server('', port, application)
    httpd.handle_request()
    #print("Serving HTTP on port %s ..."%(port))

# 开始监听HTTP请求:

httpd.serve_forever()