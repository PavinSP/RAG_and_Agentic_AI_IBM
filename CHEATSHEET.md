# Cheatsheet

Formulas, code patterns, and architecture patterns extracted directly from course notes, organized by topic. Anything the course discusses only conceptually (no concrete values/code given) is flagged rather than filled in.

## Course 1: Develop Generative AI Applications — Get Started

### Module 1: Foundations of Generative AI and Prompt Engineering

See [Cheat Sheet: Foundations of Generative AI and LangChain](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/04_Module Summary and Evaluation/02_Cheat Sheet: Foundations of Generative AI and LangChain.md>) for the module's own cheat sheet, covering:

- Setup (`pip install`, `warnings`, `WatsonxLLM`, `llm_model`, `GenParams`)
- Prompting techniques (Basic, Zero-shot, One-shot, Few-shot, Chain-of-thought, Self-consistency)
- LangChain building blocks (`PromptTemplate`, `RunnableLambda`, `StrOutputParser`)
- LCEL pattern (the `|` pipe operator for chaining)

### Module 2: Introduction to LangChain in GenAI Applications

See [Cheat Sheet: Introduction to LangChain in GenAI Applications](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/02_Module Summary and Evaluation/02_Cheat Sheet.md>) for the module's own cheat sheet, covering:

- Chat models & message types (`WatsonxLLM`, `SystemMessage`/`HumanMessage`/`AIMessage`)
- Prompt templates (`PromptTemplate`, `ChatPromptTemplate`, `MessagesPlaceholder`)
- Output parsers (`JsonOutputParser`, `CommaSeparatedListOutputParser`)
- RAG pipeline (`Document`, `PyPDFLoader`, `WebBaseLoader`, `CharacterTextSplitter`, `RecursiveCharacterTextSplitter`, `WatsonxEmbeddings`, `Chroma`, retrievers, `ParentDocumentRetriever`, `RetrievalQA`)
- Memory (`ChatMessageHistory`, `ConversationBufferMemory`)
- Chains (`LLMChain`, `SequentialChain`, `RunnablePassthrough`)
- Tools & agents (`Tool`, `@tool`, `create_react_agent`, `AgentExecutor`)

### Module 3: Build a Generative AI Application with LangChain

See [Cheat Sheet: Web Development using Flask](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/01_Application Development Workflow with Generative AI/06_Cheat Sheet: Web Development using Flask.md>) for the module's own cheat sheet, covering:

- Flask app instantiation (`Flask(__name__)`)
- Routing (`@app.route` decorator)
- Response status codes (200 OK, 4xx client errors, 500 server error)
- Error handling (`@app.errorhandler`)

See [Cheat Sheet: Build GenAI Application with LangChain](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/02_Summary and Evaluation/02_Cheat Sheet.md>) for the module's end-of-module cheat sheet, covering:

- Project setup (`venv`, `pip install ibm-watsonx-ai`, `Credentials`, `GenTextParamsMetaNames`, `ModelInference`)
- LangChain prompt templates with model-specific special tokens (Llama 3's `<|begin_of_text|>`/`<|start_header_id|>`/`<|eot_id|>`)
- LangChain chaining with the `|` pipe operator
- Structured JSON outputs (`JsonOutputParser`, Pydantic `BaseModel`/`Field`)
- Flask API integration (`/generate` route, error handling)

---

## Consolidated Quick Reference

The patterns above, condensed onto one page. These are the verified working forms from the labs — including the local-Ollama substitutions, which run without cloud credentials.

### Model setup

```python
# IBM watsonx.ai (needs an API key outside Skills Network's Cloud IDE)
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

params = {GenParams.DECODING_METHOD: "greedy", GenParams.MAX_NEW_TOKENS: 256}
model = ModelInference(model_id="ibm/granite-4-h-small", params=params,
                       credentials=Credentials(url="https://us-south.ml.cloud.ibm.com"),
                       project_id="skills-network")

# LangChain wrapper around the same
from langchain_ibm import ChatWatsonx
llm = ChatWatsonx(model_id="ibm/granite-4-h-small", url="...", project_id="skills-network", params=params)
```

```python
# Local Ollama stand-in — no credentials needed (see Module 3's local_ollama_app/)
import requests
from typing import Optional, List
from langchain_core.language_models.llms import LLM

class OllamaLLM(LLM):
    model: str = "qwen2.5:7b"
    temperature: float = 0.0
    max_tokens: int = 256

    @property
    def _llm_type(self) -> str:
        return "ollama"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        r = requests.post("http://localhost:11434/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False,
                  "options": {"temperature": self.temperature, "num_predict": self.max_tokens}},
            timeout=120)
        r.raise_for_status()
        return r.json()["response"]
```

> `LLM` is Pydantic-based, so declaring fields as class attributes works. `Embeddings` is a plain `ABC` — a custom embeddings class needs an explicit `__init__`.

### Prompt templates and LCEL

```python
from langchain_core.prompts import PromptTemplate

tmpl = PromptTemplate.from_template("Tell me a {adjective} joke about {content}.")
tmpl.format(adjective="funny", content="chickens")

chain = tmpl | llm                      # RunnableSequence
chain = tmpl | llm | StrOutputParser()  # add a parser stage
result = chain.invoke({"adjective": "funny", "content": "chickens"})
```

Type coercion: a **dict** in a chain becomes `RunnableParallel` (same input, concurrent branches); a **function** becomes `RunnableLambda`.

### Model-specific special tokens

| Family | Format |
|---|---|
| Llama 3 | `<\|begin_of_text\|><\|start_header_id\|>system<\|end_header_id\|>…<\|eot_id\|>` |
| Mistral | `<s>[INST] … [/INST]` |
| Granite | `<\|system\|>` / `<\|user\|>` / `<\|assistant\|>` |
| Qwen 2.5 (ChatML) | `<\|im_start\|>system … <\|im_end\|>` |

Leave the final assistant turn *open* — the model completes it.

### Structured JSON output

```python
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the user's message")
    sentiment: int = Field(description="Sentiment score from 0 (negative) to 100 (positive)")
    category: str = Field(description="Category of the inquiry")
    action: str = Field(description="Recommended action")

json_parser = JsonOutputParser(pydantic_object=AIResponse)

chain = template | model | json_parser
chain.invoke({
    "system_prompt": system_prompt,
    "user_prompt": user_prompt,
    "format_prompt": json_parser.get_format_instructions(),  # injects the schema
})
```

Three-step pattern: **describe the shape → tell the model the shape → validate the answer against the shape.**

### RAG pipeline (Module 2)

```python
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

docs   = PyPDFLoader("paper.pdf").load()
chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
store  = Chroma.from_documents(chunks, embedding_model)
qa     = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff",
                                     retriever=store.as_retriever(),
                                     return_source_documents=True)
qa.invoke("what is this paper discussing?")
```

Flow: **load → split → embed → store → retrieve → stuff into prompt → generate.** The model only ever sees the chunks the retriever selected.

> The lab uses `from langchain.vectorstores import Chroma`, which works but emits a deprecation warning; `from langchain_community.vectorstores import Chroma` is the current path.

### Flask + LLM

```python
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    msg, model = data.get("message"), data.get("model")
    if not msg or not model:
        return jsonify({"error": "Missing message or model selection"}), 400
    try:
        return jsonify({"response": response_func(SYSTEM_PROMPT, msg)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
```

**HTTP status codes:** `200` OK · `400` bad request · `401` missing/invalid credentials · `403` insufficient permissions · `404` not found · `405` method not supported · `422` unprocessable input · `500` server error.

> **macOS gotcha:** port 5000 is taken by AirPlay Receiver (ControlCenter), which yields a confusing 403 in the browser even though Flask itself returns 200. Use `app.run(port=5050)` instead.

### Prompting techniques, ranked by cost

| Technique | What it adds | Cost |
|---|---|---|
| Zero-shot | Nothing — just the instruction | Cheapest |
| One-shot | A single worked example as a format template | + a few tokens |
| Few-shot | Several examples; pins down format and edge cases | + more tokens |
| Chain-of-thought | "Step by step" — fixes multi-step reasoning, shows its work | + many tokens |
| Self-consistency | N independent answers, take the most consistent | + N full generations |
