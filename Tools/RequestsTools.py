# encoding: utf-8
"""
@author: fonttian
@contact: fonttian@gmail.com
@license: by-nc-sa
@file: RequestsTools.py
@time: 2020/12/2 下午5:34
"""
import requests

from Tools.Sqlite3Manager import metadata_select_url


def request_to_java(bigType, smallType, data, sensorId, strategy,
                    url="http://192.168.1.113:8094/gxzy-sr/exception/add", get_response=False):
    payload = "{\"bigType\":\"" + bigType + "\",\"smallType\":\"" + smallType + "\",\"data\":\"" + data + "\",\"sensorId\":\"" + sensorId + "\",\"strategy\":\"" + strategy + "\"} "
    headers = {
        'Content-Type': 'application/json'
    }
    diff_url = metadata_select_url("diff_url")[-1][0]
    if diff_url is not None:
        url = diff_url

    if get_response:
        return requests.request("POST", url, headers=headers, data=payload)
    else:
        requests.request("POST", url, headers=headers, data=payload)
