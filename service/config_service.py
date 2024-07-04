# -*- coding = utf-8 -*-
# @time: 2024/7/1 下午4:29
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: config_service.py
from utils.db import query, execute
from dao.sysconfig_dao import query_config, update_or_add_config


def query_config_(config_code, def_val=""):
    return query_config(config_code, def_val)


def update_or_add_config_(config_code, config_value):
    return update_or_add_config(config_code, config_value)
