# -*- coding = utf-8 -*-
# @time: 2024/6/28 下午7:31
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: chart_service.py
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

from dao.chat_dao import query_chat_record, add_chat_record, add_chat, query_chat_list, delete_chat, \
    query_chat_last_ai_record
from params.SendMessageParams import SendMessageParams
from service.knowledge_service import query_knowledge
from utils.llm_util import get_lcel

_ = load_dotenv(find_dotenv())

# 加载.env文件中的环境变量
load_dotenv()
client = OpenAI()


def query_chat_list_():
    return query_chat_list()


# 删除聊天室
def delete_chat_(chat_id):
    return delete_chat(chat_id)


# 新增聊天记录
def add_chat_record_(chat_id, chat_type, chat_role, chat_content):
    return add_chat_record(chat_id, chat_type, chat_role, chat_content)


def get_last_ai_message(chat_id):
    return query_chat_last_ai_record(chat_id)


# 发送消息
def send_message(param: SendMessageParams):
    chat_id = param.chat_id
    chat_content = param.chat_content
    chat_type = param.chat_type
    chat_record_type = param.chat_record_type
    chat_role = param.chat_role

    if chat_id is None or chat_id == "":
        chat_id = add_chat(chat_content if len(chat_content) <= 5 else chat_content[:5] + "...", chat_type)

    return chat_id, get_lcel({'query': chat_content}, 'text', chat_record_type,
                             chat_id) if chat_type == 'text' else query_knowledge(
        chat_content, chat_record_type, chat_id)  # 直接返回生成器


def builder_message(chat_id):
    chat_record_list = query_chat_record(chat_id)
    messages = []
    for chat_record in chat_record_list:
        messages.append({"role": chat_record['chat_role'], "content": chat_record['chat_content']})
    return messages
