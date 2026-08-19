from flask import Flask, request, jsonify
from model import qwen_small_response, qwen_large_response

app = Flask(__name__)

MODEL_RESPONSE_FUNCS = {
    "small": qwen_small_response,
    "large": qwen_large_response,
}

# Matches model.py's AIResponse schema: summary, sentiment, category, action.
SUPPORT_SYSTEM_PROMPT = (
    "You are a customer support triage assistant. Given the customer's message, "
    "summarize it, score its sentiment, classify its category (e.g. billing, "
    "technical, general), and recommend the next action a support representative "
    "should take."
)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True) or {}
    user_prompt = data.get("prompt", "")
    model_choice = data.get("model", "small")

    if not user_prompt:
        return jsonify({"error": "Missing 'prompt' in request body"}), 400
    if model_choice not in MODEL_RESPONSE_FUNCS:
        return jsonify({"error": f"Unknown model '{model_choice}', use 'small' or 'large'"}), 400

    response_func = MODEL_RESPONSE_FUNCS[model_choice]

    try:
        parsed = response_func(SUPPORT_SYSTEM_PROMPT, user_prompt)
    except Exception as exc:
        return jsonify({"error": "Model did not return valid JSON", "detail": str(exc)}), 502

    return jsonify(parsed)


if __name__ == "__main__":
    app.run(debug=True)
