# -*- coding = utf-8 -*-
# @time: 2024/7/3 上午11:24
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: chat_dao.py
import uuid

from utils.db import query, execute


def query_chat_list():
    sql = "select * from chat_info order by create_time desc"
    return query(sql)


# 删除聊天室
def delete_chat(chat_id):
    sql = f"delete from chat_info where id = ?"
    execute(sql, (chat_id,))
    return True


# 新增聊天室并返回自增id主键
def add_chat(chat_name, chart_type):
    id_ = str(uuid.uuid4())
    sql = f"insert into chat_info(id,chat_name,chart_type) values(?,?,?)"
    execute(sql, (id_, chat_name, chart_type))
    return id_


# 查询聊天记录
def query_chat_record(chat_id, limit=0, order='asc'):
    sql = F"select * from chat_record where chat_info_id = ? order by chat_time {order}"
    if limit > 0:
        sql += F' limit {limit}'
    return query(sql, (chat_id,))


def query_chat_last_ai_record(chat_id):
    sql = F"select * from chat_record where chat_info_id = ? and chat_role = 'assistant' order by chat_time desc limit 1"
    return query(sql, (chat_id,))[0]


# 新增聊天记录
def add_chat_record(chat_id, chat_type, chat_role, chat_content):
    id_ = str(uuid.uuid4())
    sql = f"insert into chat_record(id,chat_info_id, chat_record_type, chat_role, chat_content) values(?,?,?,?,?)"
    execute(sql, (id_, chat_id, chat_type, chat_role, chat_content))
    return id_
