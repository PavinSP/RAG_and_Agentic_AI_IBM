# Glossary

Recurring terms from the certificate, each defined as the course itself uses it, with links to the notes that discuss it most substantively. Terms are listed once they appear in 2+ notes.

## A

**Agent** — A system where a language model **determines and sequences the actions** to take, rather than following a fixed script. The model generates text to *guide* actions but does not execute them itself; the agent integrates with tools (search engines, databases, APIs) to actually carry them out. Underlies the ReAct Thought → Action → Observation loop.
→ [Chains and Agents (video note)](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/Video Notes/02_LangChain Chains and Agents for Building Applications.md>) · [LangChain Chains and Agents](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/01_LangChain Core Components and Advanced Features/03_LangChain Chains and Agents for Building Applications.md>)

## C

**Chain** — A sequence of calls where the output of one step becomes the input to the next. Built the old way with `LLMChain`/`SequentialChain` (matching output keys to input variables by hand), or the modern way with LCEL's pipe operator.
→ [Chains and Agents (video note)](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/Video Notes/02_LangChain Chains and Agents for Building Applications.md>)

**Chain-of-thought (CoT) prompting** — Asking the model to work through a problem **step by step** rather than jumping to an answer. Effective for multi-step reasoning, and it makes the model's reasoning inspectable.
→ [Advanced Methods of Prompt Engineering (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/08_Advanced Methods of Prompt Engineering.md>)

**Chat model** — A model wrapper designed for conversation: it takes a *list of role-tagged messages* rather than one text blob, and returns a message object. Contrast with a plain **language model**, which is text in → text out.
→ [LangChain Core Concepts (video note)](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/Video Notes/01_LangChain Core Concepts.md>)

**Context window** — The maximum number of tokens a model can consider at once. The hard limit that forces chunking, retrieval, and memory-summarization strategies.
→ [What are Generative AI Models (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/04_What are Generative AI Models.md>)

## D

**Discriminative AI** — Learns to *distinguish between classes* by finding a decision boundary (e.g. spam vs. not-spam). Cannot generate new content. The contrast case for generative AI.
→ [Introduction to Generative AI (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/03_Introduction to Generative AI.md>)

## F

**Few-shot prompting** — Giving the model **several examples** of the task before asking it to perform on new input, so it generalizes the pattern and the output format. Formalized in LangChain as `FewShotPromptTemplate`.
→ [Advanced Methods of Prompt Engineering (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/08_Advanced Methods of Prompt Engineering.md>)

**Fine-tuning** — Adapting a model by **updating its weights** on domain-specific data, baking the knowledge and behavior into the model itself. Needs labeled data and compute; contrast with **RAG**, which supplies knowledge at request time instead.
→ [From Idea to AI (video note)](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/Video Notes/02_From Idea to AI - Building Applications with Generative AI.md>) · [What are Generative AI Models (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/04_What are Generative AI Models.md>)

**Foundation model** — A single model, pre-trained unsupervised on an enormous amount of unstructured data, that can be **transferred to many different tasks** — replacing the older paradigm of one narrowly-trained model per task. LLMs are the language-domain case; vision, code, chemistry, and climate models also exist.
→ [What are Generative AI Models (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/04_What are Generative AI Models.md>)

## I

**In-context learning** — Teaching a model a new task purely through **examples placed in the prompt**, at inference time, with no retraining. Bounded by what fits in the context window.
→ [Introduction to In-Context Learning (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/06_Introduction to In-Context Learning.md>)

## J

**Jinja** — The template language Flask uses to render dynamic HTML pages. Ships with **MarkupSafe**, which escapes untrusted input to prevent injection attacks — relevant when rendering model-generated text.
→ [Introduction to Flask (video note)](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/Video Notes/03_Introduction to Flask.md>)

## L

**LCEL (LangChain Expression Language)** — The modern way to compose LangChain chains, using the **pipe operator** (`template | model | parser`). Syntactic sugar over `RunnableSequence`, with automatic type coercion (a dict becomes `RunnableParallel`, a function becomes `RunnableLambda`). Recommended over the older `LLMChain` approach.
→ [LCEL Chaining Method (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/09_LangChain LCEL Chaining Method.md>)

## M

**Memory** — Conversation history that a chain **reads from before** running its logic and **writes back to after**. Nothing is stored inside the model — the framework re-injects prior turns into each new prompt, which is why remembered context consumes context window on every call.
→ [Chains and Agents (video note)](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/Video Notes/02_LangChain Chains and Agents for Building Applications.md>)

**MLOps** — Machine learning operations: getting models into production and keeping them healthy. Covers containers and orchestrators (Kubernetes), production runtimes (vLLM), scaling, benchmarking, monitoring, and exception handling. The DevOps analogue for models.
→ [From Idea to AI (video note)](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/Video Notes/02_From Idea to AI - Building Applications with Generative AI.md>)

**Multi-model approach** — Keeping a *variety* of models available and picking the right one per use case, rather than standardizing on one. Framed in the course via the garden analogy: "you can't live on carrots alone."
→ [Choose the Right AI Model (video note)](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/Video Notes/01_Choose the Right AI Model for Your Use Case.md>)

## N

**NLP / NLU / NLG** — Natural language **processing** is the translation layer between unstructured human language and structured machine-readable data. Unstructured → structured is **NLU** (understanding); structured → unstructured is **NLG** (generation). The classic NLP pipeline is a "bag of tools": tokenization, stemming, lemmatization, part-of-speech tagging, named entity recognition.
→ [What is NLP (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/05_What is NLP.md>)

## O

**Output parser** — Transforms an LLM's raw text output into a structured, usable format — JSON, CSV, XML, a Pandas DataFrame. `JsonOutputParser` combined with a Pydantic schema also *validates* the result, and `get_format_instructions()` injects the required shape into the prompt.
→ [LangChain Core Concepts (video note)](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/Video Notes/01_LangChain Core Concepts.md>) · [Choosing the Right Model lab](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/01_Application Development Workflow with Generative AI/07_Hands On Lab: Choosing the Right Model for Your Application/07_Choosing the Right Model for Your Application.md>)

## P

**Prompt** — The input given to an LLM to guide it toward a task. Has four structural elements: **instructions**, **context**, **input data**, and an **output indicator** (a marker showing where the answer goes). In model selection, the prompt doubles as the written *specification* candidate models are evaluated against.
→ [Introduction to In-Context Learning (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/06_Introduction to In-Context Learning.md>)

**Prompt engineering** — Designing and refining prompts to get relevant, accurate output. Not just *what* you ask but *how* — and it substitutes for fine-tuning in low-labeled-data situations.
→ [Introduction to In-Context Learning (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/06_Introduction to In-Context Learning.md>) · [Advanced Methods (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/08_Advanced Methods of Prompt Engineering.md>)

**Prompt template** — A reusable prompt "form letter" with `{placeholder}` slots filled at runtime. Variants include `PromptTemplate` (single string), `ChatPromptTemplate` (message lists), `MessagesPlaceholder`, and `FewShotPromptTemplate`.
→ [LangChain Core Concepts (video note)](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/Video Notes/01_LangChain Core Concepts.md>)

## R

**RAG (Retrieval Augmented Generation)** — Supplementing a pre-trained model with **relevant external data retrieved at request time**, so answers are grounded in vetted documents rather than only in what the model memorized during training. The main mitigation for hallucination and for un-auditable training data.
→ [From Idea to AI (video note)](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/Video Notes/02_From Idea to AI - Building Applications with Generative AI.md>) · [Understanding Coding (Module 2)](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/01_LangChain Core Components and Advanced Features/05c_Understanding Coding.md>)

**Runnable** — LangChain's common interface for anything that can sit in a chain. `RunnableSequence` runs components in order (output → next input); `RunnableParallel` runs several concurrently on the *same* input; `RunnableLambda` wraps a plain function.
→ [LCEL Chaining Method (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/09_LangChain LCEL Chaining Method.md>)

## S

**Self-consistency** — Generating **multiple independent answers** to the same question and taking the most consistent one. Catches cases where a single chain-of-thought run reasons plausibly to a wrong answer, at the cost of several full generations.
→ [Advanced Methods of Prompt Engineering (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/08_Advanced Methods of Prompt Engineering.md>)

**Special tokens** — Literal marker strings a model family was trained to read as structure, not content: Llama's `<|start_header_id|>`/`<|eot_id|>`, Mistral's `[INST]`, Granite's `<|system|>`, Qwen's `<|im_start|>`. Using the wrong family's markers produces rambling, off-target answers. They are the on-the-wire encoding of chat message **roles**.
→ [Choosing the Right Model lab](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/01_Application Development Workflow with Generative AI/07_Hands On Lab: Choosing the Right Model for Your Application/07_Choosing the Right Model for Your Application.md>)

**SLM (Small Language Model)** — A smaller, task-specialized model. Generally **faster with lower latency** and cheaper than a large model, and often good enough — hence the "start large to prove it's possible, then scale down" selection strategy.
→ [From Idea to AI (video note)](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/Video Notes/02_From Idea to AI - Building Applications with Generative AI.md>)

## T

**Temperature** — Controls randomness in token selection. `0` is deterministic and repeatable (always the most probable next token); higher values allow more creative, varied output. Paired with the decoding method (`greedy` vs. `sampling`).
→ [Choosing the Right Model lab](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/01_Application Development Workflow with Generative AI/07_Hands On Lab: Choosing the Right Model for Your Application/07_Choosing the Right Model for Your Application.md>)

**Token** — The unit of text a model actually processes: sometimes a whole word, sometimes a word fragment or punctuation mark. Context windows are measured in tokens, API pricing is charged per token, and `max_new_tokens` caps response length.
→ [What are Generative AI Models (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/04_What are Generative AI Models.md>) · [What is NLP (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/05_What is NLP.md>)

## W

**WSGI (Web Server Gateway Interface)** — The standard Python interface between web applications and servers, implemented in Flask by **Werkzeug**. `app = Flask(__name__)` creates the WSGI application object.
→ [Introduction to Flask (video note)](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/Video Notes/03_Introduction to Flask.md>)

## Z

**Zero-shot prompting** — Asking a model to perform a task with **no examples at all**, relying entirely on its pre-training. Cheapest in tokens, least reliable for constraining output format.
→ [Advanced Methods of Prompt Engineering (video note)](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/08_Advanced Methods of Prompt Engineering.md>)
