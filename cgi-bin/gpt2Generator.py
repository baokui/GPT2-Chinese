#!/root/anaconda3/envs/tf36/bin/python3.6
# -*- coding: utf-8 -*-
# Date: 2020-03-05

#db = MySQLdb.connect("mt.tugele.rds.sogou", "tugele_new", "tUgele2017OOT", "tugele", use_unicode=True, charset="utf8")
#r = redis.Redis(host="d.redis.sogou", port=2303, password="WNnAddgLR7hIHQdp")

header = 'Content-Type: text/html; charset=utf-8'
print(header)
print()
print("<style type=text/css>")
print("#left{width:33%;float:left}")
print("#center{width:50%;float:left}")
print("#right{width:50%;float:left}")
print("</style>")
def Slove():
    #query, page, num,refer ,textLine,textNum,device,tagType,groupId = Get_params()
    #Get_headval(query,page,num,refer)
    #Get_headval(query,page,num,refer,textLine,textNum,device,tagType,groupId)

   # print "<div float:left><b>分词：</b>", getDataFenci(query),"</div>"
   # response = getData(query, page, num,refer,userid,textNum,device,tagType,gp, "http://10.144.121.185/search")
    #print "<div id='left'>"
    #print "<h2>新框架(185)</h2>"
    #print_debug_info(response)
    #print "</div>"

    #response = getData(query, page, num,refer,textLine,textNum,device,tagType,groupId, "http://yunbiaoqing-vpatemplate.venus.odin.sogou/template")
    print("<div id='center'>")
    print("<h2>线上（yunbiaoqing-vpatemplate.venus.odin.sogou）</h2>")
    #print_debug_info(response)
    print("</div>")
    print("<div id='right'>")
    print("<h2>测试(10.142.68.85)</h2>")
    #response = getData(query, page, num,refer,textLine,textNum,device,tagType,groupId,"http://10.142.68.85/template")
    #print_debug_info(response)
    print("</div>")
   
if __name__ == "__main__":
    Slove()
    #except Exception, e:
        #print(e, "<br>")
        #print(traceback.format_exc(), "<br>")
