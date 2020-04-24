style=prose
gunicorn service_prose:app -c gunicorn_prose.conf

style=gou
gunicorn service_prose:app -c gunicorn_gou.conf

#ps -ef|grep gunicorn_prose|grep -v grep|awk  '{print "kill -9 " $2}' |sh