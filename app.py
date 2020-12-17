# encoding: utf-8
"""
@author: fonttian
@contact: fonttian@gmail.com
@license: by-nc-sa
@file: app.py
@time: 2020/11/9 上午8:47
"""
import sqlite3
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename

from ODLibrary.diff import real_time_diff_detect
from Tools.ExceptionHandler import exceptionHandler
from Tools.Sqlite3Manager import db_insert_diff, db_delete_diff, db_insert_diff_single, db_delete_diff_single, \
    db_select_diff, \
    db_select_diff_single, db_select_diff_all

app = Flask(__name__)


# 默认主页
@app.route('/')
def home():
    return render_template("README.html"), 200


# 检测模块
@app.route('/thinker/hello', methods=['GET', 'POST'])  # localhost:8086/ins/json为申请的url地址，此处表示采用get和post请求
def hello():
    return {"status": "running"}, 200


# 初始化模块
@app.route('/thinker/init/database/post/sensor_last_data', methods=['POST'])
def init_database_sensor_last_data():
    connect = sqlite3.connect('./resources/diff.db')
    cursor = connect.cursor()
    cursor.execute("create table if not exists sensor_last_data(sensor_id text,last_data text)")
    cursor.close()
    connect.commit()


@app.route('/thinker/init/database/post/sec_diff', methods=['POST'])
def init_database_sec_diff():
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        sql_create_sec_diff = "create table if not exists sec_diff (type_name text,diff text);"
        cursor.execute(sql_create_sec_diff)
        db_insert_diff(request.json['data'], cursor)
        cursor.close()
        connect.commit()
        connect.close()
        return jsonify({"status": "successful", "content": "Database initialization succeeded",
                        "function": "init_database_sec_diff"}), 200
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return jsonify(list_tmp[0]), list_tmp[1]


@app.route('/thinker/init/database/local/sec_diff/', methods=['get'])
def init_database_sec_diff_local():
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()

        sql_create_sec_diff = "create table if not exists sec_diff (type_name text,diff text);"
        cursor.execute(sql_create_sec_diff)
        with open('./resources/diff.csv', 'r') as f:
            list_tmp = f.readlines()

        list_real_data = [item.replace("\n", "").split(",") for item in list_tmp]
        del list_tmp
        db_insert_diff(list_real_data, cursor)
        del list_real_data
        cursor.close()
        connect.commit()
        connect.close()
        return jsonify({"status": "successful", "content": "Database initialization succeeded",
                        "function": "init_database_sec_diff_local"}), 200
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return jsonify(list_tmp[0]), list_tmp[1]


# 文件管理模块
## 上传文件
@app.route('/thinker/file/upload', methods=['POST'])
def file_upload():
    try:
        file = request.files['file']
        file_path = "./resources/" + secure_filename(file.filename)
        import os
        if os.path.exists(file_path):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            os.remove(file_path)
        file.save(file_path)
        return jsonify({"status": "successful", "content": "File upload successful", "function": "file_upload"}), 200
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return jsonify(list_tmp[0]), list_tmp[1]


@app.route('/thinker/file/delete', methods=['POST'])
def file_delete():
    try:
        file = request.files['file']
        file_path = "./resources/" + secure_filename(file.filename)
        import os
        if os.path.exists(file_path):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            os.remove(file_path)
        return jsonify({"status": "successful", "content": "File deleted successful", "function": "file_delete"}), 200
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return jsonify(list_tmp[0]), list_tmp[1]


## 模型更新
@app.route('/thinker/mode/upload', methods=['POST'])
def mode_upload():
    try:
        file = request.files['model']
        file_path = "./ModelLibrary/" + secure_filename(file.filename)
        import os
        if os.path.exists(file_path):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            os.remove(file_path)
        file.save(file_path)
        return jsonify({"status": "successful", "content": "File upload successful", "function": "mode_upload"}), 200
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return jsonify(list_tmp[0]), list_tmp[1]


# 模型删除
@app.route("/thinker/model/delete", methods=['GET'])
def model_delete():
    try:
        path_model_path = "./ModelLibrary/" + request.json["modelName"] + '.pkl'
        import os
        if os.path.exists(path_model_path):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            os.remove(path_model_path)
        return jsonify(
            {"status": "successful", "content": "Model deleted successfully", "function": "model_delete"}), 200
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return jsonify(list_tmp[0]), list_tmp[1]


# 数据库管理
@app.route('/thinker/database/sec_diff/insert', methods=['post'])
def database_sec_diff_insert():
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        db_insert_diff(request.json['data'], cursor, True)
        connect.commit()
        connect.close()
        return jsonify({"status": "successful", "content": "Data insertion successful",
                        "function": "database_sec_diff_insert"}), 200
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return jsonify(list_tmp[0]), list_tmp[1]


@app.route('/thinker/database/sec_diff/insert_single', methods=['post'])
def database_sec_diff_insert_single():
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        db_insert_diff_single(request.json['data'], cursor, True)
        connect.commit()
        connect.close()
        return jsonify({"status": "successful", "content": "Single data inserted successfully",
                        "function": "database_sec_diff_insert_single"}), 200
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return jsonify(list_tmp[0]), list_tmp[1]


@app.route('/thinker/database/sec_diff/delete', methods=['post'])
def database_sec_diff_delete():
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        db_delete_diff(request.json['data'], cursor, True)
        connect.commit()
        connect.close()
        return jsonify({"status": "successful", "content": "Data deletion successful",
                        "function": "database_sec_diff_delete"}), 200
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return jsonify(list_tmp[0]), list_tmp[1]


@app.route('/thinker/database/sec_diff/delete_single', methods=['post'])
def database_sec_diff_delete_single():
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        db_delete_diff_single(request.json['data'], cursor, True)
        connect.commit()
        connect.close()
        return jsonify({"status": "successful", "content": "Single data deleted successfully",
                        "function": "database_sec_diff_delete_single"}), 200
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return jsonify(list_tmp[0]), list_tmp[1]


@app.route('/thinker/database/sec_diff/select', methods=['post'])
def database_sec_diff_select():
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        db_select_diff(request.json['data'], cursor, True)
        connect.commit()
        connect.close()
        return jsonify(
            {"status": "successful", "content": "Data query successful", "function": "database_sec_diff_select"}), 200
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return jsonify(list_tmp[0]), list_tmp[1]


@app.route('/thinker/database/sec_diff/select_single', methods=['post'])
def database_sec_diff_select_single():
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        db_select_diff_single(request.json['data'], cursor, True)
        connect.commit()
        connect.close()
        return jsonify({"status": "successful", "content": "Single data query successful",
                        "function": "database_sec_diff_select_single"}), 200
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return jsonify(list_tmp[0]), list_tmp[1]


@app.route('/thinker/database/sec_diff/select_all', methods=['post'])
def database_sec_diff_select_all():
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        result = db_select_diff_all(request.json['data'], cursor, True)
        connect.commit()
        connect.rollback()
        connect.close()
        return jsonify({"status": "successful", "content": "Data query successful",
                        "function": "database_sec_diff_select_all", "result": str(result)}), 200
    except Exception as err:
        return exceptionHandler(err)


# 检测模块
@app.route("/thinker/detect/joblib", methods=['GET'])
def detect_joblib():
    try:
        file_path = "./ModelLibrary/" + request.json["modelName"] + '.pkl'
        from pathlib import Path
        import joblib
        clf = joblib.load(file_path)
        result = clf.predict(request["data"])
        return jsonify({"status": "successful", "content": "Data query successful", "function": "detect_joblib",
                        "result": str(result)}), 200
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return jsonify(list_tmp[0]), list_tmp[1]


# 检测模块
@app.route("/thinker/detect/diff", methods=['post'])
def detect_diff():
    try:
        connect = sqlite3.connect('./resources/diff.db')
        result = real_time_diff_detect(request.json['data'], connect=connect)
        connect.close()
        if result is None:
            return jsonify({"status": "successful", "content": "Detect data by Diff", "function": "detect_diff"}), 200
        else:
            return jsonify(result[0]), result[1]
    except Exception as err:
        print(err)
        list_tmp = exceptionHandler(err)
        if list_tmp[0]["exceptionContent"] == "no such table: sensor_last_data":
            connect = sqlite3.connect('./resources/diff.db')
            cursor = connect.cursor()
            cursor.execute("create table if not exists sensor_last_data(sensor_id text,last_data text)")
            cursor.close()
            connect.commit()
            real_time_diff_detect(request.json['data'], connect=connect)
        return jsonify(list_tmp[0]), list_tmp[1]


if __name__ == '__main__':
    from gevent import pywsgi

    server = pywsgi.WSGIServer(('0.0.0.0', 8120), app)
    server.serve_forever()
