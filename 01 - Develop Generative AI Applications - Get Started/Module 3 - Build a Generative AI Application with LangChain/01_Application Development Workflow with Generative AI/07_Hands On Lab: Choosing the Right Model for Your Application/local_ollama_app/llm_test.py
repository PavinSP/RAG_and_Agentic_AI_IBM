from model import qwen_small_response, qwen_large_response

SUPPORT_SYSTEM_PROMPT = (
    "You are a customer support triage assistant. Given the customer's message, "
    "summarize it, score its sentiment, classify its category (e.g. billing, "
    "technical, general), and recommend the next action a support representative "
    "should take."
)


def call_all_models(system_prompt, user_prompt):
    small_result = qwen_small_response(system_prompt, user_prompt)
    large_result = qwen_large_response(system_prompt, user_prompt)

    print("Qwen2.5 7B Response:\n", small_result)
    print("\nQwen2.5 14B Response:\n", large_result)


if __name__ == "__main__":
    call_all_models(
        SUPPORT_SYSTEM_PROMPT,
        "I've been charged twice for my subscription this month and I'm quite frustrated. Please fix this.",
    )
