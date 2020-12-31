#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys, logging, traceback, json
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_formatter = logging.Formatter("[%(levelname)s:%(asctime)s %(process)s %(filename)s:%(lineno)d]: %(message)s", "%Y-%m-%d %H:%M:%S")

file_handler = RotatingFileHandler(os.path.dirname(os.path.abspath(__file__)) + "/execute.log", "a", 1024 * 1024 * 20, 5)
file_handler.setFormatter(log_formatter)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(log_formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def log_error(msg):
    logger.error(msg)
    logger.error("Failed!!!")
    sys.exit(1)

def log_warning(msg):
    logger.warning(msg)

def log_info(msg):
    logger.info(msg)
