#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import logging
import signal
import ConfigParser
import time
from src.common import output
from src.common import util
from src import task
from src.cal import cal

logger = logging.getLogger("panda")

try:
    reload(sys)
    sys.setdefaultencoding("utf8")
except:
    pass


class Panda(object):
    """"""

    def __init__(self):
        pass

    def panda_test(self, request):
        return output.normal_result("Welcome to use panda data")

    def order(self, request):
        """"""
        start_time = request.args.get("start_time", None)
        end_time = request.args.get("end_time", None)
        collection = "carno"
        app_id = request.args.get("app_id", None)
        station_id = request.args.get("station_id", None)
        m = cal.MongoQuery(start_time=start_time, end_time=end_time,collection=collection)
        result = m.get_order(app_id, station_id=station_id)
        result = {"order_Number":result}
        return output.normal_result(result)

    def flow(self, request):
        start_time = request.args.get("start_time", None)
        end_time = request.args.get("end_time", None)
        collection = "carno"
        app_id = request.args.get("app_id", None)
        station_id = request.args.get("station_id", None)
        freq = request.args.get("freq", None)
        if not freq:
            freq = False
        else:
            freq = True
        m = cal.MongoQuery(start_time=start_time, end_time=end_time,collection=collection)
        result = m.Flow(app_id, station_id=station_id, freq=freq)
        result = {"flowTo":list(result)}
        return output.normal_result(result)

    def trend(self, request):
        start_time = request.args.get("start_time", None)
        end_time = request.args.get("end_time", None)
        collection = "carno"
        app_id = request.args.get("app_id", None)
        station_id = request.args.get("station_id", None)
        plot = request.args.get("plot", None)
        interval = request.args.get("interval", None)
        filename = "start_time=%s|end_time=%s|app_id=%s|interval=%s"% (str(start_time),str(end_time),str(app_id),str(interval))
        path = "./data/%s.png" % filename
        if not plot:
            plot = False
        else:
            plot = True
        m = cal.MongoQuery(start_time=start_time, end_time=end_time,collection=collection)
        result = m.get_trend(app_id, station_id=station_id, interval=interval, plot=plot, path=path)
        if plot:
            result = {"trend":list(result), "down_picture": "/data/%s.png" % filename}
        else:
            result = {"trend":list(result)}
        return output.normal_result(result)



