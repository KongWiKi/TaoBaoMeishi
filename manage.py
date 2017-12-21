'''
@author：KongWeiKun
@file: manage.py
@time: 17-12-21 上午11:36
@contact: 836242657@qq.com
'''
from  flask import Flask,render_template,request,session,g,redirect,url_for,abort,flash
from bson import json_util
from bson.objectid import  ObjectId
import json
import pymongo

con=pymongo.MongoClient('localhost',27017)
db=con['taobao']
accunt=db.get_collection('product')
app=Flask(__name__)


def toJson(data):
    return json.dumps(data,default=json_util.default,ensure_ascii=False)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.route('/',methods=['GET'])
def index():
    if request.method == 'GET':
        total = accunt.find().count()
        return render_template('index.html',total=total)


@app.route('/search',methods=['GET'])
@app.route('/search/<item>',methods=['GET'])
def get_goods(item = None):
    if request == "POST":
        pass
        #对展示的页面进行限制
    page = request.args.get('page',1,type=int)
    limit = request.args.get('limit',30,type=int)
    p = (page - 1)*limit
    offset = request.args.get('offset',p,type=int)
    catid = request.args.get('catid',None,type=str)
    jsons = request.args.get('json','off')
    keyword = request.args.get('key','')

    if not keyword:
        keyword = item

    if catid:
        cursor = accunt.find({'location':catid})
    else:
        cursor = accunt.find({'title':{'$regex':keyword}}) #模糊查询
    results = cursor.skip(offset).limit(limit)
    resultList = []
    for result in results:
        resultList.append(result)
    if jsons == 'off':
        return render_template('search.html', entries=resultList)
    else:
        return toJson(resultList)


if __name__ == '__main__':
    # print(db.collection_names())#获取聚集列表
    # print(accunt.find_one())#查看聚集的一条记录
    # print(accunt.find_one().keys())#查看聚集的所有key
    # print(accunt.find().count())#查看记录总数
    # cursors = accunt.find({'title': {'$regex': '零食'}})
    # results = cursors.skip(1).limit(2)
    # resultList = []
    # for result in results:
    #     resultList.append(result)
    # print(resultList)

    # for cursor in cursors:
    #     print(cursor)
    app.run(debug=True)
