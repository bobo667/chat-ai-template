# -*- coding = utf-8 -*-
# @time: 2024/7/1 下午4:25
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: llm_util.py
import os

from dotenv import load_dotenv, find_dotenv
from langchain.schema import (
    AIMessage,  # 等价于OpenAI接口中的assistant role
    HumanMessage,  # 等价于OpenAI接口中的user role
    SystemMessage  # 等价于OpenAI接口中的system role
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate, SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langfuse.decorators import observe, langfuse_context

from dao.chat_dao import query_chat_record
from dao.sysconfig_dao import query_config
from utils.sqlite_memory import SqlLiteMemory

_ = load_dotenv(find_dotenv())


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


@observe()
def get_lcel(query_dict: dict, prompt_type, chat_type, chat_id):
    langfuse_context.update_current_trace(
        session_id=chat_id,
    )
    # 获取当前 LangChain 回调处理器
    langfuse_handler = langfuse_context.get_current_langchain_handler()
    model = get_llm()
    memory = SqlLiteMemory()
    # 创建聊天提示模板，包含一个系统消息、一个聊天历史占位符和一个人类消息模板。
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                "You are a nice chatbot having a conversation with a human."
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            get_local_prompts(prompt_type)
        ]
    )

    chain = (
            prompt | model | StrOutputParser()
    )
    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: memory(session_id, chat_type),
        input_messages_key="query",
        history_messages_key="chat_history",

    )

    return chain_with_history.stream(input=query_dict, config={
        "configurable": {"session_id": chat_id}, 'callbacks': [langfuse_handler]})


def get_local_prompts(prompt_type):
    # 获取当前脚本的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if prompt_type == 'rag':
        file_path = os.path.join(script_dir, 'template', 'rag_template.txt')
    else:
        file_path = os.path.join(script_dir, 'template', 'normal_template.txt')

    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    return HumanMessagePromptTemplate.from_template(file_content)
