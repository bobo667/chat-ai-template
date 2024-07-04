# -*- coding = utf-8 -*-
# @time: 2024/7/1 下午5:36
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: knowledge_controller.py
import os

from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File

from service.knowledge_service import query_knowledge_page_, del_file_, save_file_to_db_
from utils.Rs import Rs

# 加载.env文件中的环境变量
load_dotenv()
knowledge_router = APIRouter(prefix='/knowledge')


@knowledge_router.get("/query-knowledge-page")
async def query_knowledge_page_web(page: int, size: int):
    return Rs().ok(data=query_knowledge_page_(page, size))


@knowledge_router.delete("/del-file/{file_id}")
async def del_file_web(file_id: str):
    return Rs().ok(data=del_file_(file_id))


# 新增文件
@knowledge_router.post("/save-file")
async def save_file_web(file: UploadFile = File(...)):
    # 获取文件内容
    file_content = await file.read()
    # 保存文件到本地
    file_path = f"{os.getenv("FILE_LOCAL_PATH")}/{file.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(file_content)
    return Rs().ok(data=save_file_to_db_(file_path))
