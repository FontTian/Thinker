# encoding: utf-8
"""
@author: fonttian
@contact: fonttian@gmail.com
@license: by-nc-sa
@file: Sqlite3Manager.py
@time: 2020/11/20 下午3:46
"""
import sqlite3  # 驱动


def metadata_create_table():
    connect = sqlite3.connect('../resources/metadata.db')
    connect.execute("create table if not exists metadata (key text,value text);")
    connect.commit()
    connect.close()


def metadata_insert(key, value):
    connect = sqlite3.connect('../resources/metadata.db')
    connect.executemany("INSERT INTO metadata VALUES(?,?);", [[key, value]])
    connect.commit()
    connect.close()


def metadata_insert_url(value):
    connect = sqlite3.connect('../resources/metadata.db')
    connect.execute("UPDATE metadata SET value = '" + value + "' metadata WHERE key = 'diff_url'")
    connect.commit()
    connect.close()


def metadata_select_url(key):
    connect = sqlite3.connect('../resources/metadata.db')
    r = connect.execute("SELECT value FROM metadata where key =\"" + key + "\";")
    # 获取查询结果
    r = r.fetchall()
    connect.commit()
    connect.close()
    if not r:
        return None
    else:
        return r


def db_create_table():
    connect = sqlite3.connect('../resources/diff.db')
    connect.execute("create table if not exists metadata (key text,value text);")
    connect.commit()
    connect.close()


def db_select_diff(type_name_origin, cursor, close_cursor=False, database="sec_diff"):
    r = cursor.execute(
        "SELECT diff FROM " + database + " where type_name='" + type_name_origin + "Min' or type_name='" + type_name_origin + "Max';")
    # 获取查询结果
    r = r.fetchall()
    if close_cursor:
        cursor.close()
    if not r:
        return None
    else:
        return r[0][0], r[1][0]


def db_insert_diff(data, cursor, close_cursor=False, database="sec_diff"):
    for i in range(0, len(data), 2):
        r = cursor.execute("SELECT diff FROM " + database + " where type_name='" + data[i][0] + "' or type_name='" + \
                           data[i + 1][0] + "';")
        # 获取查询结果
        r = r.fetchall()
        if r:
            cursor.execute("delete FROM " + database + " where type_name='" + data[i][0] + "' or type_name='" + \
                           data[i + 1][0] + "';")
        cursor.executemany("INSERT INTO " + database + " VALUES(?,?);", [data[i], data[i + 1]])
    if close_cursor:
        cursor.close()


def db_insert_diff_single(data, cursor, close_cursor=False, database="sec_diff"):
    r = cursor.execute("SELECT diff FROM " + database + " where type_name='" + data[0][0] + "';")
    # 获取查询结果
    r = r.fetchall()
    if r:
        sql_delete = "delete FROM " + database + " where type_name='" + data[0][0] + "';"
        cursor.execute(sql_delete)
    cursor.executemany("INSERT INTO " + database + " VALUES(?,?);", data)
    if close_cursor:
        cursor.close()


def db_delete_diff(type_name_origin, cursor, close_cursor=False, database="sec_diff"):
    cursor.execute(
        "delete FROM " + database + " where type_name='" + type_name_origin + "Min' or type_name='" + type_name_origin + "Max';")
    if close_cursor:
        cursor.close()


def db_delete_diff_single(type_name, cursor, close_cursor=False, database="sec_diff"):
    cursor.execute("delete FROM " + database + " where type_name='" + type_name + "';")
    if close_cursor:
        cursor.close()


def db_select_diff_origin(type_name_origin, cursor, close_cursor=False, database="sec_diff"):
    r = cursor.execute(
        "SELECT type_name,diff FROM " + database + " where type_name='" + type_name_origin + "Min' or type_name='" + type_name_origin + "Max';")
    # 获取查询结果
    r = r.fetchall()
    if close_cursor:
        cursor.close()
    if not r:
        return None
    else:
        return [[item[0], item[1]] for item in r]


def db_select_diff_single(type_name, cursor, close_cursor=False, database="sec_diff"):
    r = cursor.execute("SELECT type_name,diff FROM " + database + " where type_name='" + type_name + "';")
    # 获取查询结果
    r = r.fetchall()
    if close_cursor:
        cursor.close()
    if not r:
        return None
    else:
        return [[item[0], item[1]] for item in r][-1]


def db_select_diff_all(cursor, close_cursor=False, database="sec_diff"):
    r = cursor.execute("SELECT * FROM " + database + ";")
    # 获取查询结果
    r = r.fetchall()
    if close_cursor:
        cursor.close()
    if not r:
        return None
    else:
        return [[item[0], item[1]] for item in r]


def getResultDiff(cursor, sensor_type, diff, close_cursor=False):
    if diff < 0:
        number = db_select_diff_single(sensor_type + "Min", cursor, close_cursor)
        if number is not None:
            if diff <= float(number[1]):
                return -1
        else:
            return sensor_type + "Min"
    else:
        number = db_select_diff_single(sensor_type + "Max", cursor, close_cursor)
        if number is not None:
            if diff >= float(number[1]):
                return 1
        else:
            return sensor_type + "Max"
