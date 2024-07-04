# -*- coding = utf-8 -*-
# @time: 2024/6/30 下午10:52
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: knowledge_service.py
import json
import os

import chromadb
from dotenv import load_dotenv, find_dotenv
from llama_index.core import Settings, PromptTemplate
from llama_index.core import SimpleDirectoryReader, StorageContext, GPTVectorStoreIndex
from llama_index.core import VectorStoreIndex
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.service_context_elements.llm_predictor import LLMPredictor
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

from dao.chat_dao import query_chat_record
from dao.file_dao import query_file, query_knowledge_page, save_file_to_db, del_file
from utils.llm_util import get_llm

# 加载.env文件中的环境变量
_ = load_dotenv(find_dotenv())
# 加载.env文件中的环境变量
load_dotenv()
# 创建 ChromaDB 向量数据库，并持久化到本地
chroma_client = chromadb.PersistentClient(path=os.getenv("VECTOR_DATABASE_URL"))
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", dimensions=512)

DEFAULT_TEMPLATE = """\
给定一个对话（在 Human 和 Assistant 之间）和来自 Human 的后续消息，将消息重写为一个独立的问题，从对话中捕获所有相关上下文。
注意：用中文回答问题

<Chat History>
{chat_history}

<Follow Up Message>
{question}

<Standalone question>
"""

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


def query_knowledge(chat_id):
    collection = get_collection()
    vector_store = ChromaVectorStore(chroma_collection=collection)
    # 初始化 VectorStoreIndex
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    llm_predictor = LLMPredictor(llm=get_llm())
    fusion_retriever = QueryFusionRetriever(
        [index.as_retriever()],
        similarity_top_k=5,  # 检索召回 top k 结果
        # num_queries=1,  # 生成 query 数
        query_gen_prompt=QUERY_GEN_PROMPT_DEFAULT_TEMPLATE,  # 可以自定义 query 生成的 prompt 模板
    )

    query_engine = RetrieverQueryEngine.from_args(
        fusion_retriever,
        streaming=True,
        llm_predictor=llm_predictor,
        node_postprocessors=[reranker]
    )

    chat_engine = CondenseQuestionChatEngine.from_defaults(
        query_engine=query_engine,
        condense_question_prompt=PromptTemplate(DEFAULT_TEMPLATE)  # 可以自定义 chat message prompt 模板
    )

    record_list = query_chat_record(chat_id)
    chat_history_list = []
    for record in record_list:
        message = ChatMessage.from_str(record['chat_content'], role=record['chat_role'])
        chat_history_list.append(message)

    last_message = chat_history_list[-1]
    # 祛除掉最后一个自己提问的多余的信息
    chat_history_list = chat_history_list[:-1]
    response = chat_engine.stream_chat(last_message.content, chat_history_list)
    return response.response_gen


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
