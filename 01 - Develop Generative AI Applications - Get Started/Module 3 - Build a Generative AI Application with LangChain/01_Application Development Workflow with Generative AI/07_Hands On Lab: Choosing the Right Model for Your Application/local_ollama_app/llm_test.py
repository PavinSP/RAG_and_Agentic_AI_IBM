from model import qwen_small_response, qwen_large_response


def call_all_models(system_prompt, user_prompt):
    small_result = qwen_small_response(system_prompt, user_prompt)
    large_result = qwen_large_response(system_prompt, user_prompt)

    print("Qwen2.5 7B Response:\n", small_result)
    print("\nQwen2.5 14B Response:\n", large_result)


if __name__ == "__main__":
    call_all_models(
        "You are a helpful assistant who provides concise and accurate answers",
        "What is the capital of Canada? Tell me a cool fact about it as well",
    )
