# -*- encoding: utf-8 -*-
from flask import Flask, request, Response
import json
import numpy as np
import gpt_gen
import sys
from datetime import datetime
import logging
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
port = 5000
style = 0#0大白狗, 1散文
if len(sys.argv)>1:
   port = int(sys.argv[1])
num0 = [10,3]
path_next = 'nnlm/D_next.json'
path_simi = 'nnlm/D_simi.json'
D_simi = json.load(open(path_simi,'r',encoding='utf-8'))
D_next = json.load(open(path_next,'r',encoding='utf-8'))
D_simi = {k:json.loads(D_simi[k]) for k in D_simi}
D_next = {k:json.loads(D_next[k]) for k in D_next}
@app.route('/api/gen', methods=['POST'])
def test2():
    r = request.json
    data = r["input"]
    if "num" in r:
        num = r["num"]
    else:
        num = 5
    quick = False
    if "quick" in r:
        print("quick pattern")
        if r["quick"]=="True":
            quick = True
    app.logger.info(data)
    try:
        now = datetime.now()
        app.logger.info('time: {}'.format(now))
        result = gpt_gen.nnlm_modelpredict(D_simi,D_next,inputStr=[data],maxNext=num,maxChoice=10)[0]
        then = datetime.now()
        app.logger.info('time: {}'.format(then))
        #app.logger.info('time for : {}'.format(then - now))
        app.logger.info("input:{}".format(data))
        app.logger.info("output:\n{}".format('\n'.join(result)))
        response = {'message':'success','input':data,'result': result}
    except Exception as e:
        app.logger.error("error:",e)
        response = {'message': 'error', 'input': data, 'result': None}
    response_pickled = json.dumps(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
