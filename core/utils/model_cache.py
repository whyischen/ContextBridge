"""
嵌入模型缓存管理器
实现 10 分钟空闲自动卸载机制
"""
import time
import threading
import gc
import weakref
from typing import Optional, Callable
from core.interfaces.embedding_model import IEmbeddingModel
from core.utils.logger import get_logger

logger = get_logger("model_cache")


class ModelCache:
    """
    嵌入模型缓存管理器
    
    特性：
    - 延迟加载：首次使用时才加载模型
    - 活动追踪：每次使用时更新最后活动时间
    - 自动卸载：10 分钟无活动后自动卸载模型释放内存
    - 线程安全：使用 RLock 支持递归锁定
    - 智能清理：使用 Timer 而非轮询，减少 CPU 占用
    """
    
    IDLE_TIMEOUT = 10 * 60  # 10 分钟
    CHECK_INTERVAL = 60  # 检查间隔（秒）
    
    def __init__(self):
        self._model: Optional[IEmbeddingModel] = None
        self._model_loader: Optional[Callable] = None
        self._last_activity_time = time.time()
        self._lock = threading.RLock()  # 使用递归锁，支持嵌套调用
        self._cleanup_timer: Optional[threading.Timer] = None
        self._is_shutting_down = False
    
    def get_model(self, model_loader_func: Callable[[], IEmbeddingModel]) -> IEmbeddingModel:
        """
        获取模型实例（延迟加载 + 活动追踪）
        
        Args:
            model_loader_func: 模型加载函数，返回 IEmbeddingModel 实例
            
        Returns:
            IEmbeddingModel 实例
        """
        with self._lock:
            # 卫语句：如果正在关闭，拒绝加载
            if self._is_shutting_down:
                raise RuntimeError("ModelCache is shutting down, cannot load model")
            
            # 更新最后活动时间
            self._last_activity_time = time.time()
            
            # 如果模型未加载，加载它
            if self._model is None:
                logger.info("Loading embedding model (first use or after idle timeout)...")
                self._model = model_loader_func()
                self._model_loader = model_loader_func  # 保存加载器以便重新加载
                logger.info(f"✅ Embedding model loaded: {self._model.__class__.__name__}")
            
            # 重置清理定时器
            self._reset_cleanup_timer()
            
            return self._model
    
    def touch(self):
        """
        更新活动时间（不获取模型）
        用于标记活动但不需要立即使用模型的场景
        """
        with self._lock:
            self._last_activity_time = time.time()
            if self._model is not None:
                self._reset_cleanup_timer()
    
    def _reset_cleanup_timer(self):
        """重置清理定时器（智能调度）"""
        # 取消现有定时器
        if self._cleanup_timer is not None:
            self._cleanup_timer.cancel()
        
        # 卫语句：如果正在关闭，不创建新定时器
        if self._is_shutting_down:
            return
        
        # 计算下次检查时间
        # 使用 CHECK_INTERVAL 而非 IDLE_TIMEOUT，避免过长等待
        next_check = min(self.CHECK_INTERVAL, self.IDLE_TIMEOUT)
        
        # 创建新定时器
        self._cleanup_timer = threading.Timer(
            next_check,
            self._check_and_cleanup
        )
        self._cleanup_timer.daemon = True
        self._cleanup_timer.start()
    
    def _check_and_cleanup(self):
        """检查空闲时间并决定是否卸载模型"""
        with self._lock:
            # 卫语句：如果正在关闭或模型已卸载，直接返回
            if self._is_shutting_down or self._model is None:
                return
            
            idle_time = time.time() - self._last_activity_time
            
            # 如果超过空闲时间，卸载模型
            if idle_time >= self.IDLE_TIMEOUT:
                logger.info(
                    f"Model cache idle for {idle_time/60:.1f} minutes, "
                    "unloading to save memory."
                )
                self._unload_model()
            else:
                # 还未到卸载时间，继续等待
                remaining_time = self.IDLE_TIMEOUT - idle_time
                next_check = min(self.CHECK_INTERVAL, remaining_time + 1)
                
                # 重新调度检查
                self._cleanup_timer = threading.Timer(
                    next_check,
                    self._check_and_cleanup
                )
                self._cleanup_timer.daemon = True
                self._cleanup_timer.start()
    
    def _unload_model(self):
        """内部方法：卸载模型并释放内存"""
        if self._model is not None:
            model_name = self._model.__class__.__name__
            self._model = None
            
            # 强制垃圾回收
            collected = gc.collect()
            logger.debug(f"Model '{model_name}' unloaded, collected {collected} objects")
    
    def force_unload(self):
        """强制卸载模型（用于测试或手动清理）"""
        with self._lock:
            if self._cleanup_timer is not None:
                self._cleanup_timer.cancel()
                self._cleanup_timer = None
            
            if self._model is not None:
                logger.info("Force unloading embedding model...")
                self._unload_model()
    
    def shutdown(self):
        """
        优雅关闭缓存管理器
        停止所有定时器并卸载模型
        """
        with self._lock:
            self._is_shutting_down = True
            
            # 取消定时器
            if self._cleanup_timer is not None:
                self._cleanup_timer.cancel()
                self._cleanup_timer = None
            
            # 卸载模型
            if self._model is not None:
                logger.info("Shutting down model cache...")
                self._unload_model()
            
            logger.debug("Model cache shutdown complete")
    
    def get_stats(self) -> dict:
        """
        获取缓存统计信息（用于监控和调试）
        
        Returns:
            包含缓存状态的字典
        """
        with self._lock:
            idle_time = time.time() - self._last_activity_time
            return {
                "model_loaded": self._model is not None,
                "model_class": self._model.__class__.__name__ if self._model else None,
                "idle_seconds": idle_time,
                "idle_minutes": idle_time / 60,
                "time_until_unload": max(0, self.IDLE_TIMEOUT - idle_time),
                "is_shutting_down": self._is_shutting_down,
            }


# 全局模型缓存实例
_global_model_cache: Optional[ModelCache] = None
_cache_lock = threading.Lock()


def get_global_model_cache() -> ModelCache:
    """获取全局模型缓存实例（线程安全，双重检查锁定）"""
    global _global_model_cache
    
    # 第一次检查（无锁，快速路径）
    if _global_model_cache is not None:
        return _global_model_cache
    
    # 第二次检查（有锁，慢速路径）
    with _cache_lock:
        if _global_model_cache is None:
            _global_model_cache = ModelCache()
            logger.debug("Global model cache initialized")
        return _global_model_cache


def set_global_model_cache(cache: ModelCache):
    """设置全局模型缓存实例（用于测试）"""
    global _global_model_cache
    with _cache_lock:
        _global_model_cache = cache


def shutdown_global_cache():
    """关闭全局模型缓存（用于优雅退出）"""
    global _global_model_cache
    with _cache_lock:
        if _global_model_cache is not None:
            _global_model_cache.shutdown()
            _global_model_cache = None
            logger.debug("Global model cache shut down")
