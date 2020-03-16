from wsgiref.simple_server import make_server
import sys
# 导入我们自己编写的application函数:


# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
if __name__=="__main__":
    port = int(sys.argv[1])
    if len(sys.argv)>=3:
        mode = sys.argv[2]
        from Application import application_post as application
    else:
        mode = 'test'
        from Application_seg import application
    httpd = make_server('', port, application)
    print("Serving HTTP on port %s for %s..."%(port,mode))

# 开始监听HTTP请求:

httpd.serve_forever()