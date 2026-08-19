# Understanding the Code: A Full Walkthrough of the Prompt Engineering Lab

This note explains every piece of code in `07b_Master Prompt Engineering and LangChain PromptTemplates (Local Ollama).ipynb`, from the Python syntax up to the LangChain/LLM concepts. It assumes you already know general programming (variables, functions, loops, dictionaries, if you've coded in any language before) but not Python's specific syntax or anything about LangChain, prompt engineering, or LLMs.

Read this top to bottom in the order the notebook itself runs — each section builds on the last.

## Table of Contents

1. Python syntax you'll see everywhere in this notebook
2. What is an LLM call, really?
3. The `OllamaLLM` class — how we talk to the local model
4. The `llm_model()` helper function
5. Prompt engineering techniques, one at a time
6. LangChain's `PromptTemplate` — templating prompts properly
7. The pipe operator and LCEL — building "chains"
8. `RunnableLambda` and `StrOutputParser` — the glue pieces
9. Putting it all together: the applications section
10. Why This Matters

---

## 1. Python syntax you'll see everywhere in this notebook

### Triple-quoted strings (`"""..."""`)

```python
prompt = """Classify the following statement as true or false:
    'The Eiffel Tower is located in Berlin.'
    Answer:
"""
```

A string wrapped in `"""` (three double-quotes) instead of a single `"` can span multiple lines. This is Python's way of writing a paragraph of text without needing `\n` (newline) characters everywhere. Almost every prompt in this notebook is written this way, because prompts are often several lines long.

### f-strings (`f"..."`)

```python
print(f"prompt: {prompt}\n")
```

An `f` right before the opening quote makes it an **f-string** — anything inside `{curly braces}` gets evaluated as a Python expression and substituted into the string. So `f"prompt: {prompt}\n"` means "take the string `'prompt: '`, then insert whatever the variable `prompt` currently holds, then add a newline." This is Python's version of string interpolation — if you've used template literals in JavaScript (`` `prompt: ${prompt}` ``), it's the same idea.

### Dictionaries (`{...}`)

```python
params = {
    "max_new_tokens": 256,
    "min_new_tokens": 10,
    "temperature": 0.5,
    "top_p": 0.2,
    "top_k": 1
}
```

A dictionary is a set of key-value pairs, written with `{key: value, key: value, ...}`. Here, `params` is a dictionary that bundles up several configuration values (all the "knobs" that control how the model generates text) into one object, so it can be passed around as a single argument instead of five separate ones. You look up a value with `params["temperature"]`, and you can merge one dictionary's values into another with `.update(...)` (used in `llm_model()`, explained below).

### `**kwargs` and `**variables` — unpacking a dictionary into arguments

```python
def format_prompt(variables):
    return prompt.format(**variables)
```

The `**` in front of a dictionary "unpacks" it — it takes every key-value pair in the dictionary and passes each one as a separate named argument. So if `variables = {"adjective": "funny", "content": "chickens"}`, then `prompt.format(**variables)` is exactly the same as writing `prompt.format(adjective="funny", content="chickens")`. This matters here because the number of variables in a prompt template changes from one exercise to the next (sometimes two, sometimes just one), so the code needs a way to pass "however many keyword arguments this dictionary happens to contain" without hardcoding their names.

### Classes and `class OllamaLLM(LLM):`

```python
class OllamaLLM(LLM):
    model: str = "qwen2.5:7b"
    temperature: float = 0.5
    max_tokens: int = 256

    @property
    def _llm_type(self) -> str:
        return "ollama"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        ...
```

`class OllamaLLM(LLM):` defines a new class named `OllamaLLM` that **inherits** from LangChain's own `LLM` base class. Inheriting means `OllamaLLM` automatically gets all the behavior of `LLM` (like the standard `.invoke()` method used throughout the notebook), and only needs to fill in the parts that are specific to *this* model — namely, how to actually send a prompt to Ollama and get text back.

- The lines `model: str = "qwen2.5:7b"` etc. are **type-annotated fields with defaults** — Pydantic (the library LangChain's base classes are built on) uses this style to declare "this object has a `model` field, it should be a string, and if nobody says otherwise it defaults to `qwen2.5:7b`."
- `@property` above `_llm_type` marks that method so it can be accessed like an attribute (`self._llm_type`) instead of being called like a function (`self._llm_type()`). LangChain requires every LLM subclass to expose a `_llm_type` so it can identify what kind of model it's wrapping internally.
- `_call` is the one method LangChain actually requires you to implement yourself — it's the function that gets invoked, under the hood, whenever someone calls `.invoke(prompt)` on your object. Everything else (`.invoke()`, chaining with `|`, etc.) is inherited for free from `LLM`.

### Type hints (`Optional[List[str]]`, `-> str`)

```python
def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
```

`prompt: str` means "this argument is expected to be a string." `-> str` after the parenthesis means "this function returns a string." `Optional[List[str]] = None` means "this argument is either a list of strings, or `None`, and if you don't pass it, it defaults to `None`." Python doesn't actually enforce these at runtime (unlike, say, Java or C#) — they're purely documentation/tooling hints for humans and editors, but LangChain's internals do rely on them being accurate to work correctly.

---

## 2. What is an LLM call, really?

Every technique in this notebook — zero-shot, few-shot, chain-of-thought, all of it — boils down to the same underlying operation: **you send a block of text to a language model, and it sends back more text that continues/responds to it.** That's it. There's no separate "mode" for zero-shot vs. few-shot inside the model itself — the *only* lever you have is what text you put into the prompt. Everything in prompt engineering is about crafting that input text cleverly enough that the model's natural next-word-prediction behavior produces the output you want.

Concretely, in this notebook, "sending a prompt to a model" means an HTTP request. When you run:

```python
response = llm_model(prompt, params)
```

what actually happens underneath is a POST request to `http://localhost:11434/api/generate` (Ollama's local API server), with the prompt text and generation settings included as JSON, and Ollama's response comes back as JSON containing the generated text. Everything else in the notebook — `PromptTemplate`, chains, the pipe operator — exists to make *constructing and dispatching* that HTTP request more organized and reusable; none of it changes what fundamentally happens at the model level.

---

## 3. The `OllamaLLM` class — how we talk to the local model

This class only exists in the *local Ollama variant* of this notebook (it replaces IBM's `WatsonxLLM`, which needs cloud credentials this variant doesn't use). Walking through `_call` line by line:

```python
def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": self.temperature, "num_predict": self.max_tokens},
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["response"]
```

- `requests.post(url, json={...})` — the `requests` library is Python's standard tool for making HTTP requests. `json={...}` tells it "serialize this dictionary as a JSON request body, and set the right `Content-Type` header automatically."
- `"model": self.model` — tells Ollama which locally-installed model to use (`qwen2.5:7b` by default here). `self.model` refers back to the class field defined earlier.
- `"stream": False` — Ollama can either stream the response back token-by-token (useful for a live-typing UI effect) or wait and send the whole response at once. We use `False` because we just want the complete text in one go.
- `"options": {"temperature": ..., "num_predict": ...}` — Ollama's equivalent of the generation parameters (`temperature` controls randomness, `num_predict` caps how many tokens/words the response can contain — comparable to `max_new_tokens` you'll see elsewhere).
- `timeout=120` — if Ollama doesn't respond within 120 seconds, raise an error instead of hanging forever. Larger/slower prompts (like the 512-token chain-of-thought ones) can genuinely take a while on a laptop CPU.
- `resp.raise_for_status()` — if the HTTP response indicates an error (like a 404 or 500), this line raises an exception immediately rather than silently continuing with a broken response.
- `resp.json()["response"]` — Ollama's JSON response body has several fields; `"response"` is the one containing the actual generated text. `.json()` parses the raw JSON text into a Python dictionary, and `["response"]` looks up that one key.

---

## 4. The `llm_model()` helper function

```python
def llm_model(prompt_txt, params=None):
    default_params = {
        "max_new_tokens": 256,
        "min_new_tokens": 0,
        "temperature": 0.5,
        "top_p": 0.2,
        "top_k": 1
    }
    if params:
        default_params.update(params)

    ollama_llm = OllamaLLM(
        model="qwen2.5:7b",
        temperature=default_params["temperature"],
        max_tokens=default_params["max_new_tokens"],
    )

    response = ollama_llm.invoke(prompt_txt)
    return response
```

This function exists purely for convenience throughout the earlier part of the notebook (before `PromptTemplate`/chains are introduced) — it's a shortcut so you can write `llm_model(prompt, params)` in one line instead of constructing an `OllamaLLM` object every single time.

- `params=None` — a default argument. If you call `llm_model(prompt)` without a second argument, `params` is `None`.
- `default_params = {...}` — a baseline set of generation settings.
- `if params: default_params.update(params)` — `.update()` merges another dictionary into this one, overwriting any keys that exist in both. So if you call `llm_model(prompt, {"max_new_tokens": 10})`, only `max_new_tokens` changes to 10; everything else in `default_params` stays at its original value. This pattern ("defaults + selective overrides") is extremely common in configuration-heavy code.
- `ollama_llm = OllamaLLM(...)` then `.invoke(prompt_txt)` — creates a fresh model wrapper with the merged settings, and calls it. `.invoke()` is the standard method every LangChain "runnable" object exposes (you'll see this exact method name reused later on `PromptTemplate`, on chains, on everything) — it means "run this thing with this input, and give me back the result."

---

## 5. Prompt engineering techniques, one at a time

Remember from Section 2: none of these are special "modes." Each one is just a different *pattern for writing the prompt text*, exploiting how the model naturally continues text.

### Basic prompt

```python
prompt = "The wind is "
```

No instruction, no context — just a sentence fragment. The model's job is simply "what word plausibly comes next?" This is the simplest possible use of an LLM, useful mainly for exploring how a model behaves with minimal guidance.

### Zero-shot prompt

```python
prompt = """Classify the following statement as true or false:
    'The Eiffel Tower is located in Berlin.'
    Answer:
"""
```

"Zero-shot" means zero examples are given — you describe the task in words ("classify... as true or false") and trust the model's general knowledge to figure out how to do it, without showing it a single worked example first.

### One-shot prompt

```python
prompt = """Here is an example of translating a sentence from English to French:
    English: "How is the weather today?"
    French: "Comment est le temps aujourd'hui?"

    Now, translate the following sentence from English to French:

    English: "Where is the nearest supermarket?"
"""
```

Here, exactly **one worked example** is included before the real question. This gives the model a concrete pattern to imitate — not just "translate this," but "translate this the same way I just showed you translating something else."

### Few-shot prompt

```python
prompt = """Here are few examples of classifying emotions in statements:
    Statement: 'I just won my first marathon!'
    Emotion: Joy

    Statement: 'I can't believe I lost my keys again.'
    Emotion: Frustration

    Statement: 'My best friend is moving to another country.'
    Emotion: Sadness

    Now, classify the emotion in the following statement:
    Statement: 'That movie was so scary I had to cover my eyes.'
"""
```

Same idea as one-shot, but with multiple (here, three) examples. More examples generally help the model infer the *pattern* more reliably, especially when the task is subtle (like emotional tone) rather than purely mechanical (like translation).

### Chain-of-thought (CoT) prompt

```python
prompt = """Consider the problem: 'A store had 22 apples. They sold 15 apples today and received a new delivery of 8 apples.
    How many apples are there now?'
    Break down each step of your calculation
"""
```

Instead of asking for just the final answer, the prompt explicitly asks the model to show its reasoning step by step. This matters because LLMs generate text one token at a time, left to right, with no ability to "think ahead" or backtrack — so if a problem needs multiple steps of reasoning, asking for the *steps themselves* to be written out (not just the final number) gives the model a chance to reason its way there incrementally, rather than trying to leap straight to a correct answer in one shot.

### Self-consistency

```python
prompt = """When I was 6, my sister was half of my age. Now I am 70, what age is my sister?
    Provide three independent calculations and explanations, then determine the most consistent result.
"""
```

This asks the model to solve the *same problem multiple times, independently*, and then compare its own answers. The idea: if a model is prone to occasional reasoning slips, having it generate several independent attempts and cross-check them increases the odds that the majority/most-consistent answer is the correct one — similar in spirit to asking three different people the same question and going with whichever answer most of them agree on.

---

## 6. LangChain's `PromptTemplate` — templating prompts properly

Every prompt above was a plain Python string, hand-written for that one specific example. That doesn't scale — what if you want the *same* prompt structure applied to many different inputs? That's what `PromptTemplate` solves.

```python
template = """Tell me a {adjective} joke about {content}.
"""
prompt = PromptTemplate.from_template(template)
prompt
```

- `{adjective}` and `{content}` are **placeholders** — much like Python f-string `{}` syntax, but these get filled in later, not immediately, and LangChain (not Python itself) is doing the substitution.
- `PromptTemplate.from_template(template)` parses that string and creates a reusable template *object* — it automatically detects that `adjective` and `content` are the two "input variables" it needs, just by scanning for `{...}` patterns in the text.

```python
prompt.format(adjective='funny', content='chickens')
```

`.format(...)` fills in the placeholders and returns the finished string — you'll get back `"Tell me a funny joke about chickens.\n"`. This is the templated equivalent of an f-string, except the template is defined once, as reusable object, and can be filled in many different ways later without rewriting it.

---

## 7. The pipe operator and LCEL — building "chains"

LCEL stands for **LangChain Expression Language** — it's the modern way LangChain recommends connecting pieces together, using Python's `|` (pipe) operator.

```python
joke_chain = (
    RunnableLambda(format_prompt)
    | llm
    | StrOutputParser()
)
```

Think of `|` here the same way you might in a Unix shell pipeline (`cat file | grep pattern | sort`) — it means "take the output of the thing on the left, and feed it as the input to the thing on the right." So this chain reads as: *take my input → format it into a prompt (`RunnableLambda(format_prompt)`) → send that prompt to the model (`llm`) → clean up the model's raw output into a plain string (`StrOutputParser()`)*.

Importantly, `|` is **not** a Python built-in behavior for arbitrary objects — LangChain's base classes (the same `LLM` class `OllamaLLm` inherits from, plus `RunnableLambda`, `StrOutputParser`, etc.) all implement Python's special `__or__` method, which is what lets `a | b` do something custom instead of throwing an error. This is the same mechanism that lets you write `3 | 5` in Python and get a bitwise-OR result for integers — LangChain repurposes that same operator for "connect these two processing steps."

Once a chain is built, you run the whole thing with `.invoke(...)`:

```python
response = joke_chain.invoke({"adjective": "happy", "content": "indians"})
```

The dictionary `{"adjective": "happy", "content": "indians"}` is the *starting* input — it flows into `format_prompt` first, then the formatted-prompt-string flows into `llm`, then the raw model output flows into `StrOutputParser()`, and whatever comes out the other end is what `response` gets.

---

## 8. `RunnableLambda` and `StrOutputParser` — the glue pieces

```python
def format_prompt(variables):
    return prompt.format(**variables)
```
```python
RunnableLambda(format_prompt)
```

`format_prompt` is just an ordinary Python function — nothing LangChain-specific about it. The problem is that a plain function can't be connected with `|` on its own, because `|` only works between objects that implement that special chaining behavior (Section 7). `RunnableLambda(...)` is a thin wrapper that takes any ordinary Python function and makes it chainable — "wrap this regular function so it behaves like a proper link in the chain."

`StrOutputParser()` solves a different, smaller problem: depending on the model/LangChain version, an LLM's raw output object can carry extra metadata (token counts, stop reasons, etc.) alongside the actual text. `StrOutputParser()` simply extracts the plain string content and discards the rest, so whatever code runs after it (a `print(...)`, or another step in a chain) gets clean text instead of having to know how to unwrap a model-specific response object.

---

## 9. Putting it all together: the applications section

Every "application" cell later in the notebook (text summarization, Q&A, text classification, SQL generation, role playing, and the Exercise 5 product-review analyzer) follows the **exact same five-step recipe**:

```python
content = "..."                          # 1. the data/problem to work on
template = "... {content} ..."           # 2. a template with placeholders
prompt = PromptTemplate.from_template(template)   # 3. turn it into a PromptTemplate
some_chain = (
    RunnableLambda(format_prompt)
    | llm
    | StrOutputParser()
)                                         # 4. build the LCEL chain
result = some_chain.invoke({"content": content})  # 5. run it
```

Once you recognize this five-step shape, every "application" in the notebook is really just this same pattern with a different template string and a different input. For example, your own Exercise 5 solution (the product review analyzer, cell 58 in the notebook) follows it precisely:

```python
template = """Analyze the following product review: "{review}".
Provide in the following format:
1) The sentiment of the review: (postive, negative or neutral)
2) Key product features mentioned
3) One sentence summary
"""
product_review_prompt = PromptTemplate.from_template(template)

def format_review_prompt(variables):
    return product_review_prompt.format(**variables)

review_analysis_chain = (
    RunnableLambda(format_review_prompt)
    | llm
    | StrOutputParser()
)

for review in reviews:
    analysis = review_analysis_chain.invoke({"review": review})
```

Same five steps: a template with one placeholder (`{review}`), a `PromptTemplate`, a formatting function wrapped in `RunnableLambda`, a chain, and `.invoke(...)` called once per review inside a loop.

---

## Why This Matters

Prompt engineering can look like a grab-bag of unrelated tricks (zero-shot, few-shot, CoT, self-consistency), but they all share one underlying truth: an LLM is a text-completion engine, and the *only* control surface you have is the text you send it. Every technique in this lab is a different strategy for writing that input text so the model's next-word predictions land where you want.

LangChain's `PromptTemplate` + LCEL (`|`) pattern matters for a parallel reason: once you understand that a "chain" is nothing more than "step A's output becomes step B's input," you can build arbitrarily complex applications (RAG pipelines, multi-agent systems, tool-using agents — the later courses in this certificate) out of the same small set of building blocks: a template, a model, an output parser, and the pipe operator connecting them. The complexity in more advanced LLM applications almost always comes from *what* gets chained together (retrievers, multiple models, tools, memory) — not from a fundamentally different mechanism than what's already fully demonstrated in this one lab.
