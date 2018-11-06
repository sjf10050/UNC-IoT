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

@app.route('/download/<string:fileFormat>/<string:tablename>', methods=['get'])
def downloadfile(fileFormat, tablename):
    if(dbAPI.exportToFile(tablename)):
        if(fileFormat == 'csv' or fileFormat == 'xls'):
            return send_from_directory('results', ''+tablename+'.'+fileFormat, as_attachment=True)
    return make_response(jsonify({'error': 'Not found'}), 404)


# search
@app.route('/search/<string:keyword>', methods=['GET'])
def search(keyword):
    baidu.getfromBaidu(keyword)
    rst = make_response("doing")
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


# return number
@app.route('/result/<string:keyword>', methods=['GET'])
def getresultcount(keyword):
    rst = make_response(str(baidu.getresultcount(keyword)))
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@app.route('/DelResult/<string:tablename>', methods=['GET'])
def DelResult(tablename):
    dbAPI.DelResult(tablename)
    rst = make_response("doing")
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst

# return all


@app.route('/SearchRecords', methods=['GET'])
def getSearchRecords():
    rst = make_response(dbAPI.getSearchRecords())
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
