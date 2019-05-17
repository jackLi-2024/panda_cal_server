#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def normal_result(data=None, log_data=None):
    """normal result"""
    response = {
        'status': 0,
        'msg': "success",
        'data': data
    }
    result = {
        'status': 0,
        'response': json.dumps(response),
        'log_data': log_data
    }
    return result


def error_result(error_code, error_msg):
    """error result"""
    response = {
        'status': error_code,
        'msg': error_msg,
    }
    result = {
        'status': error_code,
        'response': json.dumps(response),
        'log_data': response
    }
    return result
