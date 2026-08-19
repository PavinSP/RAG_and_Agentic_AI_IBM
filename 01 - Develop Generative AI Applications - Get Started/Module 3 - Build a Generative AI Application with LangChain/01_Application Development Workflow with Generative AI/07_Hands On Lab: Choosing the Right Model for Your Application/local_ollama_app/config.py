# Model parameters (equivalent of the lab's GenTextParamsMetaNames PARAMETERS dict)
TEMPERATURE = 0.0
MAX_NEW_TOKENS = 256

# Local Ollama model names, standing in for the lab's watsonx model IDs.
# Only models actually pulled locally (`ollama list`) are used here —
# the lab's Llama/Granite/Mistral IDs don't exist as local Ollama tags.
QWEN_SMALL_MODEL_ID = "qwen2.5:7b"
QWEN_LARGE_MODEL_ID = "qwen2.5:14b"
