from core.config import CONFIG
from core.runtimes.qmd_runtime import QMDRuntime
from core.managers.openviking_manager import OpenVikingManager
from core.utils.logger import get_logger
from core.utils.model_cache import get_global_model_cache

logger = get_logger("factories")

# Singleton instance cache
_context_manager_instance = None

def _load_embedding_model():
    """
    加载嵌入模型（由 ModelCache 调用）
    
    Returns:
        IEmbeddingModel 实例或 None（使用 ChromaDB 默认模型）
    """
    embedding_config = CONFIG.get("embedding", {})
    model_type = embedding_config.get("model", "gte-small-zh")
    
    if model_type == "gte-small-zh":
        from core.embeddings.gte_small_zh import GTESmallZhONNX
        logger.debug("🚀 Initializing GTE-Small-Zh ONNX embedding model...")
        model = GTESmallZhONNX()
        logger.debug(f"✅ GTE-Small-Zh model loaded (dimension: {model.get_dimension()})")
        return model
    elif model_type == "chromadb-default":
        logger.debug("Using ChromaDB default embedding model (ONNXMiniLM_L6_V2)")
        return None
    else:
        logger.warning(f"Unknown embedding model type: {model_type}, using ChromaDB default")
        return None

def initialize_system():
    """
    工厂模式：根据配置初始化底层检索引擎 (QMD) 和 上下文管理器 (OpenViking)
    使用单例模式避免重复初始化和模型重复下载
    
    支持自定义嵌入模型配置：
    - gte-small-zh: 阿里达摩院 GTE-Small-Zh ONNX INT8 量化模型（默认）
    - chromadb-default: ChromaDB 内置的 ONNXMiniLM_L6_V2 模型
    
    模型缓存策略：
    - 延迟加载：首次使用时才加载模型
    - 10 分钟空闲自动卸载：节省内存
    - 活动追踪：每次使用时重置空闲计时器
    """
    global _context_manager_instance
    
    if _context_manager_instance is not None:
        return _context_manager_instance
    
    # 1. 获取模型缓存管理器
    model_cache = get_global_model_cache()
    
    # 2. 使用缓存获取嵌入模型（延迟加载 + 10 分钟空闲卸载）
    embedding_config = CONFIG.get("embedding", {})
    model_type = embedding_config.get("model", "gte-small-zh")
    
    embedding_model = None
    if model_type != "chromadb-default":
        try:
            embedding_model = model_cache.get_model(_load_embedding_model)
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}", exc_info=True)
            logger.warning("⚠️ Falling back to ChromaDB default embedding model")
            embedding_model = None
    
    # 3. 初始化全局分块策略管理器（注入嵌入模型）
    from core.utils.chunk_strategy_manager import set_global_strategy_manager, ChunkStrategyManager
    chunk_config = CONFIG.get("chunk_strategy", {})
    default_strategy = chunk_config.get("default", "semantic")
    
    strategy_manager = ChunkStrategyManager(
        default_strategy=default_strategy,
        embedding_model=embedding_model
    )
    set_global_strategy_manager(strategy_manager)
    logger.debug(f"✅ Chunk strategy manager initialized (default: {default_strategy})")
    
    # 4. 实例化底层检索运行时（注入嵌入模型）
    qmd_runtime = QMDRuntime(CONFIG, embedding_model=embedding_model)
    
    # 5. 实例化上下文管理器，并将底层引擎注入进去 (依赖注入)
    viking_manager = OpenVikingManager(search_runtime=qmd_runtime, config=CONFIG)
    
    _context_manager_instance = viking_manager
    return viking_manager
