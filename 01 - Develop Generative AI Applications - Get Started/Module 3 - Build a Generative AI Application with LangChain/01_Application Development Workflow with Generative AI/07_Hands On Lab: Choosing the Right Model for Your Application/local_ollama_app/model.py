from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from ollama_llm import OllamaLLM
from config import TEMPERATURE, MAX_NEW_TOKENS, QWEN_SMALL_MODEL_ID, QWEN_LARGE_MODEL_ID


# Define JSON output structure.
# Includes the lab's "Exercise: Enhancing the JSON Structure" fields
# (category, action) in place of the original plain `response` field.
class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the user's message")
    sentiment: int = Field(description="Sentiment score from 0 (negative) to 100 (positive)")
    category: str = Field(description="Category of the inquiry (e.g., billing, technical, general)")
    action: str = Field(description="Recommended action for the support rep")


# JSON output parser
json_parser = JsonOutputParser(pydantic_object=AIResponse)


def initialize_model(model_id):
    return OllamaLLM(model=model_id, temperature=TEMPERATURE, max_tokens=MAX_NEW_TOKENS)


# Initialize models
qwen_small_llm = initialize_model(QWEN_SMALL_MODEL_ID)
qwen_large_llm = initialize_model(QWEN_LARGE_MODEL_ID)

# Qwen models use ChatML-style special tokens (<|im_start|>/<|im_end|>) instead of
# Llama's <|start_header_id|> or Mistral's [INST] — same idea as the lab, different vocabulary.
qwen_template = PromptTemplate(
    template=(
        "<|im_start|>system\n{system_prompt}\n{format_prompt}<|im_end|>\n"
        "<|im_start|>user\n{user_prompt}<|im_end|>\n"
        "<|im_start|>assistant\n"
    ),
    input_variables=["system_prompt", "format_prompt", "user_prompt"],
)


def get_ai_response(model, template, system_prompt, user_prompt):
    chain = template | model | json_parser
    return chain.invoke({
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "format_prompt": json_parser.get_format_instructions(),
    })


def qwen_small_response(system_prompt, user_prompt):
    return get_ai_response(qwen_small_llm, qwen_template, system_prompt, user_prompt)


def qwen_large_response(system_prompt, user_prompt):
    return get_ai_response(qwen_large_llm, qwen_template, system_prompt, user_prompt)
