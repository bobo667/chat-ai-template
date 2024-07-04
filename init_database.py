# -*- coding = utf-8 -*-
# @time: 2024/6/27 下午5:42
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: init_database.py
import utils.db as db

create_table_sql_list = [
    """
    create TABLE IF NOT EXISTS chat_info
    (
        id          STR not null ,
        chat_name   STR     not null,
        chart_type  STR     not null,
        create_time TIMESTAMP default CURRENT_TIMESTAMP
    );
    """,
    """
    create TABLE IF NOT EXISTS chat_record
    (
        id          STR not null , 
        chat_record_type   STR     not null, -- 聊天类型
        chat_role        STR     not null, -- 角色
        chat_info_id     STR  not null, -- 聊天室ID
        chat_time   TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 聊天时间
        chat_content TEXT     not null  -- 聊天内容
    );
    """,
    """
    create TABLE IF NOT EXISTS file_info
    (
        id          STR not null , -- 文件ID
        file_name   STR     not null, -- 文件名
        file_path   STR     not null, -- 文件路径
        vector_ids JSON   not null, -- 向量ID
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 创建时间
    );
    """,
    """
    create TABLE IF NOT EXISTS sys_config
    (
        id          STR not null , -- 文件ID
        config_code STR not null , -- 配置编码
        config_name   STR     not null, -- 配置名
        config_value   STR     not null, -- 配置值
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 创建时间
    );
    """
]


# 执行创建表的操作，由于使用了"IF NOT EXISTS"，所以如果表已存在则不会重复创建
def sql_run():
    print("初始化sql...")
    for create_table_sql in create_table_sql_list:
        db.execute(create_table_sql)
