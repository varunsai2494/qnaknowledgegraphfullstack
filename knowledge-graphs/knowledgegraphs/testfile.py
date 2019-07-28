import requests
import json
# the word you want to search for
# cka=["acceptable","ace","admirable","agreeable","bad","boss","bully","capital","choice","commendable","congenial","crack","deluxe","excellent","exceptional","favorable","first-class","first-rate","gnarly","gratifying","great","honorable","marvelous","neat","nice","pleasing","positive","precious","prime","rad","reputable","satisfactory","satisfying","select","shipshape","sound","spanking","splendid","sterling","stupendous","super","super-eminent","super-excellent","superb","superior","tip-top","up to snuff","valuable","welcome","wonderful","worthy"]
# dfg=[]
# print cka
# for item in cka:
#     GL=[str(item)]
#     goodlist=[]
#     # increase the count and get more synonyms
#     count=2
#     for item in range(count):
#         print item
#         goodlist=list(set(GL))
#         for j in goodlist:
#             if " " not in j:
#                 urlg= "http://words.bighugelabs.com/api/2/83d0640747929c9e6b5ae66a2d24ca38/"+str(j)+"/json"
#                 result=requests.get(url=urlg)
#                 a= result.json()
#                 for i in a.keys():
#                     if "syn" in a[str(i)]:
#                         GL=GL+a[str(i)]["syn"]
#     finallist=list(set([str(i) for i in GL]))
#     dfg=dfg+finallist
#     print dfg
# print dfg


# import pandas as pd
# import ezodf
#
# def read_ods(filename, sheet_no=0, header=0):
#     tab = ezodf.opendoc(filename=filename).sheets[sheet_no]
#     return pd.DataFrame({col[header].value:[x.value for x in col[header+1:]]
#                          for col in tab.columns()})
#
# a = read_ods("export_3.ods")
# print a._get_values
# for i in a:
#     print a
import traceback
from flask import Flask, request
import app
import qaSystem
from flask_cors import CORS, cross_origin
appf = Flask(__name__, static_url_path='')
CORS(appf)
@appf.route('/updategraph', methods=['GET', 'POST'])
def updategraph():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            if "text" in data:
                output=app.updateNode(str(data["text"]).replace('"',''))
                if output:
                    return json.dumps({"text":output})
                else:
                    return json.dumps({"text": "fail"})
            else:
                return json.dumps({"text": "fail"})
        except Exception as e:
            return json.dumps({"text": "fail"})


@appf.route('/')
def root():
    return appf.send_static_file('index.html')



@appf.route('/qna', methods=['GET', 'POST'])
def qna():
    if request.method == 'POST':
        try:
            data =json.loads(request.data)
            print data
            if "text" in data:
                output=qaSystem.finalOutput(qaSystem.stringfilter(str(data["text"]).replace('"','') ))
                if output:
                    return json.dumps({"text":output})
                else:
                    return json.dumps({"text":"Sorry I couldn't find what you were looking for"})
            else:
                return json.dumps({"text": "Sorry I couldn't find what you were looking for"})
        except Exception as e:
            return json.dumps({"text": "Sorry I couldn't find what you were looking for"})




if __name__ == '__main__':
    appf.run(host="0.0.0.0", port=8000,debug=True, threaded=True)

