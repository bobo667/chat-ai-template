# -*- coding = utf-8 -*-
# @time: 2024/7/3 下午9:58
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: file_dao.py
import json
import uuid

from utils.db import query, execute
from utils.page_util import get_page, get_page_index


# 查詢文件分页
def query_knowledge_page(page, size):
    sql = "select * from file_info order by create_time desc limit ?,?"
    count_sql = "select count(1) as count from file_info"
    count = query(count_sql, ())[0]['count']
    rows = query(sql, get_page_index(page, size))
    return get_page(rows, count, page, size)


def save_file_to_db(file_path, vector_ids):
    file_name = file_path.split('/')[-1]
    file_id = str(uuid.uuid4())
    sql = "insert into file_info(id,file_name,file_path,vector_ids) values(?,?,?,?)"

    execute(sql, (file_id, file_name, file_path, json.dumps(vector_ids)))
    return file_id


def query_file(file_id):
    sql = "select * from file_info where id = ?"
    return query(sql, (file_id,))[0]


def del_file(file_id):
    sql = f"delete from file_info where id = ?"
    execute(sql, (file_id,))
    return True
