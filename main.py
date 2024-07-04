# -*- coding = utf-8 -*-
# @time: 2024/6/27 下午10:48
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: main.py
# app_main.py
import uvicorn
from fastapi import FastAPI
from controller.chat_controller import query_chat_router
from controller.sysconfig_controller import sysconfig_router
from controller.knowledge_controller import knowledge_router
from init_database import sql_run

sql_run()

app = FastAPI()
# 导入其他模块
app.include_router(query_chat_router)
app.include_router(sysconfig_router)
app.include_router(knowledge_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
