from flask import Flask, request, jsonify
from langchain_core.output_parsers import JsonOutputParser
from model import qwen_small_response, qwen_large_response

app = Flask(__name__)

MODEL_RESPONSE_FUNCS = {
    "small": qwen_small_response,
    "large": qwen_large_response,
}

json_parser = JsonOutputParser()

STRUCTURED_SYSTEM_PROMPT = (
    "You are a helpful assistant. Respond ONLY with a single valid JSON object "
    "that answers the user's question. Do not include any text outside the JSON."
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
    raw_output = response_func(STRUCTURED_SYSTEM_PROMPT, user_prompt)

    try:
        parsed = json_parser.parse(raw_output)
    except Exception:
        return jsonify({"error": "Model did not return valid JSON", "raw_output": raw_output}), 502

    return jsonify(parsed)


if __name__ == "__main__":
    app.run(debug=True)
