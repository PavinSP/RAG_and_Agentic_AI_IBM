import time
from flask import Flask, request, jsonify, render_template
from model import qwen_small_plain_response, qwen_large_plain_response

app = Flask(__name__)

MODEL_RESPONSE_FUNCS = {
    "small": qwen_small_plain_response,
    "large": qwen_large_plain_response,
}

CHAT_SYSTEM_PROMPT = (
    "You are an AI assistant helping with customer inquiries. "
    "Provide a helpful and concise response."
)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_message = data.get("message")
    model = data.get("model")

    if not user_message or not model:
        return jsonify({"error": "Missing message or model selection"}), 400
    if model not in MODEL_RESPONSE_FUNCS:
        return jsonify({"error": "Invalid model selection"}), 400

    response_func = MODEL_RESPONSE_FUNCS[model]
    start_time = time.time()

    try:
        text = response_func(CHAT_SYSTEM_PROMPT, user_message)
        return jsonify({"response": text, "duration": time.time() - start_time})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
