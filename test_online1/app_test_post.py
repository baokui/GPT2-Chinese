import requests
import time
import sys
def main(data):
    user_info = {"input":data}
    T0 = time.asctime(time.localtime(time.time()))
    r = requests.post("http://127.0.0.1:7000/api/gen_test", data=user_info)
    T1 = time.asctime(time.localtime(time.time()))
    s = r.text+'\t'+'post-time:'+T0[11:19]+'->'+T1[11:19]
    print(s)
if __name__=="__main__":
    data = sys.argv[1]
    main(data)