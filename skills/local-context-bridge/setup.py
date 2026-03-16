"""Setup and initialization for ContextBridge Skill."""

from typing import Dict, Any, Optional


class ContextBridgeSetup:
    """Handle ContextBridge setup and initialization."""

    def auto_setup(self, workspace_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Automatically setup based on environment detection.
        
        Delegates to Core's auto_configure() function.
        
        Args:
            workspace_dir: Optional custom workspace directory
            
        Returns:
            Setup result with status and details
        """
        try:
            from core.config import auto_configure
            return auto_configure(workspace_dir)
        except ImportError as e:
            return {
                "status": "error",
                "message": f"Failed to import core.config: {e}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Setup failed: {e}"
            }

    def setup_embedded_mode(self, workspace_dir: str) -> Dict[str, Any]:
        """Setup embedded mode (built-in ChromaDB)."""
        try:
            from core.config import save_config
            
            config = {
                "mode": "embedded",
                "workspace_dir": workspace_dir,
                "watch_dirs": [],
            }
            
            save_config(config)
            
            return {
                "status": "success",
                "mode": "embedded",
                "workspace": workspace_dir,
                "message": "ContextBridge configured in embedded mode"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to setup embedded mode: {e}"
            }

    def setup_external_mode(
        self,
        workspace_dir: str,
        qmd_endpoint: str,
        openviking_endpoint: str
    ) -> Dict[str, Any]:
        """Setup external mode (connect to existing services)."""
        try:
            from core.config import save_config
            
            config = {
                "mode": "external",
                "workspace_dir": workspace_dir,
                "watch_dirs": [],
                "qmd": {
                    "endpoint": qmd_endpoint,
                    "collection": "contextbridge_docs"
                },
                "openviking": {
                    "endpoint": openviking_endpoint,
                    "mount_path": "viking://contextbridge/"
                }
            }
            
            save_config(config)
            
            return {
                "status": "success",
                "mode": "external",
                "workspace": workspace_dir,
                "message": "ContextBridge configured in external mode"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to setup external mode: {e}"
            }

    def initialize_workspace(self) -> Dict[str, Any]:
        """Initialize workspace after configuration."""
        try:
            from core.config import init_workspace
            init_workspace()
            return {
                "status": "success",
                "message": "Workspace initialized successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to initialize workspace: {e}"
            }

    def get_setup_status(self) -> Dict[str, Any]:
        """Get current setup status."""
        try:
            from core.config import is_configured, CONFIG
            
            return {
                "configured": is_configured(),
                "config": CONFIG
            }
        except Exception as e:
            return {
                "configured": False,
                "error": str(e)
            }
