# encoding: utf-8
"""
@author: fonttian
@contact: fonttian@gmail.com
@license: by-nc-sa
@file: ExceptionHandler.py
@time: 2020/12/1 下午1:41
"""
dict_exception = {"OperationalError": "601"}


def exceptionHandler(classException):
    exceptionName = classException.__class__.__name__
    int_status_code = 500
    if exceptionName in dict_exception.keys():
        int_status_code = int(dict_exception[exceptionName])

    str_exceptionModule = "The object has no attribute '__module__'"
    try:
        str_exceptionModule = classException.__module__
    except Exception as err:
        pass
    finally:
        str_classException = str(classException)
        if str_classException == "unable to open database file":
            int_status_code = "602"
        return {"status": "exception", "exceptionModule": str_exceptionModule, "exceptionName": exceptionName,
                "exceptionContent": str_classException, "function": "exceptionHandler"}, int_status_code


def exceptionSpecified(content, function, status_code):
    return {"status": "failed",
            "content": content,
            "function": function}, status_code
