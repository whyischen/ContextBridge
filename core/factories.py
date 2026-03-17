from core.config import CONFIG
from core.runtimes.qmd_runtime import QMDRuntime
from core.managers.openviking_manager import OpenVikingManager

# Singleton instance cache
_context_manager_instance = None

def initialize_system():
    """
    工厂模式：根据配置初始化底层检索引擎 (QMD) 和 上下文管理器 (OpenViking)
    使用单例模式避免重复初始化和模型重复下载
    """
    global _context_manager_instance
    
    if _context_manager_instance is not None:
        return _context_manager_instance
    
    # 1. 实例化底层检索运行时
    qmd_runtime = QMDRuntime(CONFIG)
    
    # 2. 实例化上下文管理器，并将底层引擎注入进去 (依赖注入)
    viking_manager = OpenVikingManager(search_runtime=qmd_runtime, config=CONFIG)
    
    _context_manager_instance = viking_manager
    return viking_manager
