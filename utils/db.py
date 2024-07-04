# -*- coding = utf-8 -*-
# @time: 2024/6/27 下午9:25
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: dao.py
import sqlite3
from contextlib import closing

from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量
load_dotenv()

# 数据库文件路径
db_file_path = os.getenv('DATABASE_URL')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db_connection():
    conn = sqlite3.connect(db_file_path)
    conn.row_factory = dict_factory  # 设置 row_factory
    return conn


def _db_execute(sql, params=None, commit=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)
    if commit:
        conn.commit()
    return cursor, conn


def query(sql, params=None):
    cursor, conn = _db_execute(sql, params)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records


def execute(sql, params=None):
    cursor, conn = _db_execute(sql, params, commit=True)
    cursor.close()
    conn.close()


def get_conn():
    # 连接到SQLite数据库
    return sqlite3.connect(db_file_path)
