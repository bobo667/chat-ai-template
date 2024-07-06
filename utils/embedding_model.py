# -*- coding = utf-8 -*-
# @time: 2024/7/6 下午3:01
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: embedding_model.py
from typing import List

from llama_index.core.base.embeddings.base import BaseEmbedding, Embedding
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType

embedding = OpenAIEmbedding(model=OpenAIEmbeddingModelType.TEXT_EMBED_3_SMALL, dimensions=512)


class CustomEmbedding(BaseEmbedding):

    def _get_query_embedding(self, query: str) -> List[float]:
        """Get query embedding."""
        return embedding.get_query_embedding(query)

    async def _aget_query_embedding(self, query: str) -> List[float]:
        """The asynchronous version of _get_query_embedding."""
        return await embedding.aget_query_embedding(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        """Get text embedding."""
        client = self._get_client()
        return embedding.get_text_embedding(text)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        """Asynchronously get text embedding."""
        aclient = self._get_aclient()
        return await embedding.aget_text_embedding(text)

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get text embeddings.

        By default, this is a wrapper around _get_text_embedding.
        Can be overridden for batch queries.

        """
        return embedding.get_text_embedding_batch(texts)

    async def _aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Asynchronously get text embeddings."""
        return await embedding.aget_text_embedding_batch(texts)
