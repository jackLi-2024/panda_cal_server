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

logger = logging.getLogger("panda")


class Panda(object):
    """"""

    def __init__(self):
        pass

    def panda_test(self, request):
        return output.normal_result("Welcome to use panda data")


    def get_task_id(self, request):
        """get task id"""
        user_id = request.form.get("user_id", None)
        task_log = request.form.get("task_log", None)
        os.system("mkdir -p ./data/%s/%s" % (user_id, task_log))
        task_id = str(time.time())
        os.system("mkdir -p ./temp/%s/%s" % (user_id, task_id))
        result = {"user_id": user_id, "task_id": task_id, "task_log": task_log}
        return output.normal_result(result)

    def delete_temp(self, request):
        """delete"""
        user_id = request.form.get("user_id", None)
        task_id = request.form.get("task_id", None)
        os.system("rm -rf ./temp/%s/%s" % (user_id, task_id))
        result = {"user_id": user_id, "task_id": task_id}
        return output.normal_result(result)


