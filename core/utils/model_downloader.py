from rich.console import Console
from core.i18n import t

console = Console(stderr=True)

def ensure_chroma_model():
    """
    Trigger ChromaDB's built-in model download at startup with a friendly prompt,
    rather than letting it happen silently during the first query.
    """
    try:
        from chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2 import ONNXMiniLM_L6_V2
        import os

        extracted = os.path.join(ONNXMiniLM_L6_V2.DOWNLOAD_PATH, ONNXMiniLM_L6_V2.EXTRACTED_FOLDER_NAME, "model.onnx")
        if not os.path.exists(extracted):
            console.print(t("mdl_first_run", model_name=ONNXMiniLM_L6_V2.MODEL_NAME))
            console.print(t("mdl_desc"))
            console.print(f"[cyan]📁 下载位置: {ONNXMiniLM_L6_V2.DOWNLOAD_PATH}[/cyan]")

        ef = ONNXMiniLM_L6_V2()
        ef._download_model_if_not_exists()
    except Exception as e:
        console.print(t("mdl_failed", error=str(e)))
        console.print(t("mdl_hint"))
