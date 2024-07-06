# -*- coding = utf-8 -*-
# @time: 2024/7/5 下午8:28
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: sqlite_memory.py
from typing import List, Dict, Any, Sequence

from cacheout import Cache
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from dao.chat_dao import query_chat_record, add_chat_record

cache = Cache(ttl=10 * 60)

column_mapping: Dict[str, str] = {
    'ai': 'assistant',
    'human': 'user'
}

message_type_mapping = {
    'assistant': lambda content: AIMessage(content=content),
    'user': lambda content: HumanMessage(content=content),
    'system': lambda content: SystemMessage(content=content),
}


class SqlLiteMemory(BaseChatMessageHistory):
    """存储关于实体信息的内存类。"""

    chat_type: str = "text"
    session_id: str
    max_history: int = 6

    messages = []

    # 定义将实体信息传递到提示中的键。
    memory_key: str = "chat_history"

    def __call__(self, session_id: str, chat_type: str):
        self.session_id = session_id
        self.chat_type = chat_type
        return self

    @property
    def messages(self):
        message_list = cache.get(self.session_id) or []
        if len(message_list) == 0:
            record_list = query_chat_record(self.session_id, limit=self.max_history, order='desc')
            record_list.reverse()
            for record in record_list:
                message = message_type_mapping[record['chat_role']](record['chat_content'])
                message_list.append(message)
            cache.set(self.session_id, message_list)

        if len(message_list) > self.max_history:
            message_list = message_list[-self.max_history:]
            cache.set(self.session_id, message_list)

        return message_list

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        for message in messages:
            role = column_mapping[message.type]
            self.messages.append(message)
            add_chat_record(self.session_id, self.chat_type, role, message.content)

    def clear(self):
        cache.set(self.session_id, [])
