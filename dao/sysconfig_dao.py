# -*- coding = utf-8 -*-
# @time: 2024/7/3 下午9:52
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: sysconfig_dao.py
import uuid

from utils.db import query, execute


def query_config(config_code, def_val=""):
    sql = "select * from sys_config where config_code = ?"
    config_list = query(sql, (config_code,))
    if config_list:
        return config_list[0]['config_value']
    return def_val


def update_or_add_config(config_code, config_value):
    info = query_config(config_code, "")
    if info == '':
        sql = "insert into sys_config(id,config_code,config_name,config_value) values(?,?,?,?)"
        params = (str(uuid.uuid4()), config_code, config_code, config_value)
    else:
        sql = "update sys_config set config_value = ? where config_code = ?"
        params = (config_value, config_code)

    return execute(sql, params)
