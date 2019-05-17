#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import logging
import signal
import multiprocessing

from flask import request
from flask import Flask

from src.common import output
from src.common import log
from src.common import util


sys.path.append("%s/.." % util.home_dir())

log.init_log()
logger = logging.getLogger("panda")


class Handler(object):
    """main handler"""

    def __init__(self):
        self.load_controller_map()

    def load_controller_map(self):
        """load controller obj"""
        self._controller_map = {}
        for root, dirs, files in os.walk("./src/controllers"):
            for name in files:
                if "__init" not in name:
                    controller = None
                    if name[-3:] == ".py":
                        controller = name[:-3]
                    elif name[-4:] == ".pyc":
                        controller = name[:-4]
                    if controller:
                        controller_cls = util.load_cls("src.controllers", controller)
                        self._controller_map[controller] = controller_cls()

    def handle(self, controller_name, method_name):
        """handle"""
        if controller_name not in self._controller_map:
            return output.error_result(-1, u"逻辑模块 %s 不存在" % controller_name)
        controller_obj = self._controller_map[controller_name]

        try:
            method = getattr(controller_obj, method_name)
        except AttributeError:
            return output.error_result(-2, u"逻辑模块 %s 未找到对应方法 %s"
                                       % (controller_name, method_name))
        try:
            result = method(request)
            if not result or 'status' not in result:
                return output.error_result(-2, u"方法 %s.%s 返回错误"
                                           % (controller_name, method_name))
            return result

        except Exception as e:
            return output.error_result(-1, u"运行 %s.%s 失败, except: [%s]"
                                       % (controller_name, method_name, e))


handler = Handler()
app = Flask(__name__)

logger.info("test server is ready.")


@app.route('/panda/<controller_name>/<method_name>', methods=['GET', 'POST'])
def main_function(controller_name, method_name):
    """main entry"""
    # handle the request
    start_time = time.time()
    result = handler.handle(controller_name=controller_name, method_name=method_name)
    end_time = time.time()

    # log
    log_content = {
        "cost_time": end_time - start_time,
        "status": result['status'],
        "request": request.args,
        "rs": result.get('log_data', "")
    }
    logger.info(json.dumps(log_content))

    return result['response']


if __name__ == '__main__':
    # read_dict()
    app.run(host='0.0.0.0', port=8472)
