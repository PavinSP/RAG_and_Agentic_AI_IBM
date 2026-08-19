# Understanding This Lab, in Plain English

This is a from-scratch, no-jargon walkthrough of everything in this lab — what an AI model actually is, why the code is shaped the way it is, how every file talks to every other file, and why you got that weird "403 Access Denied" error in your browser. Nothing here assumes you already know programming terms; anything technical gets explained the first time it shows up.

---

## Part 1: The Big Picture — What Are We Even Building?

Imagine you want to build a customer-support chat website. A person types a message like "my internet has been down for three days," and you want a smart robot to write back a helpful reply.

To do that you need three things:

1. **A brain** — something that can actually understand text and write a reply. That's the AI model (like ChatGPT, but here we're using free models running on your own laptop called Qwen2.5).
2. **A way to talk to the brain from code** — you can't just yell at the AI model in English from Python; you need a structured way to send it text and get text back. That's what **LangChain** gives us.
3. **A website** — something a person can actually open in a browser, type into, and see replies. That's what **Flask** gives us.

This lab builds exactly that, layer by layer. Let's go through each layer.

---

## Part 2: What Is an AI Model, Really?

Skip this if you already feel solid on this — but here's the short version, because everything else builds on it.

An AI language model (like Qwen2.5, Llama, GPT, Granite, Mistral — there are many) is a giant mathematical machine that was shown an enormous amount of text (basically much of the internet and books) and trained to do one very simple thing over and over: **guess the next word**.

Given "The capital of Canada is ___", it learned that "Ottawa" is overwhelmingly the most likely next word. Given "Once upon a ___", it learned "time" is most likely. It does this same guessing game, one word-piece at a time, thousands of times per second, and stringing those guesses together is what looks like "the AI writing a reply."

It doesn't "know" facts the way a person does — it has absorbed statistical patterns from text. That's why it can sometimes be confidently wrong (this is called "hallucination"), and why giving it clearer instructions (a better *prompt*) makes it much more reliable, even though the underlying machine hasn't changed at all.

### Tokens — the model's actual units of text

The model doesn't see "words" the way you do. It breaks text into chunks called **tokens** — sometimes a whole word, sometimes half a word, sometimes just a punctuation mark. "Hello world" might become two tokens: `Hello` and ` world`. This matters practically because:

- Every model has a maximum number of tokens it can "see" at once (its **context window**).
- Companies charge money per token when you use their hosted models (that's why the lab's pricing table showed "$ per million tokens").
- A setting called `MAX_NEW_TOKENS` (you'll see this in the code) caps how long the model's *reply* is allowed to be, so it doesn't ramble forever and cost you money or time.

### Why different models exist at all

Just like there are different cars for different jobs (a truck for hauling, a sports car for speed, a small car for cheap commuting), different AI models trade off:

- **Quality** — how smart/accurate the answers are.
- **Speed** — how fast it replies.
- **Cost** — how much money it costs per use (if it's a paid cloud model).
- **Size** — bigger models (more "parameters," which are the internal numbers the model adjusted during training) are usually smarter but slower and more expensive.

This whole lab is literally called "Choosing the Right Model for Your Application" because picking the right one for your specific job is a real, practical decision — not just "always pick the biggest one."

---

## Part 3: Why watsonx.ai vs. Why We Used Ollama Instead

The original Coursera lab uses **IBM watsonx.ai** — IBM's paid cloud service that hosts big models (Llama, Granite, Mistral) on IBM's own servers. You send your text over the internet to IBM's computers, their computer runs the model, and sends the reply back. This needs a paid API key and works over the internet.

Since running this outside Coursera's practice environment would need that paid key, we swapped it for **Ollama** — a free program that runs AI models directly *on your own Mac*, no internet or payment needed. You already had two models downloaded: `qwen2.5:7b` (smaller/faster) and `qwen2.5:14b` (bigger/smarter, "7b"/"14b" meaning roughly 7 billion / 14 billion parameters — the internal adjustable numbers from training).

The tradeoff: watsonx's models (Llama, Granite, Mistral) aren't available to run locally for free, so we use Qwen2.5 instead. The *code pattern* — how you structure prompts, chains, and a web app around a model — is identical either way. That's the actual point of the lab: not memorizing specific model names, but learning the reusable pattern.

---

## Part 4: What Is LangChain, and Why Not Just Call the Model Directly?

You technically *could* just send text straight to Ollama yourself with basic code, no LangChain. So why bother with LangChain at all?

LangChain is a toolkit that gives you **standardized building blocks** for talking to AI models, so that:

- Swapping one model for another (say, from Qwen to Llama, or from your laptop to the cloud) means changing a tiny bit of code, not rewriting everything.
- You can **chain** steps together — "format my prompt, THEN send it to the model, THEN parse its answer into neat data" — using one clean, readable line of code instead of a tangle of manual steps.
- There are ready-made tools for common problems, like making sure the AI's reply is valid JSON (structured data), which we'll get to.

Think of LangChain like a **universal remote control**. Every TV brand has different buttons and menus, but a universal remote gives you the same "power," "volume," "channel" buttons no matter which TV you point it at. LangChain does that for AI models.

### The pipe operator: `|`

You'll see code like:

```python
chain = template | model | json_parser
```

That `|` symbol is LangChain's way of saying **"take the output of the thing on the left, and feed it as input to the thing on the right."** Read it left to right like an assembly line:

1. `template` — first, fill in a prompt template with your actual text.
2. `| model` — take that filled-in prompt and hand it to the AI model to generate a reply.
3. `| json_parser` — take the model's raw text reply and turn it into clean, structured data.

It's exactly like a factory conveyor belt: raw prompt goes in one end, a fully processed, structured answer comes out the other end, and each station along the belt does one specific job.

---

## Part 5: Walking Through Every File in `local_ollama_app/`

Here's the actual folder, and what each piece is responsible for:

```
local_ollama_app/
├── ollama_llm.py     ← teaches LangChain how to talk to Ollama
├── config.py         ← settings (which models, how creative, how long)
├── model.py          ← sets up the models + prompt templates + the "chains"
├── app.py            ← the website itself (Flask)
├── templates/
│   └── index.html    ← the webpage's HTML skeleton
└── static/
    ├── script.js     ← the webpage's interactive behavior
    └── styles.css    ← the webpage's visual styling
```

### `ollama_llm.py` — the translator/adapter

```python
class OllamaLLM(LLM):
    model: str = "qwen2.5:7b"
    temperature: float = 0.0
    max_tokens: int = 256

    def _call(self, prompt, stop=None, **kwargs):
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False, ...},
        )
        return resp.json()["response"]
```

LangChain has its own idea of what "a model" is — it expects any model to have a specific shape/interface so it can plug into chains (those `|` conveyor belts). But Ollama doesn't know or care about LangChain; Ollama just listens for plain web requests on your computer at address `http://localhost:11434`.

**`localhost:11434`** simply means "the Ollama program that's currently running on this same computer, listening on door number 11434." (Every program that talks over the network picks a "port," which is just a numbered door on your machine.)

This file is a **translator**: it wraps Ollama up in the shape LangChain expects, so that from LangChain's perspective, this looks and acts exactly like any other AI model it knows how to use. Internally, all it does is send an HTTP request (a structured internet-style message, even though it's just going to your own machine) to Ollama saying "here's a prompt, please generate a reply," and hands back whatever text Ollama sends.

- **`temperature`** — controls randomness/creativity. `0.0` means "always pick the most likely/safest next word" (consistent, boring, predictable). Higher numbers (like `0.8`) let it take more creative risks, sometimes at the cost of accuracy.
- **`max_tokens`** — the cap on how long a reply can be, as discussed above.

### `config.py` — the settings dial

```python
TEMPERATURE = 0.0
MAX_NEW_TOKENS = 256
QWEN_SMALL_MODEL_ID = "qwen2.5:7b"
QWEN_LARGE_MODEL_ID = "qwen2.5:14b"
```

This file exists purely so all the "knobs" live in one obvious place. If you wanted to try a different model later, or make replies longer, you'd change exactly one number here instead of hunting through every file.

### `model.py` — the heart of the app

This is the most important file, so let's go slowly.

**Step 1 — Turning on the two models:**

```python
qwen_small_llm = initialize_model(QWEN_SMALL_MODEL_ID)
qwen_large_llm = initialize_model(QWEN_LARGE_MODEL_ID)
```

This creates two "ready to use" model objects — one for the 7-billion-parameter Qwen, one for the 14-billion-parameter Qwen — using the translator class from `ollama_llm.py`.

**Step 2 — Prompt templates (the "form letter" trick):**

```python
qwen_plain_template = PromptTemplate(
    template=(
        "<|im_start|>system\n{system_prompt}<|im_end|>\n"
        "<|im_start|>user\n{user_prompt}<|im_end|>\n"
        "<|im_start|>assistant\n"
    ),
    input_variables=["system_prompt", "user_prompt"],
)
```

Think of a **prompt template** exactly like a mail-merge form letter: "Dear `{name}`, your appointment is on `{date}}`." You write the fixed wrapper text once, and just plug in the changing parts (`name`, `date`) every time.

Here, the fixed wrapper is a set of **special tokens** that Qwen was specifically trained to recognize as structural markers — not visible punctuation you'd normally type, but literal signal strings the model was taught during training to interpret as "this is where the system instructions start," "this is where the user's message starts," and so on:

- `<|im_start|>system ... <|im_end|>` — "Here's the AI's role/personality/instructions" (e.g., "You are a helpful customer support assistant").
- `<|im_start|>user ... <|im_end|>` — "Here's what the actual human typed."
- `<|im_start|>assistant` — "Now it's your turn to reply" (this is left open/unfinished on purpose — the model's job is to complete it).

**Why does this matter?** Every model family invented its own version of these markers during training — Llama uses `<|start_header_id|>`, Mistral uses `[INST]`, Granite uses `<|system|>`, Qwen uses `<|im_start|>`. If you don't wrap your text in the *exact* markers a specific model was trained on, the model gets confused about what's an instruction versus what's the actual question — you saw this exact problem play out in the reading, where switching to Llama without the right markers gave a rambling, off-topic answer instead of a clean one.

There are **two** templates in this file:

- `qwen_template` — includes an extra `{format_prompt}` slot, used when we want the AI's answer back as neat structured data (see Part 6).
- `qwen_plain_template` — the simpler version, used by the chat website, where we just want normal conversational text back.

**Step 3 — The chains (the assembly line from Part 4):**

```python
def get_plain_ai_response(model, template, system_prompt, user_prompt):
    chain = template | model
    return chain.invoke({"system_prompt": system_prompt, "user_prompt": user_prompt})
```

`chain.invoke({...})` is the button that actually runs the assembly line: fill in the template with the real system prompt and user message, hand the result to the model, and return whatever text comes back.

**Step 4 — The friendly wrapper functions:**

```python
def qwen_small_plain_response(system_prompt, user_prompt):
    return get_plain_ai_response(qwen_small_llm, qwen_plain_template, system_prompt, user_prompt)
```

These exist just so the rest of the app (specifically `app.py`) doesn't need to know or care about templates and chains at all — it just calls `qwen_small_plain_response("be helpful", "what's the weather")` and gets text back, full stop. This is a very common programming habit called **abstraction**: hide the messy details behind a simple, clearly-named function so other code doesn't need to understand the internals.

### `app.py` — the actual website

```python
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
```

This says: "When someone's browser asks for the homepage (`/`), send them the `index.html` page." `render_template` is Flask's way of reading that HTML file and sending it back as the response.

```python
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_message = data.get("message")
    model = data.get("model")
    ...
    text = response_func(CHAT_SYSTEM_PROMPT, user_message)
    return jsonify({"response": text, "duration": time.time() - start_time})
```

This is the "behind the scenes" endpoint. When you type a message and hit send in the browser, the webpage doesn't reload — instead, JavaScript quietly sends your message to this `/generate` address in the background, gets back a JSON reply (structured data, not a full webpage), and updates the chat window with it. This "ask the server for just data, not a whole new page" pattern is how basically every modern chat app, including this one, works without ever refreshing.

- `request.json` — reads the data the browser sent (your message + which model you picked).
- `MODEL_RESPONSE_FUNCS` — a dictionary (a lookup table) mapping `"small"` → the small model's function, `"large"` → the big model's function, so the code can pick the right one based on what you clicked in the dropdown.
- The `try/except` block means: "try to get an AI reply; if literally anything goes wrong (Ollama isn't running, model errors out, etc.), don't crash the whole website — just send back a polite error message instead."
- `time.time()` before and after is just a stopwatch — subtracting start from end tells you how many seconds the AI took to reply, which gets shown to you as `duration`.

### `templates/index.html` — the webpage's skeleton

This is standard HTML — the structural bones of the page (a header, a chat area, a text box, a send button, a dropdown to pick the model). It has almost no "smarts" of its own; it just says what elements exist and gives them ID names (like `id="messageInput"`) so the JavaScript file can find and control them.

One thing worth calling out: the model dropdown here has

```html
<option value="small">Qwen2.5 7B (local Ollama)</option>
<option value="large">Qwen2.5 14B (local Ollama)</option>
```

Whatever you pick sends the string `"small"` or `"large"` to `/generate`, which is exactly what `app.py`'s `MODEL_RESPONSE_FUNCS` dictionary is expecting as its lookup key. This is a good example of a **contract** between frontend and backend: both sides have to agree on the exact same words, or things silently break.

### `static/script.js` and `static/styles.css` — behavior and appearance

- `styles.css` makes the page look like an actual chat app (colors, spacing, message bubbles, fonts) instead of plain unstyled text.
- `script.js` is what makes the page *interactive*: it listens for you pressing Enter or clicking Send, grabs your typed text and chosen model, sends that background request to `/generate` mentioned above, shows a "AI is thinking..." animation while waiting, and then displays the reply once it arrives.

These two files were downloaded as-is from a public GitHub Gist the lab links to — nobody in this project wrote them from scratch, and that's completely normal in real software: reusing solid, already-written frontend code so you can focus your own effort on the AI logic, not on reinventing chat-bubble CSS.

---

## Part 6: The JSON Part — Making the AI Answer Like a Form, Not an Essay

Separately from the plain chat feature, this lab also covers something called **structured output** — teaching the AI to answer in a very specific, predictable data shape instead of free-form prose. This is used in `llm_test.py`, not the chat website.

### Why would you want this?

If your AI just replies with a paragraph of English, a computer program can't easily *do* anything with that reply automatically — a human has to read it. But if the AI replies with something like:

```json
{"summary": "customer double-charged", "sentiment": 20, "category": "billing", "action": "issue a refund"}
```

...now a program can automatically file this under "billing issues," flag it as urgent because sentiment is low, and route it to the right team — all without a human reading raw text first. That's the entire point of structured output: **turning a chatty AI reply into clean data your other software can act on.**

### How it's built, step by step

**1. Define the shape you want (`Pydantic`):**

```python
class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the user's message")
    sentiment: int = Field(description="Sentiment score from 0 (negative) to 100 (positive)")
    category: str = Field(description="Category of the inquiry (e.g., billing, technical, general)")
    action: str = Field(description="Recommended action for the support rep")
```

`Pydantic` is a library for describing exactly what fields a piece of data should have, and what type each one should be (text, a number, etc). This class is basically a blueprint/checklist: "a valid answer MUST have a `summary` (text), a `sentiment` (a number), a `category` (text), and an `action` (text) — nothing missing, nothing extra."

**2. Turn that blueprint into instructions the AI can read:**

```python
json_parser = JsonOutputParser(pydantic_object=AIResponse)
...
json_parser.get_format_instructions()
```

`get_format_instructions()` automatically writes out a plain-English/JSON explanation of the blueprint above (something like "respond with a JSON object containing these exact fields...") and that explanation gets inserted into the prompt sent to the AI — that's what the `{format_prompt}` slot in `qwen_template` is for. In other words: **we're literally telling the AI, in its own instructions, exactly what shape to answer in.**

**3. Validate what actually comes back:**

```python
chain = template | model | json_parser
```

Even with good instructions, an AI can still occasionally reply with slightly broken JSON, or skip a field. The `json_parser` step at the end of the chain checks the AI's raw text reply against the blueprint, and:

- If it matches → hands back a clean Python dictionary you can use immediately.
- If it doesn't match → raises an error, so your code can catch that and handle it gracefully instead of silently trusting broken data.

This whole three-step pattern — **describe the shape → tell the AI the shape → verify the AI's answer against the shape** — is the standard, reusable way of getting reliable structured data out of any AI model, no matter which one you use.

---

## Part 7: Why the Browser Said "403 Access Denied" on Port 5000

This one isn't really about AI or LangChain at all — it's a classic Mac quirk that trips people up constantly.

Every website, including one running on your own laptop, is reached at an **address + a port number** — think of the address as a building, and the port as a specific numbered door into that building. `http://127.0.0.1:5000` means "door number 5000 on this same computer."

The problem: **macOS itself already uses port 5000** for its own built-in "AirPlay Receiver" feature (the thing that lets you stream video/audio from your phone to your Mac). So when Flask also tried to open "door 5000," it collided with macOS's own service already sitting there, and the "403 Access Denied" you saw was effectively a wrong door — something answered the knock, but it wasn't your Flask app, and it refused you.

The fix was simple: tell Flask to use a *different*, unclaimed door instead — port `5050` — so there's no collision, and now `http://127.0.0.1:5050` reaches your Flask app cleanly, confirmed by both a direct terminal test (`curl`) and the server logs showing a real `200 OK` response.

This is a good example of a bug that has **nothing to do with your code being wrong** — the code was correct the whole time — and everything to do with the environment around your code (in this case, an unrelated Mac feature squatting on the same numbered door your app wanted to use).

---

## Part 8: How It All Connects — The Full Journey of One Message

Let's trace exactly what happens, start to finish, when you type "What is the capital of Canada?" into the chat and hit send:

1. **Browser:** `script.js` notices you hit Enter/Send, reads your typed text and the selected model from the page, and sends a background request to `http://127.0.0.1:5050/generate` containing `{"message": "What is the capital of Canada?", "model": "small"}`.
2. **Flask (`app.py`):** The `/generate` route wakes up, pulls `message` and `model` out of that request, and — because `model` is `"small"` — looks up `qwen_small_plain_response` in `MODEL_RESPONSE_FUNCS`.
3. **`model.py`:** `qwen_small_plain_response` fills in the `qwen_plain_template` "form letter" with the system instructions ("You are an AI assistant helping with customer inquiries...") and your actual question, producing one big block of text with all the right `<|im_start|>`/`<|im_end|>` markers.
4. **`ollama_llm.py`:** That finished block of text gets handed to `OllamaLLM`, which sends it as a web request to Ollama running on your Mac at `localhost:11434`.
5. **Ollama (outside this whole codebase):** Actually runs the `qwen2.5:7b` model on your Mac's hardware, generates a reply token by token, and sends the finished text back.
6. **Back up through the chain:** That raw text flows back through `ollama_llm.py` → `model.py`'s chain → to `app.py`.
7. **Flask (`app.py`):** Wraps that text plus how long it took into `{"response": "...", "duration": 1.4}` and sends it back to the browser as JSON.
8. **Browser:** `script.js` receives that JSON, stops the "AI is thinking..." animation, and displays the reply as a new chat bubble on the page.

Every file in this project exists to handle exactly one link in that eight-step chain — that's the whole architecture, end to end.

---

## Why This Matters

This lab is really teaching one transferable skill disguised as a Flask tutorial: **how to wrap any AI model in a real, usable application**, safely and predictably. The specific model (Qwen vs. Llama vs. GPT), the specific hosting (your laptop vs. IBM's cloud), and the specific framework (Flask vs. something else) are all interchangeable details. What stays the same in *any* real AI product you'll ever build or work on is this exact shape:

- Something has to turn a user's raw input into a properly-formatted prompt (the template).
- Something has to send that prompt to a model and get text back (the chain/model wrapper).
- Sometimes you need that reply to come back as clean, structured data instead of prose (the JSON parser + schema).
- Something has to expose all of this to actual humans through a web interface (Flask, HTML, JS).
- And underneath all of it, small environment issues (a busy port, a missing dependency, a wrong prompt format for a specific model) are just as common a source of bugs as anything in your own logic — debugging them is a completely normal, expected part of the job, not a sign something is fundamentally broken.
