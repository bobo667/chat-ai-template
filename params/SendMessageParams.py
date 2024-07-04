# -*- coding = utf-8 -*-
# @time: 2024/6/29 上午12:30
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: SendMessageParams.py
from typing import Optional

from pydantic import BaseModel


class SendMessageParams(BaseModel):
    chat_id: str = None
    chat_content: str
    chat_type: str
    chat_record_type: str = 'text'
    chat_role: str = 'user'
