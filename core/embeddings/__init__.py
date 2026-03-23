"""
嵌入模型实现模块

提供各种嵌入模型的具体实现，包括：
- GTE-Small-Zh: 阿里达摩院的中文嵌入模型（ONNX INT8 量化版本）
- 未来可扩展: BGE, M3E, OpenAI Embeddings 等
"""

from core.embeddings.gte_small_zh import GTESmallZhONNX

__all__ = ['GTESmallZhONNX']
