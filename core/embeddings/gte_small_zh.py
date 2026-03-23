import os
import logging
from pathlib import Path
from typing import List
import numpy as np
from core.interfaces.embedding_model import IEmbeddingModel
from core.i18n import t
from rich.console import Console

# 设置 Hugging Face 镜像（国内访问加速）
# 如果用户已设置环境变量，则不覆盖
if "HF_ENDPOINT" not in os.environ:
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# Windows 特定：禁止 Hugging Face Hub 显示进度条弹窗
if "HF_HUB_DISABLE_PROGRESS_BARS" not in os.environ:
    os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

# Windows 特定：禁止 Transformers 显示进度条
if "TRANSFORMERS_NO_ADVISORY_WARNINGS" not in os.environ:
    os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

logger = logging.getLogger(__name__)
console = Console(stderr=True)


class GTESmallZhONNX(IEmbeddingModel):
    """
    GTE-Small-Zh ONNX INT8 量化模型
    
    使用阿里达摩院的 GTE-Small-Zh 模型的 ONNX INT8 量化版本。
    模型来源: towing/gte-small-zh (Hugging Face)
    模型大小: 30.5 MB
    向量维度: 384
    
    特点:
    - 专为中文优化
    - INT8 量化，推理速度快
    - 体积小，适合本地部署
    """
    
    MODEL_NAME = "towing/gte-small-zh"
    MODEL_FILE = "model_quantized.onnx"
    DIMENSION = 384
    
    def __init__(self, model_dir: Path = None):
        """
        初始化 GTE-Small-Zh 模型
        
        Args:
            model_dir: 模型存储目录，默认为 ~/.cbridge/models/gte-small-zh
        """
        if model_dir is None:
            model_dir = Path.home() / ".cbridge" / "models" / "gte-small-zh"
        
        self.model_dir = model_dir
        self.model_path = model_dir / "onnx" / self.MODEL_FILE
        self.session = None
        self.tokenizer = None
        
        self._ensure_model()
    
    def _ensure_model(self):
        """确保模型已下载并加载"""
        if not self.model_path.exists():
            self._download_model()
        self._load_model()
    
    def _download_model(self):
        """从 Hugging Face 下载模型"""
        try:
            from huggingface_hub import snapshot_download
            
            console.print(t("emb_gte_downloading"))
            
            # 显示镜像提示
            if os.environ.get("HF_ENDPOINT") == "https://hf-mirror.com":
                console.print(t("emb_gte_mirror_hint"))
            
            logger.info(f"Downloading GTE-Small-Zh model from {self.MODEL_NAME}")
            logger.info(f"Using HF_ENDPOINT: {os.environ.get('HF_ENDPOINT', 'default')}")
            
            self.model_dir.mkdir(parents=True, exist_ok=True)
            
            # 下载模型（新版 huggingface_hub 不再需要 local_dir_use_symlinks 参数）
            snapshot_download(
                repo_id=self.MODEL_NAME,
                local_dir=self.model_dir,
                allow_patterns=["onnx/model_quantized.onnx", "*.json", "*.txt"]
            )
            
            console.print(t("emb_gte_download_success"))
            logger.info(f"✅ GTE-Small-Zh model downloaded to {self.model_dir}")
            
        except Exception as e:
            console.print(t("emb_gte_download_failed", error=str(e)))
            logger.error(f"Failed to download GTE-Small-Zh model: {e}", exc_info=True)
            
            # 提供手动下载提示
            console.print("\n[yellow]💡 手动下载方法 / Manual Download:[/yellow]")
            console.print(f"[dim]1. 访问 / Visit: https://hf-mirror.com/towing/gte-small-zh[/dim]")
            console.print(f"[dim]2. 下载 / Download: onnx/model_quantized.onnx, *.json, *.txt[/dim]")
            console.print(f"[dim]3. 解压到 / Extract to: {self.model_dir}[/dim]")
            
            raise
    
    def _load_model(self):
        """加载 ONNX 模型和 tokenizer"""
        try:
            import onnxruntime as ort
            from transformers import AutoTokenizer
            
            logger.info(f"Loading GTE-Small-Zh ONNX model from {self.model_path}")
            
            # 配置 ONNX Runtime 会话选项
            sess_options = ort.SessionOptions()
            
            # Windows 特定：禁止弹出控制台窗口
            import sys
            if sys.platform == "win32":
                # 设置日志级别为错误，减少输出
                sess_options.log_severity_level = 3  # 3 = ERROR
                # 禁用遥测
                sess_options.enable_profiling = False
            
            # 加载 ONNX 模型
            self.session = ort.InferenceSession(
                str(self.model_path),
                sess_options=sess_options,
                providers=['CPUExecutionProvider']
            )
            
            # 加载 tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                str(self.model_dir),
                local_files_only=True
            )
            
            logger.info(f"✅ GTE-Small-Zh ONNX model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load GTE-Small-Zh model: {e}", exc_info=True)
            raise
    
    def embed_text(self, text: str) -> List[float]:
        """
        单文本向量化
        
        Args:
            text: 待向量化的文本
            
        Returns:
            文本的向量表示（384 维）
        """
        return self.embed_batch([text])[0]
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        批量文本向量化
        
        Args:
            texts: 待向量化的文本列表
            
        Returns:
            文本向量列表，每个文本对应一个 384 维向量
        """
        if not texts:
            return []
        
        try:
            # Tokenize
            inputs = self.tokenizer(
                texts,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="np"
            )
            
            # ONNX 推理
            onnx_inputs = {
                "input_ids": inputs["input_ids"].astype(np.int64),
                "attention_mask": inputs["attention_mask"].astype(np.int64),
            }
            
            # 如果模型需要 token_type_ids，添加它
            if "token_type_ids" in inputs:
                onnx_inputs["token_type_ids"] = inputs["token_type_ids"].astype(np.int64)
            
            outputs = self.session.run(None, onnx_inputs)
            embeddings = outputs[0]  # 取第一个输出（通常是 last_hidden_state）
            
            # Mean pooling
            attention_mask = inputs["attention_mask"]
            embeddings = self._mean_pooling(embeddings, attention_mask)
            
            # Normalize
            embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
            
            return embeddings.tolist()
            
        except Exception as e:
            logger.error(f"Error during embedding: {e}", exc_info=True)
            raise
    
    def _mean_pooling(self, token_embeddings: np.ndarray, attention_mask: np.ndarray) -> np.ndarray:
        """
        平均池化
        
        对 token embeddings 进行加权平均，权重由 attention_mask 决定
        
        Args:
            token_embeddings: Token 级别的嵌入向量 [batch_size, seq_len, hidden_size]
            attention_mask: 注意力掩码 [batch_size, seq_len]
            
        Returns:
            句子级别的嵌入向量 [batch_size, hidden_size]
        """
        input_mask_expanded = np.expand_dims(attention_mask, -1).astype(float)
        sum_embeddings = np.sum(token_embeddings * input_mask_expanded, axis=1)
        sum_mask = np.clip(input_mask_expanded.sum(axis=1), a_min=1e-9, a_max=None)
        return sum_embeddings / sum_mask
    
    def get_dimension(self) -> int:
        """
        获取向量维度
        
        Returns:
            384 (GTE-Small-Zh 的向量维度)
        """
        return self.DIMENSION
