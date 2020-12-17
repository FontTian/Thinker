# encoding: utf-8
"""
@author: fonttian
@contact: fonttian@gmail.com
@license: by-nc-sa
@file: main.py
@time: 2020/12/17 下午1:49
"""
import sqlite3

import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from werkzeug.utils import secure_filename

from ODLibrary.diff import real_time_diff_detect
from Tools.ExceptionHandler import exceptionHandler
from Tools.Sqlite3Manager import db_insert_diff, db_delete_diff, db_insert_diff_single, db_delete_diff_single, \
    db_select_diff, \
    db_select_diff_single, db_select_diff_all

tags_metadata = [
    {
        "name": "init",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "file",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "model",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "database",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "detect",
        "description": "Operations with users. The **login** logic is also here.",
    },
]

app = FastAPI(title="Thinker API",
              description="This is a very fancy project, with auto docs for the API and everything",
              version="0.2.0",
              openapi_tags=tags_metadata)


class RequestJSON(BaseModel):
    data: list


# 默认主页
@app.get('/')
def home():
    return JSONResponse(status_code=200, content={'Hello': 'Hello Word'})


# 检测模块
@app.get('/thinker/hello', )
def hello():
    return JSONResponse(status_code=200,
                        content={'status': 'running'})


# 初始化模块
@app.post('/thinker/init/database/sensor_last_data', tags=["init"])
def init_database_sensor_last_data(request_json: RequestJSON):
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        cursor.execute("create table if not exists sensor_last_data(sensor_id text,last_data text)")
        db_insert_diff(request_json.data, cursor)
        cursor.close()
        connect.commit()
        connect.close()
        return JSONResponse(status_code=200,
                            content=({"status": "successful", "content": "Database initialization succeeded",
                                      "function": "init_database_sec_diff"}))
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return JSONResponse(status_code=list_tmp[1],
                            content=(list_tmp[0]))


@app.post('/thinker/init/database/sec_diff', tags=["init"])
def init_database_sec_diff(request_json: RequestJSON):
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        cursor.execute("create table if not exists sec_diff (type_name text,diff text);")
        db_insert_diff(request_json.data, cursor)
        cursor.close()
        connect.commit()
        connect.close()
        return JSONResponse(status_code=200,
                            content=({"status": "successful", "content": "Database initialization succeeded",
                                      "function": "init_database_sec_diff"}))
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return JSONResponse(status_code=list_tmp[1],
                            content=(list_tmp[0]))


@app.post('/thinker/init/database/local/sec_diff/', tags=["init"])
def init_database_sec_diff_local():
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()

        cursor.execute("create table if not exists sec_diff (type_name text,diff text);")
        with open('./resources/diff.csv', 'r') as f:
            list_tmp = f.readlines()

        list_real_data = [item.replace("\n", "").split(",") for item in list_tmp]
        del list_tmp
        db_insert_diff(list_real_data, cursor)
        del list_real_data
        cursor.close()
        connect.commit()
        connect.close()
        return JSONResponse(status_code=200,
                            content={"status": "successful", "content": "Database initialization succeeded",
                                     "function": "init_database_sec_diff_local"})

    except Exception as err:
        list_tmp = exceptionHandler(err)
        return JSONResponse(status_code=list_tmp[1],
                            content=(list_tmp[0]))


@app.put('/thinker/file/upload/{filename}', tags=["file"])
async def file_upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_path = "./resources/" + secure_filename(file.filename)
        with open(file_path, 'wb') as f:
            f.write(contents)

        return JSONResponse(status_code=200,
                            content={"status": "successful", "content": "File upload successful",
                                     "function": "file_upload"})
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return JSONResponse(status_code=list_tmp[1],
                            content=(list_tmp[0]))


@app.delete('/thinker/file/delete/{filename}', tags=["file"])
def file_delete(filename: str):
    try:
        import os
        if os.path.exists("./resources/" + filename):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            os.remove("./resources/" + filename)
        return JSONResponse(status_code=200, content={"status": "successful", "content": "File deleted successful",
                                                      "function": "file_delete"})
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return JSONResponse(status_code=list_tmp[1],
                            content=(list_tmp[0]))


@app.get('/thinker/mode/upload', tags=["model"])
async def mode_upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_path = "./ModelLibrary/" + secure_filename(file.filename)
        with open(file_path, 'wb') as f:
            f.write(contents)

        return JSONResponse(status_code=200,
                            content={"status": "successful", "content": "Model upload successful",
                                     "function": "mode_upload"})
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return JSONResponse(status_code=list_tmp[1],
                            content=(list_tmp[0]))


# 模型删除
@app.delete("/thinker/model/delete/{modelName}", tags=["model"])
def model_delete(modelName: str):
    try:
        path_model_path = "./ModelLibrary/" + modelName + '.pkl'
        import os
        if os.path.exists(path_model_path):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            os.remove(path_model_path)
        return JSONResponse(status_code=200, content={"status": "successful", "content": "Model deleted successfully",
                                                      "function": "model_delete"})
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return JSONResponse(status_code=list_tmp[1],
                            content=(list_tmp[0]))


# 数据库管理
@app.put('/thinker/database/insert/sec_diff', tags=["database"])
def database_sec_diff_insert(request_json: RequestJSON):
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        db_insert_diff(request_json.data, cursor, True)
        connect.commit()
        connect.close()
        return JSONResponse(status_code=200, content={"status": "successful", "content": "Data insertion successful",
                                                      "function": "database_sec_diff_insert"})
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return JSONResponse(status_code=list_tmp[1],
                            content=(list_tmp[0]))


@app.put('/thinker/database/single_insert/sec_diff', tags=["database"])
def database_sec_diff_insert_single(request_json: RequestJSON):
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        db_insert_diff_single(request_json.data, cursor, True)
        connect.commit()
        connect.close()
        return JSONResponse(status_code=200,
                            content={"status": "successful", "content": "Single data inserted successfully",
                                     "function": "database_sec_diff_insert_single"})
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return JSONResponse(status_code=list_tmp[1],
                            content=(list_tmp[0]))


@app.delete('/thinker/database/delete/sec_diff', tags=["database"])
def database_sec_diff_delete(request_json: RequestJSON):
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        db_delete_diff(request_json.data, cursor, True)
        connect.commit()
        connect.close()
        return JSONResponse(status_code=200, content={"status": "successful", "content": "Data deletion successful",
                                                      "function": "database_sec_diff_delete"})
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return JSONResponse(status_code=list_tmp[1],
                            content=(list_tmp[0]))


@app.delete('/thinker/database/sec_diff/delete_single', tags=["database"])
def database_sec_diff_delete_single(request_json: RequestJSON):
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        db_delete_diff_single(request_json.data, cursor, True)
        connect.commit()
        connect.close()
        return JSONResponse(status_code=200,
                            content={"status": "successful", "content": "Single data deleted successfully",
                                     "function": "database_sec_diff_delete_single"})
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return JSONResponse(status_code=list_tmp[1],
                            content=(list_tmp[0]))


@app.get('/thinker/database/select/sec_diff', tags=["database"])
def database_sec_diff_select(request_json: RequestJSON):
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        db_select_diff(request_json.data, cursor, True)
        connect.commit()
        connect.close()
        return JSONResponse(status_code=200, content={"status": "successful", "content": "Data query successful",
                                                      "function": "database_sec_diff_select"})
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return JSONResponse(status_code=list_tmp[1],
                            content=(list_tmp[0]))


@app.get('/thinker/database/single_select/sec_diff', tags=["database"])
def database_sec_diff_select_single(request_json: RequestJSON):
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        db_select_diff_single(request_json.data, cursor, True)
        connect.commit()
        connect.close()
        return JSONResponse(status_code=200, content={"status": "successful", "content": "Single data query successful",
                                                      "function": "database_sec_diff_select_single"})
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return JSONResponse(status_code=list_tmp[1],
                            content=(list_tmp[0]))


@app.get('/thinker/database/sec_diff/select_all', tags=["database"])
def database_sec_diff_select_all(request_json: RequestJSON):
    try:
        connect = sqlite3.connect('./resources/diff.db')
        cursor = connect.cursor()
        result = db_select_diff_all(request_json.data, cursor, True)
        connect.commit()
        connect.rollback()
        connect.close()
        return JSONResponse(status_code=200, content={"status": "successful", "content": "Data query successful",
                                                      "function": "database_sec_diff_select_all",
                                                      "result": str(result)})
    except Exception as err:
        return exceptionHandler(err)


# 检测模块
@app.get("/thinker/detect/joblib/{modelName}", tags=["detect"])
def detect_joblib(request_json: RequestJSON, modelName: str):
    try:
        file_path = "./ModelLibrary/" + modelName + '.pkl'
        from pathlib import Path
        import joblib
        clf = joblib.load(file_path)
        result = clf.predict(request_json)
        return JSONResponse(status_code=200, content={"status": "successful", "content": "Data query successful",
                                                      "function": "detect_joblib",
                                                      "result": str(result)})
    except Exception as err:
        list_tmp = exceptionHandler(err)
        return JSONResponse(status_code=list_tmp[1],
                            content=(list_tmp[0]))


# 检测模块
@app.get("/thinker/detect/diff/{data}", tags=["detect"])
def detect_diff(request_json: RequestJSON):
    try:
        connect = sqlite3.connect('./resources/diff.db')
        result = real_time_diff_detect(request_json.data, connect=connect)
        connect.close()
        if result is None:
            return JSONResponse(status_code=200,
                                content={"status": "successful", "content": "Detect data by Diff",
                                         "function": "detect_diff"})
        else:
            return JSONResponse(status_code=result[1], content=result[0]), result[1]
    except Exception as err:
        print(err)
        list_tmp = exceptionHandler(err)
        if list_tmp[0]["exceptionContent"] == "no such table: sensor_last_data":
            connect = sqlite3.connect('./resources/diff.db')
            cursor = connect.cursor()
            cursor.execute("create table if not exists sensor_last_data(sensor_id text,last_data text)")
            cursor.close()
            connect.commit()
            real_time_diff_detect(request_json.data, connect=connect)
        return JSONResponse(status_code=list_tmp[1], content=list_tmp[0])


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="0.0.0.0", port=8120, reload=True, debug=True)
