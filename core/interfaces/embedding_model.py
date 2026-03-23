from abc import ABC, abstractmethod
from typing import List


class IEmbeddingModel(ABC):
    """
    嵌入模型抽象接口
    
    定义了文本向量化的标准接口，支持单文本和批量文本的向量化操作。
    实现此接口可以轻松切换不同的嵌入模型（如 GTE、BGE、M3E 等）。
    """
    
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """
        单文本向量化
        
        Args:
            text: 待向量化的文本
            
        Returns:
            文本的向量表示（浮点数列表）
        """
        pass
    
    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        批量文本向量化
        
        Args:
            texts: 待向量化的文本列表
            
        Returns:
            文本向量列表，每个文本对应一个向量
        """
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """
        获取向量维度
        
        Returns:
            向量的维度大小
        """
        pass
