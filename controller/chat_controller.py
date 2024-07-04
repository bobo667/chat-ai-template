# -*- coding = utf-8 -*-
# @time: 2024/6/27 下午10:39
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: chat_controller.py
from fastapi import APIRouter
import asyncio
from service.chart_service import query_chat_list, builder_message, delete_chat, send_message, add_chat_record, \
    get_last_ai_message
from utils.Rs import Rs
from fastapi.responses import StreamingResponse
import time
from params.SendMessageParams import SendMessageParams

query_chat_router = APIRouter()


@query_chat_router.get("/query-chat-list")
async def query_chat():
    return Rs().ok(data=query_chat_list())


# 查询聊天记录
@query_chat_router.get("/query-chat-record/{chat_id}")
async def query_chat_record_router(chat_id):
    return Rs().ok(data=builder_message(chat_id))


# 查询聊天记录
@query_chat_router.get("/query-chat-last-ai-record/{chat_id}")
async def query_chat_last_ai_record_router(chat_id):
    return Rs().ok(data=get_last_ai_message(chat_id))


# 删除聊天室
@query_chat_router.delete("/delete-chat{chat_id}")
async def delete_chat_router(chat_id):
    return Rs().ok(data=delete_chat(chat_id))


@query_chat_router.post("/chunked")
async def chunked_transfer():
    message = """
        以下是使用C语言实现的冒泡排序算法：\n\n```c\n#include <stdio.h>\n\nvoid bubbleSort(int arr[], int n) {\n    int i, j;\n    for (i = 0; i < n - 1; i++) {\n        for (j = 0; j < n - i - 1; j++) {\n            if (arr[j] > arr[j + 1]) {\n                // 交换 arr[j] 和 arr[j+1]\n                int temp = arr[j];\n                arr[j] = arr[j + 1];\n                arr[j + 1] = temp;\n            }\n        }\n    }\n}\n\nint main() {\n    int arr[] = {64, 34, 25, 12, 22, 11, 90};\n    int n = sizeof(arr) / sizeof(arr[0]);\n    \n    printf(\"排序前数组：\");\n    for (int i = 0; i < n; i++) {\n        printf(\"%d \", arr[i]);\n    }\n    printf(\"\\\n\");\n\n    bubbleSort(arr, n);\n\n    printf(\"排序后数组：\");\n    for (int i = 0; i < n; i++) {\n        printf(\"%d \", arr[i]);\n    }\n    printf(\"\\\n\");\n\n    return 0;\n}\n```\n\n这段C语言代码实现了冒泡排序算法。通过比较相邻的元素并进行交换，依次将较大的元素移动到数组的末尾，直到整个数组有序为止。C语言是一种经典的编程语言，冒泡排序算法的实现在这里也体现了其基本逻辑和操作。
    """

    async def generate_large_data():
        for i in message:
            data = f"data:{i}\n\n"
            yield data
            await asyncio.sleep(0.03)

    return StreamingResponse(generate_large_data(), media_type="text/event-stream")


# 发送消息 流式返回
@query_chat_router.post("/send-message")
async def send_message_router(param: SendMessageParams):
    start = time.time()
    res = send_message(param)
    chat_id, response = res
    end = time.time() - start
    print(f"耗时{end}秒")

    def generate():
        chat_content = ''
        data = f"data:#startId:{chat_id}\n\n"
        yield data
        for msg in response:
            chat_content += msg
            data = f"data:{msg}\n\n"
            yield data
        data = F"data:#end:\n\n"
        yield data
        add_chat_record(chat_id, 'text', 'assistant', chat_content)

    return StreamingResponse(generate(), media_type="text/event-stream")
