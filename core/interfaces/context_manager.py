from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IContextManager(ABC):
    @abstractmethod
    def write_context(self, filename: str, content: str, level: str = "L2") -> bool:
        """
        写入上下文。
        例如：write_context("report.docx", "...", level="L2")
        """
        pass

    @abstractmethod
    def delete_context(self, filename: str) -> bool:
        """
        删除上下文。
        例如：delete_context("report.docx")
        """
        pass

    @abstractmethod
    def recursive_retrieve(
        self, 
        query: str, 
        top_k: int = None,
        min_similarity: float = None,
        enable_rerank: bool = True,
        explain: bool = False
    ) -> List[Dict[str, Any]]:
        """
        执行高级检索策略（如 OpenViking 的目录递归检索）
        
        Args:
            query: 搜索查询
            top_k: 返回结果数量（None 使用配置默认值）
            min_similarity: 最小相似度阈值（None 使用配置默认值）
            enable_rerank: 是否启用高级重排序（BM25 + 关键词 + 位置）
            explain: 是否返回详细的打分解释
        """
        pass

    @abstractmethod
    def get_all_filenames(self) -> List[str]:
        """
        获取所有已索引的文件名
        """
        pass
