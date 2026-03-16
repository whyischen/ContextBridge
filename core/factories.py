from core.config import CONFIG
from core.runtimes.qmd_runtime import QMDRuntime
from core.managers.openviking_manager import OpenVikingManager

def initialize_system():
    """
    工厂模式：根据配置初始化底层检索引擎 (QMD) 和 上下文管理器 (OpenViking)
    """
    # 1. 实例化底层检索运行时
    qmd_runtime = QMDRuntime(CONFIG)
    
    # 2. 实例化上下文管理器，并将底层引擎注入进去 (依赖注入)
    viking_manager = OpenVikingManager(search_runtime=qmd_runtime, config=CONFIG)
    
    return viking_manager

def detect_services():
    """
    检测可用的外部服务（QMD 和 OpenViking）。
    
    Returns:
        包含服务可用性和端点信息的字典
    """
    import os
    import requests
    from typing import Dict, Any
    
    def check_service(endpoint: str, timeout: int = 2) -> bool:
        """检查服务是否运行"""
        try:
            response = requests.get(f"{endpoint}/health", timeout=timeout)
            return response.status_code == 200
        except Exception:
            return False
    
    # 获取端点
    qmd_endpoint = os.environ.get("QMD_ENDPOINT", "http://localhost:9090")
    openviking_endpoint = os.environ.get("OPENVIKING_ENDPOINT", "http://localhost:8080")
    
    return {
        "qmd_available": check_service(qmd_endpoint),
        "openviking_available": check_service(openviking_endpoint),
        "qmd_endpoint": qmd_endpoint,
        "openviking_endpoint": openviking_endpoint,
    }
