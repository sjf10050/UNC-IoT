# -*- coding:utf-8 -*-
from flask import abort
from flask import Flask, jsonify
from flask import make_response
import baidu as baidu
app = Flask(__name__)

# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
# def get_task(task_id):
#     task = filter(lambda t: t['id'] == task_id, tasks)
#     if len(task) == 0:
#         abort(404)
#     return jsonify({'task': task[0]})

@app.route('/a/<string:num>', methods=['GET'])
def getnum(num):
    print('a: '+num)
    return num

# return number 
@app.route('/result/<string:keyword>', methods=['GET'])
def getresultcount(keyword):
    count=baidu.getresultcount(keyword)
    return jsonify({'count':count})



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)