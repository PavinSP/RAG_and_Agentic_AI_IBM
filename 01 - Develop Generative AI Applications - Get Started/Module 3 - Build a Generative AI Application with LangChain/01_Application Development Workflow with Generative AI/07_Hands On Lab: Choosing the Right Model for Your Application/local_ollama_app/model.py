from langchain_core.prompts import PromptTemplate
from ollama_llm import OllamaLLM
from config import TEMPERATURE, MAX_NEW_TOKENS, QWEN_SMALL_MODEL_ID, QWEN_LARGE_MODEL_ID


def initialize_model(model_id):
    return OllamaLLM(model=model_id, temperature=TEMPERATURE, max_tokens=MAX_NEW_TOKENS)


# Initialize models
qwen_small_llm = initialize_model(QWEN_SMALL_MODEL_ID)
qwen_large_llm = initialize_model(QWEN_LARGE_MODEL_ID)

# Qwen models use ChatML-style special tokens (<|im_start|>/<|im_end|>) instead of
# Llama's <|start_header_id|> or Mistral's [INST] — same idea as the lab, different vocabulary.
qwen_template = PromptTemplate(
    template=(
        "<|im_start|>system\n{system_prompt}<|im_end|>\n"
        "<|im_start|>user\n{user_prompt}<|im_end|>\n"
        "<|im_start|>assistant\n"
    ),
    input_variables=["system_prompt", "user_prompt"],
)


def get_ai_response(model, template, system_prompt, user_prompt):
    chain = template | model
    return chain.invoke({"system_prompt": system_prompt, "user_prompt": user_prompt})


def qwen_small_response(system_prompt, user_prompt):
    return get_ai_response(qwen_small_llm, qwen_template, system_prompt, user_prompt)


def qwen_large_response(system_prompt, user_prompt):
    return get_ai_response(qwen_large_llm, qwen_template, system_prompt, user_prompt)
