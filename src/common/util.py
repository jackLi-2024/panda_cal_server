#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import hashlib
import importlib
import traceback
import json
import time as _time
from datetime import datetime
import logging
import urllib
import sys
import requests

reload(sys)
sys.setdefaultencoding('utf8')

logger = logging.getLogger("upload")


def load_cls(controller_package, controller_name):
    """load_cls"""
    controller_package = controller_package
    controller_file = controller_name
    controller_cls_name = controller_name.capitalize()
    try:
        module = importlib.import_module(controller_package + "." + controller_file)
        controller_cls = getattr(module, controller_cls_name)
    except:
        logger.exception("failed to load package[%s], controller[%s]" %
                         (controller_package, controller_name))
        controller_cls = None

    # try:
    #     module = importlib.import_module(controller_package + "." + controller_file)
    #     controller_cls = getattr(module, controller_cls_name)
    # except ImportError:
    #     controller_cls = None
    # except AttributeError:
    #     controller_cls = None
    return controller_cls


def home_dir():
    """Get this project home directory"""
    p = os.path.split(os.path.realpath(__file__))[0]
    return os.path.abspath(p + "/../..") + "/"


def user_id_dir(user_name, create=True):
    """Get user_id dir"""
    full_path = os.path.join(home_dir(), "data", "user_data", user_name)
    if create and not os.path.exists(full_path):
        os.makedirs(full_path)
    return os.path.abspath(full_path) + "/"
