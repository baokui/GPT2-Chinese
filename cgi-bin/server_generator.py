from wsgiref.simple_server import make_server
import sys
# 导入我们自己编写的application函数:
from Application import application

# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
if __name__=="__main__":
    port = int(sys.argv[1])
    httpd = make_server('', port, application)
    print("Serving HTTP on port %s..."%port)

# 开始监听HTTP请求:

httpd.serve_forever()