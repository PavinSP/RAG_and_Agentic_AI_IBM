# Hands-on Lab: Choosing the Right Model for Your Application

> This lab is a multi-file Flask project built step-by-step in IBM's Cloud IDE, not a single notebook — reformatted here as a reading note. A companion runnable version rewired to local Ollama models lives alongside it (see [Local Ollama Version](#local-ollama-version) below).

## Build Your First GenAI Application the Right Way

Build a smart AI-powered web application using Flask and cutting-edge language models. This hands-on project teaches you to create intelligent applications that generate structured responses and leverage enterprise-grade AI tools — integrating watsonx.ai, implementing JSON parsing, and engineering prompts that deliver consistent, actionable results.

### Learning Objectives

By the end of this project, you will be able to:

- Develop a Flask web application integrated with AI capabilities
- Utilize the `ibm-watsonx-ai` library to interact with advanced language models
- Implement LangChain's `JsonOutputParser` for structured AI outputs
- Apply prompt engineering techniques for generating actionable JSON responses
- Compare and evaluate different language models including Llama, Granite, Mixtral
- Enhance your application with modular and reusable AI integration code

## How Large Language Models Work

Large Language Models are thinking machines that can understand and generate human language with incredible fluency. Unlike traditional software that follows rigid rules, LLMs learn patterns from vast amounts of text to develop an intuitive understanding of language, knowledge, and reasoning — like having read millions of books and learned to predict what comes next in any conversation.

**Tokenization.** Every journey begins with breaking text into digestible pieces called tokens. The sentence "Hello world" becomes separate tokens that the model can process. Using techniques like Byte Pair Encoding, common letter combinations become single tokens, while rare words get split apart. Each token gets assigned a unique number, transforming human language into mathematical data the model can understand.

**Embeddings.** Token numbers are transformed into vectors — lists of hundreds of decimal numbers that capture meaning in mathematical space. Words with similar meanings cluster together in this high-dimensional space, like "cat" and "dog" being closer than "cat" and "airplane."

**Attention is All You Need.** The transformer's secret weapon is attention mechanisms. As the model processes each word, it simultaneously looks at every other word in the sentence to understand relationships and context. When processing "The cat sat on the mat," the model learns that "sat" relates most strongly to "cat" as the subject performing the action. Multiple attention heads work in parallel, each specializing in different types of relationships like grammar, meaning, or long-range dependencies.

**Transformer Layers.** Attention mechanisms stack into layers. Information flows upward through dozens of layers, with each one building more sophisticated representations. Early layers might focus on basic grammar and word relationships, while deeper layers develop complex reasoning abilities and factual knowledge. The model also passes forward the original input of each layer alongside the new transformations, which helps preserve important details and prevents information from being lost or distorted as it moves through many layers.

**Next Token Prediction.** The model's training objective is simple: predict the next word in a sequence. Given "The capital of France is," it learns to predict "Paris." This simple task teaches remarkable complexity — grammar, facts, reasoning, and even creativity — because language follows patterns that encode the structure of how we think.

**Massive Scale Training.** Training happens on an enormous scale: the model processes trillions of words from books, articles, and websites, learning from the collective knowledge of the internet and beyond. Thousands of powerful computers work together for months, adjusting billions of parameters through backpropagation. Each time the model makes a wrong prediction, it slightly adjusts its internal connections to do better next time.

**Inference.** During actual use, the trained model generates text one token at a time. It considers everything you've said, processes it through all its layers of understanding, and predicts the most appropriate next word. That word gets added to the conversation and fed back in to predict the following word, creating a chain of coherent thought. Temperature and sampling control the trade-off between creativity versus consistency.

## Setting Up Your Development Environment

The original lab environment is IBM's Cloud IDE (Ubuntu 22.04).

**Step 1: Create your project directory**

```bash
mkdir genai_flask_app
cd genai_flask_app
```

**Step 2: Set up a Python virtual environment**

```bash
python3.11 -m venv venv
source venv/bin/activate
```

**Step 3: Install the `ibm-watsonx-ai` library**

```bash
pip install ibm-watsonx-ai==1.3.39
```

This installs `ibm-watsonx-ai`, used to configure and call watsonx-hosted LLMs.

## Using the `ibm-watsonx-ai` Python Library

The lab's first call is to `ibm/granite-4-h-small`, in a file `capital.py`:

```python
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames
```

This imports the modules needed to authenticate, interact with the API, define models, and set parameters.

```python
credentials = Credentials(
    url="https://us-south.ml.cloud.ibm.com",
    # api_key = "<YOUR_API_KEY>"  # Skills Network's Cloud IDE handles this automatically
)
```

This sets up the `Credentials` object to authenticate with IBM watsonx.ai.

```python
params = {
    GenTextParamsMetaNames.DECODING_METHOD: "greedy",
    GenTextParamsMetaNames.MAX_NEW_TOKENS: 100
}
```

- **`DECODING_METHOD`** controls how the LLM selects its next token. `greedy` always picks the most probable next token (deterministic, predictable). `sampling` introduces randomness (with `temperature` as a key control) for more creative, varied outputs.
- **`MAX_NEW_TOKENS`** caps how many tokens the model can generate in a response — important for managing cost, since both input and output tokens usually count toward it.

```python
model = ModelInference(
    model_id='ibm/granite-4-h-small',
    params=params,
    credentials=credentials,
    project_id="skills-network"
)
```

```python
text = """
Only reply with the answer. What is the capital of Canada?
"""

print(model.generate(text)['results'][0]['generated_text'])
```

```bash
python capital.py
```

Expected output: `Ottawa.`

## Trying Other LLMs

Choosing an LLM is deceptively complicated. Specs alone — token limits, training data, parameter count — only take you so far; the real test is how a model performs for your specific use case. Factors to weigh:

- **Capabilities:** Does the model meet your needs? Some models are multimodal (text + images); others are text-only.
- **Cost:** Input and output token pricing, balanced against performance.
- **Speed:** How quickly the model generates responses — critical for real-time applications.
- **Quality:** How accurate and relevant the outputs are for your tasks, tested empirically.
- **Other considerations:** Vendor lock-in, licensing restrictions, integration with existing systems.

Specs can guide you, but hands-on testing against your own use cases is the only way to truly know if a model works for your scenario.

Swapping `capital.py`'s model to `meta-llama/llama-4-maverick-17b-128e-instruct-fp8`:

```python
model = ModelInference(
    model_id='meta-llama/llama-4-maverick-17b-128e-instruct-fp8',
    params=params,
    credentials=credentials,
    project_id="skills-network"
)
```

Running it produced an unexpected result — something like:

> "Ottawa - IELTS Listening Sample Question. To answer this question, we simply need to identify the capital city of Canada. The capital of Canada is Ottawa"

Not quite the clean answer expected. The fix (special tokens) is covered in the next section.

### Models referenced in the lab (as listed, June 2026 pricing)

| Provider | Model ID | Use Cases | Context Length | Price (USD / million tokens) |
|---|---|---|---|---|
| IBM | `ibm/granite-4-h-small` | Q&A, summarization, classification, generation, extraction, RAG, coding, multi-tool agentic workflows | 128k | In: 0.06 / Out: 0.25 |
| Meta | `meta-llama/llama-4-maverick-17b-128e-instruct-fp8` | Multimodal reasoning, long-context processing, code generation/analysis, multilingual (200 languages), STEM/logical reasoning | 1M | In: 0.35 / Out: 1.40 |
| Mistral | `mistralai/mistral-small-3-1-24b-instruct-2503` | Instruction following, conversational assistance, image understanding, function calling, multilingual Q&A, summarization, classification, generation, RAG | 128k | In: 0.10 / Out: 0.30 |
| Mistral | `mistralai/mistral-medium-2505` | Programming, mathematical reasoning, long document understanding, summarization, dialogue, multimodal (text + image) | 128k | In: 0.40 / Out: 2.00 |

## Special Tokens & Prompt Formatting

Without special tokens, a model's responses can be unpredictable because it lacks cues to interpret the structure, context, or intent of the input. Different model families use different conventions.

**Llama**

| Token | Description |
|---|---|
| `<\|begin_of_text\|>` | Start of the prompt |
| `<\|end_of_text\|>` | End of the prompt |
| `<\|start_header_id\|>` / `<\|end_header_id\|>` | Enclose the role for a message. Roles: `system`, `user`, `assistant`, `ipython` |
| `<\|eot_id\|>` | End of turn — signals the model has finished generating a response |

Llama roles:
- **system** — sets the assistant's behavior, tone, context, and guidelines.
- **user** — the human's queries, requests, or commands.
- **assistant** — the AI-generated response.
- **ipython** (Llama 3.1+) — marks tool-call output sent back to the model; not used in this lab.

**Mistral**

| Token | Description |
|---|---|
| `<s>` | Start of a sentence/sequence |
| `<\s>` | End of a sentence/sequence |
| `[INST]` / `[/INST]` | Enclose an instructional message/command |

**Granite**

| Token | Description |
|---|---|
| `<\|system\|>` | The system prompt for the foundation model |
| `<\|user\|>` | The query text to be answered |
| `<\|assistant\|>` | Cue at the end of the prompt indicating a generated answer is expected |

## Prompting with Special Tokens

Updating the prompt to use Llama's special tokens:

```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an expert assistant who provides concise and accurate answers.<|eot_id|>

<|start_header_id|>user<|end_header_id|>
What is the capital of Canada?<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
```

Output:

```
The capital of Canada is Ottawa.
```

**Why did that happen?** LLMs aren't yet equipped for true logical reasoning — they transform content into tokens and predict the next token based on probability, not understanding. Asked "Why did the chicken cross the road?", a model might respond "Is a common riddle joke" just as readily as "To get to the other side." Using special tokens to clearly mark roles gives tighter control over the model's responses, aligning outputs more closely with the intended outcome.

## From Prompts to Structured Outputs

Special tokens give better control over *how* a model responds, but the output is still raw text. Real-world applications usually need structured data that code can parse, store, and act on.

Instead of:

```
The capital of Canada is Ottawa.
```

The goal is something like:

```json
{ "country": "Canada", "capital": "Ottawa" }
```

Managing prompts, roles, and output formatting manually gets messy fast — which is where LangChain comes in.

## What is LangChain?

LangChain provides an abstraction layer over multiple language models, letting developers use a consistent API and toolset to switch between or combine different models. It includes built-in utilities for managing prompts, chaining responses, parsing outputs, and structuring conversations.

**Why use LangChain?**

- **Consistent and modular integration** — reusable components let you swap models without major code changes.
- **Structured outputs with JSON parsers** — helps ensure model responses are consistent and easily parsed.
- **Support for multi-step workflows** — enables complex workflows involving multiple prompts and multiple models.

## Creating Your Flask Application

Install Flask and LangChain libraries:

```bash
pip install Flask langchain-ibm langchain
```

**Step 1: Create `app.py`**

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    # This is where we'll add our AI logic later
    return jsonify({"message": "AI response will be generated here"})

if __name__ == '__main__':
    app.run(debug=True)
```

- Imports the necessary Flask modules.
- Creates a Flask application instance.
- Defines a `/generate` route that will handle POST requests (where the AI logic goes).
- Returns a placeholder JSON response for now.
- The `if __name__ == '__main__':` block runs the Flask dev server when the file is executed directly.

## Integrating AI Models with LangChain

**Step 1: `config.py`** — centralizes model parameters and credentials.

```python
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# Model parameters
PARAMETERS = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 256,
}

# watsonx credentials
# Note: Skills Network's Cloud IDE handles the API key automatically.
CREDENTIALS = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "project_id": "skills-network"
}

# Model IDs
LLAMA_MODEL_ID = "meta-llama/llama-3-2-11b-vision-instruct"
GRANITE_MODEL_ID = "ibm/granite-4-h-small"
MISTRAL_MODEL_ID = "mistralai/mistral-small-3-1-24b-instruct-2503"
```

**Step 2: `model.py`** — model integration.

```python
from langchain_ibm import ChatWatsonx
from langchain_core.prompts import PromptTemplate
from config import PARAMETERS, LLAMA_MODEL_ID, GRANITE_MODEL_ID, MISTRAL_MODEL_ID
```

- `ChatWatsonx` — the interface to IBM watsonx.ai models.
- `PromptTemplate` — creates dynamic prompts with placeholders for AI input.
- The rest are the configuration values defined in `config.py`.

```python
# Function to initialize a model
def initialize_model(model_id):
    return ChatWatsonx(
        model_id=model_id,
        url="https://us-south.ml.cloud.ibm.com",
        project_id="skills-network",
        params=PARAMETERS
    )

# Initialize models
llama_llm = initialize_model(LLAMA_MODEL_ID)
granite_llm = initialize_model(GRANITE_MODEL_ID)
mistral_llm = initialize_model(MISTRAL_MODEL_ID)
```

This uses LangChain's `ChatWatsonx`, a wrapper around the watsonx API client, to initialize each model.

```python
# Prompt templates
llama_template = PromptTemplate(
    template='''<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>
{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
''',
    input_variables=["system_prompt", "user_prompt"]
)

granite_template = PromptTemplate(
    template="<|system|>{system_prompt}\n\<|user|>{user_prompt}\n<|assistant|>",
    input_variables=["system_prompt", "user_prompt"]
)

mistral_template = PromptTemplate(
    template="<s>[INST]{system_prompt}\n{user_prompt}[/INST]",
    input_variables=["system_prompt", "user_prompt"]
)
```

`PromptTemplate` makes prompts reusable and adaptable: placeholders like `system_prompt` and `user_prompt` get filled dynamically at runtime, and each model gets the template format it expects.

```python
def get_ai_response(model, template, system_prompt, user_prompt):
    chain = template | model
    return chain.invoke({'system_prompt': system_prompt, 'user_prompt': user_prompt})
```

`get_ai_response` chains a prompt template and model together with the pipe operator (`|`), feeding the template's output directly into the model as input.

```python
# Model-specific response functions
def llama_response(system_prompt, user_prompt):
    return get_ai_response(llama_llm, llama_template, system_prompt, user_prompt)

def granite_response(system_prompt, user_prompt):
    return get_ai_response(granite_llm, granite_template, system_prompt, user_prompt)

def mistral_response(system_prompt, user_prompt):
    return get_ai_response(mistral_llm, mistral_template, system_prompt, user_prompt)
```

Each model-specific function calls the generic `get_ai_response` with its own model and template, so the right prompt format is always used for the right model. This modular approach makes it easy to add or swap models later.

## Sanity Check

Testing all three models together, in `llm_test.py`:

```python
from model import llama_response, granite_response, mistral_response

def call_all_models(system_prompt, user_prompt):
    llama_result = llama_response(system_prompt, user_prompt)
    granite_result = granite_response(system_prompt, user_prompt)
    mistral_result = mistral_response(system_prompt, user_prompt)

    print("Llama Response:\n", llama_result.content)
    print("\nGranite Response:\n", granite_result.content)
    print("\nMistral Response:\n", mistral_result.content)

# Example call to test all models
call_all_models(
    "You are a helpful assistant who provides concise and accurate answers",
    "What is the capital of Canada? Tell me a cool fact about it as well"
)
```

```bash
python llm_test.py
```

Expected output (paraphrased — exact wording varies per run):

- **Llama:** The capital of Canada is Ottawa. A cool fact: the Rideau Canal, a UNESCO World Heritage Site, becomes the world's largest naturally frozen ice skating rink in winter.
- **Granite:** The capital of Canada is Ottawa, known for historic architecture, museums, and a vibrant cultural scene — also home to that same Rideau Canal Skateway.
- **Mistral:** The capital of Canada is Ottawa, one of the coldest capitals in the world, with winter temperatures dropping to -40°C, making the frozen Rideau Canal a popular skating destination.

## Setting up JSON Outputs

An important step: making sure the AI's output follows a well-defined format. This is essential for taking the output and integrating it seamlessly into other systems, like a website.

Pydantic can define a clear schema for the AI's response, ensuring consistent structure and validation — enforcing the correct format and making data integration smoother and more reliable.

```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
```

`BaseModel` and `Field` define the JSON output structure. `JsonOutputParser` automatically parses and validates the AI's output into that structured format.

### Pydantic Model

```python
# Define JSON output structure
class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the user's message")
    sentiment: int = Field(description="Sentiment score from 0 (negative) to 100 (positive)")
    response: str = Field(description="Suggested response to the user")
```

### JSON Output Parser

```python
# JSON output parser
json_parser = JsonOutputParser(pydantic_object=AIResponse)
```

The expected output is defined using the `AIResponse` Pydantic model, specifying fields like `summary`, `sentiment`, and `response`. `JsonOutputParser` ensures the AI output conforms to this structure, providing well-formatted, validated data for further use in the application.

### Updating the Chain

```python
def get_ai_response(model, template, system_prompt, user_prompt):
    chain = template | model | json_parser
    return chain.invoke({'system_prompt': system_prompt, 'user_prompt': user_prompt, 'format_prompt': json_parser.get_format_instructions()})
```

`json_parser` is added to the chain, and `json_parser.get_format_instructions()` updates the prompt with instructions to respond in well-structured JSON as defined by the `AIResponse` class.

### Putting it All Together

`AIResponse` and `json_parser` go at the top of `model.py`, along with the extra `json_parser` link in the chain inside `get_ai_response`. The full file:

```python
from langchain_ibm import WatsonxLLM
from langchain_ibm import ChatWatsonx
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from config import PARAMETERS, CREDENTIALS, LLAMA_MODEL_ID, GRANITE_MODEL_ID, MISTRAL_MODEL_ID

# Define JSON output structure
class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the user's message")
    sentiment: int = Field(description="Sentiment score from 0 (negative) to 100 (positive)")
    response: str = Field(description="Suggested response to the user")

# JSON output parser
json_parser = JsonOutputParser(pydantic_object=AIResponse)

# Function to initialize a model
def initialize_model(model_id):
    return ChatWatsonx(
        model_id=model_id,
        url="https://us-south.ml.cloud.ibm.com",
        project_id="skills-network",
        params=PARAMETERS
    )

# Initialize models
llama_llm = initialize_model(LLAMA_MODEL_ID)
granite_llm = initialize_model(GRANITE_MODEL_ID)
mistral_llm = initialize_model(MISTRAL_MODEL_ID)

# Prompt templates
llama_template = PromptTemplate(
    template='''<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system_prompt}\n{format_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>
{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
''',
    input_variables=["system_prompt", "format_prompt", "user_prompt"]
)

granite_template = PromptTemplate(
    template="System: {system_prompt}\n{format_prompt}\nHuman: {user_prompt}\nAI:",
    input_variables=["system_prompt", "format_prompt", "user_prompt"]
)

mistral_template = PromptTemplate(
    template="<s>[INST]{system_prompt}\n{format_prompt}\n{user_prompt}[/INST]",
    input_variables=["system_prompt", "format_prompt", "user_prompt"]
)

def get_ai_response(model, template, system_prompt, user_prompt):
    chain = template | model | json_parser
    return chain.invoke({'system_prompt': system_prompt, 'user_prompt': user_prompt, 'format_prompt': json_parser.get_format_instructions()})

# Model-specific response functions
def llama_response(system_prompt, user_prompt):
    return get_ai_response(llama_llm, llama_template, system_prompt, user_prompt)

def granite_response(system_prompt, user_prompt):
    return get_ai_response(granite_llm, granite_template, system_prompt, user_prompt)

def mistral_response(system_prompt, user_prompt):
    return get_ai_response(mistral_llm, mistral_template, system_prompt, user_prompt)
```

Note the Granite template switched from its earlier `<|system|>`/`<|user|>`/`<|assistant|>` special-token format to a plain `System:`/`Human:`/`AI:` format here — the lab doesn't call out why, but plain role labels tend to be more robust once a JSON-formatting instruction block gets inserted into the prompt.

### Exercise: Enhancing the JSON Structure

Add a new field to the `AIResponse` class that recommends the next step the support representative may take to resolve the issue:

1. Update the `AIResponse` class in `model.py`.
2. Modify the system prompt in `app.py` to include this new field.
3. Test the changes with a variety of user messages.

```python
class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the user's message")
    sentiment: int = Field(description="Sentiment score from 0 (negative) to 100 (positive)")
    category: str = Field(description="Category of the inquiry (e.g., billing, technical, general)")
    action: str = Field(description="Recommended action for the support rep")
```

> The exercise's target `AIResponse` also drops the `response` field in favor of `category` and `action` — matching the schema as given in the exercise text.

## Enhancing Your Flask Application with AI Capabilities

Now that the AI models are set up, they get integrated into the Flask application.

### Step 1: Update `app.py`

```python
from flask import Flask, request, jsonify, render_template
from model import llama_response, granite_response, mistral_response
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_message = data.get('message')
    model = data.get('model')

    if not user_message or not model:
        return jsonify({"error": "Missing message or model selection"}), 400

    system_prompt = "You are an AI assistant helping with customer inquiries. Provide a helpful and concise response."

    start_time = time.time()

    try:
        if model == 'llama':
            result = llama_response(system_prompt, user_message)
        elif model == 'granite':
            result = granite_response(system_prompt, user_message)
        elif model == 'mistral':
            result = mistral_response(system_prompt, user_message)
        else:
            return jsonify({"error": "Invalid model selection"}), 400

        result['duration'] = time.time() - start_time
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

- Imports the model-specific response functions.
- The `/generate` route now expects JSON input with `message` and `model` fields.
- Adds error handling for missing inputs.
- Wraps AI processing in a try/except block to handle potential errors.
- Measures and includes processing time (`duration`) in the response.

This setup allows the app to handle requests for different models with robust error handling.

### Step 2: Create `templates/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Assistant</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body class="font-ibm-plex">
    <div class="app-container">
        <!-- Header -->
        <div class="header">
            <div class="header-content">
                <h1 class="header-title">AI Assistant</h1>
                <button id="clearBtn" class="clear-btn" style="display: none;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="m3 6 18 0"></path>
                        <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                        <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                    </svg>
                    Clear Chat
                </button>
            </div>
        </div>

        <!-- Chat Container -->
        <div class="chat-container">
            <!-- Messages Area -->
            <div class="messages-area">
                <div class="messages-content">
                    <!-- Welcome Screen -->
                    <div id="welcomeScreen" class="welcome-screen">
                        <div class="welcome-icon">
                            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
                                <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
                                <line x1="9" y1="9" x2="9.01" y2="9"/>
                                <line x1="15" y1="9" x2="15.01" y2="9"/>
                            </svg>
                        </div>
                        <h2 class="welcome-title">Welcome to AI Assistant</h2>
                        <p class="welcome-text">Choose a model and start a conversation. I'm here to help with your questions and tasks.</p>
                    </div>

                    <!-- Messages Container -->
                    <div id="messagesContainer" class="messages-container"></div>

                    <!-- Loading Indicator -->
                    <div id="loadingIndicator" class="loading-indicator" style="display: none;">
                        <div class="loading-bubble">
                            <div class="loading-content">
                                <div class="loading-dots">
                                    <div class="dot"></div>
                                    <div class="dot"></div>
                                    <div class="dot"></div>
                                </div>
                                <span class="loading-text">AI is thinking...</span>
                            </div>
                        </div>
                    </div>

                    <!-- Messages End -->
                    <div id="messagesEnd"></div>
                </div>
            </div>

            <!-- Input Area -->
            <div class="input-area">
                <div class="input-content">
                    <form id="chatForm" class="chat-form">
                        <!-- Model Selection -->
                        <div class="model-section">
                            <span class="model-label">Model:</span>
                            <div class="select-wrapper">
                                <select id="modelSelect" class="model-select">
                                    <option value="llama">Llama</option>
                                    <option value="granite">Granite</option>
                                    <option value="mistral">Mistral</option>
                                </select>
                            </div>
                        </div>

                        <!-- Message Input -->
                        <div class="input-section">
                            <div class="textarea-container">
                                <textarea
                                    id="messageInput"
                                    class="message-textarea"
                                    placeholder="Type your message... (Enter to send, Shift+Enter for new line)"
                                    rows="1"
                                ></textarea>
                            </div>

                            <button type="submit" id="sendButton" class="send-button">
                                <svg id="sendIcon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <line x1="22" y1="2" x2="11" y2="13"></line>
                                    <polygon points="22,2 15,22 11,13 2,9 22,2"></polygon>
                                </svg>
                                <div id="loadingSpinner" class="loading-spinner" style="display: none;">
                                    <div class="spinner"></div>
                                </div>
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <script src="/static/script.js"></script>
</body>
</html>
```

Simple HTML providing a form that calls the `/generate` endpoint, passing a message and model selection.

### Step 3: Adding CSS and JavaScript

Flask serves static assets (CSS, JS) from a dedicated `static/` folder. The lab hosts the frontend's CSS and JavaScript as GitHub Gists rather than inline in the reading:

```bash
mkdir static
wget -O static/script.js "https://gist.githubusercontent.com/tenzinmigmar/0168709391266a8d8da7936f1a866c71/raw/95f4f4e1a1966b3f5183dd2f822cfcfd08d2238a/script.js"
wget -O static/styles.css "https://gist.githubusercontent.com/tenzinmigmar/278575598f79a4940993a1fc8640a60a/raw/24eda98885e854b01b4a46d1756112e91d3acc10/styles.css"
```

### Step 4: Testing the AI-Enabled Application

```bash
python app.py
```

This starts the Flask development server on port 5000. In IBM's Cloud IDE, a "Test your application" button opens the running app; running locally, that's simply `http://127.0.0.1:5000`.

Try different messages and models to see how the responses vary — congratulations, a fully LLM-enabled Flask application.

## Conclusion and Next Steps

### Key Takeaways

- Set up a Flask application with AI capabilities.
- Integrated and compared multiple language models (Llama, Granite, Mistral).
- Implemented LangChain's `JsonOutputParser` for structured AI outputs.
- Gained insights into prompt engineering and model performance analysis.
- Created a modular and maintainable codebase for AI integration.

### Next Steps

To further enhance this application:

- **Implement caching** — improve performance for repeated queries.
- **Explore advanced LangChain features** — e.g. memory for maintaining conversation context.
- **Add more models** — try integrating other models available through watsonx.ai.
- **Implement A/B testing** — compare responses from different models for the same query.
- **Enhance error handling** — more robust error handling and logging.
- **Explore IBM Cloud services** — expand the application's capabilities with other IBM Cloud integrations.

### Further Learning

- IBM's hands-on learning path on agentic AI, with more guided projects like this one.
- The IBM watsonx.ai documentation, for more advanced features.
- LangChain, for more sophisticated AI application architectures.
- Prompt engineering techniques, to improve AI model outputs.

## Local Ollama Version

This lab's full stack — the `/generate` route wired to the JSON-structured chain, the `index.html` chat UI, and the `static/script.js` + `static/styles.css` assets — needs an IBM Cloud API key to run against watsonx.ai outside Skills Network's Cloud IDE. A working local version of this same project — same file structure, same LangChain patterns and UI, rewired to local Ollama models — lives in [`local_ollama_app/`](<./local_ollama_app/>).
