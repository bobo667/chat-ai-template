# -*- coding = utf-8 -*-
# @time: 2024/7/1 下午4:25
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: llm_util.py
from dotenv import load_dotenv, find_dotenv
from langchain.prompts import PromptTemplate
from langchain.schema import (
    AIMessage,  # 等价于OpenAI接口中的assistant role
    HumanMessage,  # 等价于OpenAI接口中的user role
    SystemMessage  # 等价于OpenAI接口中的system role
)
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from dao.chat_dao import query_chat_record
from dao.sysconfig_dao import query_config

_ = load_dotenv(find_dotenv())

# 加载.env文件中的环境变量
load_dotenv()


def get_llm():
    config = query_config("llm_model", 'gpt-3.5-turbo')
    temperature_config = query_config("llm_temperature", 0.2)
    llm = ChatOpenAI(model=config, temperature=temperature_config)
    return llm


# 获取历史聊天记录
def get_historical_chat(chat_id):
    record_list = query_chat_record(chat_id)
    historical_list = []
    for record in record_list:
        if record['chat_role'] == 'assistant':
            historical_list.append(AIMessage(content=record['chat_content']))
        elif record['chat_role'] == 'user':
            historical_list.append(HumanMessage(content=record['chat_content']))
        else:
            historical_list.append(SystemMessage(content=record['chat_content']))
    return historical_list


def get_lcel(chat_id):
    model = get_llm()
    message_list = get_historical_chat(chat_id)
    chain = (
            model | StrOutputParser()
    )
    return chain.stream(message_list)


def get_local_prompts():
    template = PromptTemplate.from_file("./template/normal_template.txt")
    return template
