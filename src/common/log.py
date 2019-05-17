#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import logging
import logging.handlers
import logging.config


def init_log(log_conf_path="./conf/logging.conf"):
    """init log"""
    logging.config.fileConfig(log_conf_path)
