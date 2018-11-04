# -*- coding:utf-8 -*-
from flask import abort
from flask import Flask, jsonify
from flask import request, redirect, url_for
from flask import send_file, send_from_directory
from flask import make_response
import baidu as baidu
import dbAPI as dbAPI
from flask import Response
import os
app = Flask(__name__)
# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
# def get_task(task_id):
#     task = filter(lambda t: t['id'] == task_id, tasks)
#     if len(task) == 0:
#         abort(404)
#     return jsonify({'task': task[0]})

# @app.route('/large.csv')
# def generate_large_csv():
#     def generate():
#         for row in iter_all_rows():
#             yield ','.join(row) + '\n'
#     return Response(generate(), mimetype='text/csv')



# @app.route('/a', methods=['POST'])
# def getPara():
#     value = request.values.get('newtext', 0)
#     print(value)
#     return value

#download/[fileformat]/[tablename]
@app.route('/download/<string:fileFormat>/<string:tablename>', methods=['get'])
def downloadfile(fileFormat,tablename):
    if(dbAPI.exportToFile(tablename)):
        if(fileFormat=='csv' or fileFormat=='xls'):
            return send_from_directory('results', ''+tablename+'.'+fileFormat, as_attachment=True)
    return make_response(jsonify({'error': 'Not found'}), 404)
   



#搜索
@app.route('/search/<string:keyword>', methods=['GET'])
def search(keyword):
    baidu.getfromBaidu(keyword)
    rst = make_response("doing")
    rst.headers['Access-Control-Allow-Origin'] = '*' #任意域名
    return rst


# return number
@app.route('/result/<string:keyword>', methods=['GET'])
def getresultcount(keyword):
    rst = make_response(str(baidu.getresultcount(keyword)))
    rst.headers['Access-Control-Allow-Origin'] = '*' #任意域名
    return rst


# return all
@app.route('/SearchRecords', methods=['GET'])
def getSearchRecords():
    rst=make_response(dbAPI.getSearchRecords())
    rst.headers['Access-Control-Allow-Origin'] = '*' #任意域名
    return rst

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
