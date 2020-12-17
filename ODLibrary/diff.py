# encoding: utf-8
"""
@author: fonttian
@contact: fonttian@gmail.com
@license: by-nc-sa
@file: diff.py
@time: 2020/12/1 上午9:38
"""
from Tools.RequestsTools import request_to_java
from Tools.Sqlite3Manager import getResultDiff
from Tools import dict_sensor_type


def real_time_diff_detect(list_real_time_data, connect, parameter_dict_sensor_type=dict_sensor_type):
    cursor = connect.cursor()
    r = cursor.execute(
        "SELECT sensor_id,last_data FROM sensor_last_data where sensor_id='" + list_real_time_data[0][0] + "';")
    r = r.fetchall()
    if not r:
        cursor.executemany("INSERT INTO sensor_last_data VALUES(?,?)", list_real_time_data)
        connect.commit()
        return {"status": "successful", "content": "Initializes the data in the difference database",
                "function": "real_time_diff_detect"}, 201
    else:
        last_data = [[item[0], item[1]] for item in r][-1]

        # delete old data and insert new data
        # cursor.execute("delete FROM sensor_last_data where sensor_id='" + list_real_time_data[0][0] + "';")
        # cursor.executemany("INSERT INTO sensor_last_data VALUES(?,?)", list_real_time_data)
        for item in list_real_time_data:
            cursor.execute("UPDATE sensor_last_data SET value = '" + item[1] + "' metadata WHERE sensor_id = '"+ item[0]+"'")
        connect.commit()

        # get diff
        now_diff = float(list_real_time_data[0][1]) - float(last_data[1])

        # get result
        sensor_type = parameter_dict_sensor_type[list_real_time_data[0][0].split(":")[3]]

        if now_diff == 0:
            return None
        else:
            result = getResultDiff(cursor, sensor_type=sensor_type, diff=now_diff, close_cursor=False)

        cursor.close()
        connect.commit()
        # Record the data
        if result == -1:
            request_to_java(bigType="701", smallType="-1", data=list_real_time_data[0][1],
                            sensorId=list_real_time_data[0][0], strategy="diff")
            return {"status": "successful", "content": "Data diff smaller than threshold",
                    "function": "db_select_diff_single"}, 200
        elif result == 1:
            return {"status": "successful", "content": "data diff larger than the threshold",
                    "function": "db_s"
                                "elect_diff_single"}, 200
        elif isinstance(result, str):
            request_to_java(bigType="701", smallType="1", data=list_real_time_data[0][1],
                            sensorId=list_real_time_data[0][0], strategy="diff")
            return {"status": "failed",
                    "content": "The data of " + result + " does not exist in the difference table",
                    "function": "db_select_diff_single"}, 603
        else:
            return None
