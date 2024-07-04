# -*- coding = utf-8 -*-
# @time: 2024/7/1 下午5:36
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: knowledge_controller.py

from dotenv import load_dotenv
from fastapi import APIRouter, Body

from service.config_service import query_config_, update_or_add_config_
from utils.Rs import Rs

# 加载.env文件中的环境变量
load_dotenv()
sysconfig_router = APIRouter(prefix='/sys-config')


@sysconfig_router.get("/query-sys-config/{code}")
async def query_sys_config(code):
    return Rs().ok(data=query_config_(code))


@sysconfig_router.post("/save-config")
async def save_config(config_code: str = Body(), config_value=Body()):
    return Rs().ok(data=update_or_add_config_(config_code, config_value))
