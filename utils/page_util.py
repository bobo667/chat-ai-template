# -*- coding = utf-8 -*-
# @time: 2024/7/2 下午4:05
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: page_util.py

def get_page_index(page: int, size: int):
    """
    获取分页信息
    :param page: 页码
    :param size: 每页条数
    :return: 分页信息
    """
    return (page - 1) * size, size


def get_page(rows, total, page, size):
    """
    获取分页信息
    :param rows: 数据
    :param total: 总数
    :param page: 页码
    :param size: 每页条数
    :return: 分页信息
    """
    return {
        "rows": rows,
        "total": total,
        "page": page,
        "size": size
    }
