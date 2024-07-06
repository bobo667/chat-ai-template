# -*- coding = utf-8 -*-
# @time: 2024/6/30 下午10:52
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: knowledge_service.py
import json
import os

import chromadb
from dotenv import load_dotenv, find_dotenv
from langfuse.decorators import observe
from llama_index.core import Settings
from llama_index.core import SimpleDirectoryReader, StorageContext, GPTVectorStoreIndex
from llama_index.core import VectorStoreIndex
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.vector_stores.chroma import ChromaVectorStore

from dao.file_dao import query_file, query_knowledge_page, save_file_to_db, del_file
from utils.embedding_model import CustomEmbedding
from utils.llm_util import get_lcel

# 加载.env文件中的环境变量
_ = load_dotenv(find_dotenv())
# 加载.env文件中的环境变量
load_dotenv()
# 创建 ChromaDB 向量数据库，并持久化到本地
chroma_client = chromadb.PersistentClient(path=os.getenv("VECTOR_DATABASE_URL"))
Settings.embed_model = CustomEmbedding()

QUERY_GEN_PROMPT_DEFAULT_TEMPLATE = (
    "注意：需要用中文回答问题"
    "您是一个有用的助手，可以根据 "
    "单个输入查询。生成 {num_queries} 个搜索查询，每行一个, "
    "与以下输入查询相关:\n"
    "Query: {query}\n"
    "Queries:\n"
)

# 定义检索后排序模型
reranker = SentenceTransformerRerank(
    model=r"C:\Users\huibo.ma\.cache\modelscope\hub\maidalun\bce-reranker-base_v1", top_n=3
)


# 查詢文件分页
def query_knowledge_page_(page, size):
    return query_knowledge_page(page, size)


def save_file_to_db_(file_path):
    vector_ids = save_file_to_vectordb(file_path)
    file_id = save_file_to_db(file_path, vector_ids)
    return file_id


def del_file_(file_id):
    file_info = query_file(file_id)
    remove_knowledge(json.loads(file_info['vector_ids']))
    return del_file(file_id)


@observe()
def query_knowledge(chat_content, chat_type, chat_id):
    collection = get_collection()
    vector_store = ChromaVectorStore(chroma_collection=collection)
    # 初始化 VectorStoreIndex
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    fusion_retriever = QueryFusionRetriever(
        [index.as_retriever()],
        similarity_top_k=5,  # 检索召回 top k 结果
        # num_queries=1,  # 生成 query 数
        query_gen_prompt=QUERY_GEN_PROMPT_DEFAULT_TEMPLATE,  # 可以自定义 query 生成的 prompt 模板
    )

    query_engine = fusion_retriever.retrieve(chat_content)
    query_engine = reranker.postprocess_nodes(nodes=query_engine, query_str=chat_content)

    context = ''
    for node in query_engine:
        context += node.get_content()
        context += '\n'

    return get_lcel({'query': chat_content, 'context': context}, 'rag', chat_type,
                    chat_id)


# 文件处理函数
def process_file(file_path):
    file_extension = file_path.split('.')[-1].lower()
    reader = SimpleDirectoryReader(input_files=[file_path]).load_data()
    return reader


def save_file_to_vectordb(file_path):
    chroma_collection = get_collection()
    # 创建 Chroma 向量存储
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    # 创建存储上下文
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # 加载文档
    documents = process_file(file_path)
    # 创建索引
    index = GPTVectorStoreIndex.from_documents(documents, storage_context=storage_context)
    # 返回文档id
    return [doc.doc_id for doc in documents]


def remove_knowledge(ids):
    chroma_collection = get_collection()
    # 创建 Chroma 向量存储
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    # 删除向量
    for _id in ids:
        vector_store.delete(ref_doc_id=_id)


def get_collection():
    collection_name = "chat-ai-qa"
    return chroma_client.get_or_create_collection(name=collection_name)
