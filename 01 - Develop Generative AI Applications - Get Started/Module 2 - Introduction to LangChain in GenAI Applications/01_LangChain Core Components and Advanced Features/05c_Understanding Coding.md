# Understanding the Code: A Full Walkthrough of the "Build Smarter AI Apps" Lab

This note explains every LangChain concept and every piece of code in `05b_Build Smarter AI Apps Empower LLMs with LangChain (Local Ollama).ipynb`. It assumes you've already read [07c_Understanding Coding.md](<../../Module 1 - Foundations of Generative AI and Prompt Engineering/03_Working with Prompt Engineering and Prompt Templates/07c_Understanding Coding.md>) from Module 1 — that note covers general Python syntax (triple-quoted strings, f-strings, dictionaries, `**kwargs`, the pipe operator, `PromptTemplate`, `RunnableLambda`, `StrOutputParser`) and this note builds on top of it without repeating those basics. It assumes general programming literacy but not prior LangChain/RAG/agent knowledge.

This lab is a big step up from the first one — it moves from "send a single prompt, get a single response" into the concepts that make LangChain actually useful for real applications: giving a model access to documents it wasn't trained on (retrieval-augmented generation, or RAG), giving it memory across a conversation, and giving it the ability to take actions (agents and tools).

Read this top to bottom in the order the notebook itself runs — each section builds on the last.

## Table of Contents

**Part 1 — The Code**

1. Model vs. Chat Model — why the distinction matters
2. Chat messages — `SystemMessage`, `HumanMessage`, `AIMessage`
3. Prompt templates, revisited — chat templates and `MessagesPlaceholder`
4. Output parsers — JSON and comma-separated list
5. Documents — the `Document` object
6. Document loaders — PDF and web
7. Text splitters — why and how documents get chunked
8. Embeddings — turning text into vectors
9. Vector stores — Chroma
10. Retrievers — vector-store-backed and parent-document
11. RetrievalQA — putting it all together into a QA bot
12. Memory — `ChatMessageHistory` and `ConversationBufferMemory`
13. Chains, revisited — `LLMChain`/`SequentialChain` vs. LCEL
14. Tools — giving the model the ability to act
15. Agents — the ReAct reasoning loop

**Part 2 — The Theory Behind It All**

16. What is actually happening when you call `.invoke()`?
17. Why embeddings work: geometry, not understanding
18. Why chunking is a trade-off, not a solved problem
19. Why RAG works — and where it breaks
20. Why "memory" is really just a context-window budgeting problem
21. Why agents can "reason" — and the real limits of that reasoning
22. Putting the theory back into the lab

23. Why This Matters

---

## Part 1 — The Code

## 1. Model vs. Chat Model — why the distinction matters

The original IBM version of this lab draws a distinction between a raw **Model** (`ModelInference`, which takes a plain string and returns a plain string) and a **Chat Model** (`WatsonxLLM`-wrapped, which understands roles like "system," "human," and "AI"). In the local Ollama variant, this distinction is flattened — `OllamaLLM` (defined once, early in the notebook) plays both roles, because Ollama's own API is a single text-completion endpoint underneath either way.

The conceptual point still matters even though the code is unified: a **chat model** isn't a different kind of AI, it's a raw model wrapped with conventions for structuring a conversation as a sequence of role-tagged messages, so the model can tell the difference between "instructions I was given" (system), "what the user said" (human), and "what I said previously" (AI). This is what Section 2 covers.

## 2. Chat messages — `SystemMessage`, `HumanMessage`, `AIMessage`

```python
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

msg = llama_llm.invoke(
    [
        SystemMessage(content="You are a supportive AI bot that suggests fitness activities."),
        HumanMessage(content="I like high-intensity workouts, what should I try?"),
        AIMessage(content="You should try a CrossFit class"),
        HumanMessage(content="How often should I attend?")
    ]
)
```

Instead of invoking the model with a single string, you invoke it with a **list of message objects**. Each one is tagged with a role:

- `SystemMessage` — instructions that set the model's behavior, usually the first message in the list. It's not something the "user" said; it's a steering instruction from the application itself.
- `HumanMessage` — something the user actually typed.
- `AIMessage` — something the model said previously, in an earlier turn.

Why pass previous `AIMessage`s back in, rather than just the new question? Because the model itself has **no memory between calls** — every `.invoke()` is a fresh, stateless request. If you want the model to know that it already told the user "try CrossFit," you have to re-send that fact as part of the input every single time. This is the single most important idea underlying everything in this lab that looks like "the AI remembers" — it doesn't, really; the application is reconstructing the appearance of memory by resending history. Section 12 (Memory) automates exactly this bookkeeping so you don't have to build the message list by hand every turn.

## 3. Prompt templates, revisited — chat templates and `MessagesPlaceholder`

`07c` already covered `PromptTemplate` for plain strings. This lab introduces the chat-message equivalent:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("user", "Tell me a joke about {topic}")
])
```

Instead of one template string with `{placeholders}`, `ChatPromptTemplate.from_messages` takes a **list of (role, template-string) tuples** — each tuple becomes one message in the final chat, and each one can have its own placeholders.

```python
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("msgs")
])

input_ = {"msgs": [HumanMessage(content="What is the day after Tuesday?")]}
```

`MessagesPlaceholder("msgs")` is a special slot that doesn't take a plain string — it takes a **list of message objects** supplied at invocation time, and splices that whole list into the template at that position. This is the mechanism that makes it possible to inject an entire, variable-length conversation history into a template — you can't do that with an ordinary `{placeholder}`, because a placeholder holds one string, not a list of typed message objects.

## 4. Output parsers — JSON and comma-separated list

An LLM only ever produces text. If your application needs *structured* data (a Python dict, a list), something has to parse that text back into a real data structure — that's an output parser's job.

### JSON parser

```python
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

output_parser = JsonOutputParser(pydantic_object=Joke)
format_instructions = output_parser.get_format_instructions()
```

`Joke` is a **Pydantic model** — a class that declares the exact shape of data you want (a `setup` field and a `punchline` field, both strings). You don't fill this class in with real data yourself; instead, you hand it to `JsonOutputParser`, and `.get_format_instructions()` generates a chunk of text describing that schema in a way an LLM can read and follow (something like "respond with JSON matching this structure: {...}"). You then splice those instructions into your prompt:

```python
prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": format_instructions},
)
chain = prompt | llama_llm | output_parser
chain.invoke({"query": "Tell me a joke."})
```

Notice `partial_variables` vs. `input_variables`: `input_variables` are filled in fresh every time you call `.invoke()` (here, `query`); `partial_variables` are baked into the template once, at creation time, and don't change between calls (here, `format_instructions` — the schema doesn't change from one joke to the next, only the query does).

The chain itself is the same three-stage pipe pattern from `07c`: format the prompt → send to the model → parse the output. The only difference from the earlier lab is which parser sits in the third slot. `JsonOutputParser` specifically expects the model's raw text output to *contain* valid JSON somewhere in it, and it extracts and parses that into an actual Python dict — so `chain.invoke(...)` returns `{'setup': '...', 'punchline': '...'}`, a real dict you can index with `result['setup']`, not a string that merely looks like one.

### Comma-separated list parser

```python
from langchain.output_parsers import CommaSeparatedListOutputParser

output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()
```

Same pattern, simpler target format: instead of a JSON schema, the format instructions just tell the model "respond with a comma-separated list," and the parser splits the model's response on commas into a Python list of strings.

## 5. Documents — the `Document` object

```python
from langchain_core.documents import Document

Document(
    page_content="""Python is an interpreted high-level general-purpose programming language...""",
    metadata={
        'my_document_id': 234234,
        'my_document_source': "About Python",
        'my_document_create_time': 1680013019
    }
)
```

A `Document` is LangChain's universal container for "a piece of text plus information about that text." `page_content` is the actual text. `metadata` is an open-ended dictionary for anything you want to track alongside it — where it came from, an ID, a timestamp, a page number. Nothing in LangChain requires specific metadata keys; it's just a bag of extra facts that travels with the text through the rest of the pipeline (loaders attach it, splitters preserve it across chunks, retrievers can return it alongside the content).

This matters because everything downstream in this lab — loaders, splitters, embeddings, vector stores, retrievers — operates on lists of `Document` objects, not raw strings. Once you understand `Document` is just `(text, metadata)`, the rest of the RAG pipeline is really just "different tools that consume and produce lists of this one simple container type."

## 6. Document loaders — PDF and web

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("https://arxiv.org/pdf/2403.05568")
document = loader.load()
document[2]  # page 2 as a Document object
```

A loader's job is narrow and mechanical: take a source (a URL, a file path, a database) and produce a `list[Document]`. `PyPDFLoader` specifically downloads a PDF and produces **one `Document` per page** — `document[2]` is the third page (index 2), as a `Document` whose `page_content` is that page's extracted text and whose `metadata` includes which page number it came from.

```python
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://python.langchain.com/v0.2/docs/introduction/")
web_data = loader.load()
```

`WebBaseLoader` does the same job for a web page: it fetches the HTML, strips it down to readable text, and returns it as `Document` objects (usually one per page, unlike the PDF loader's one-per-page-of-the-PDF granularity). Both loaders exist so that the *rest* of your pipeline (splitting, embedding, retrieval) never needs to know or care whether the original content came from a PDF, a website, a database, or anything else — everything downstream just sees `Document` objects.

> **Note (local variant):** the original lab's PDF URL (hosted on IBM's Skills Network S3 bucket) is dead outside their lab environment — confirmed with a direct HTTP request while building this notebook (a 404). The local variant substitutes the real paper the lab describes, fetched live from arXiv, flagged inline in the notebook rather than silently changed.

## 7. Text splitters — why and how documents get chunked

A whole PDF or web page is usually too large to be useful directly — both because a model has a limited context window, and because for retrieval (Section 10) you want to compare a *specific relevant passage* against a query, not an entire document at once. Text splitters break large `Document`s into smaller ones.

```python
from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20, separator="\n")
chunks = text_splitter.split_documents(document)
```

- `chunk_size=200` — aim for roughly 200 characters per chunk.
- `chunk_overlap=20` — each chunk shares its last 20 characters with the start of the next chunk. This overlap exists so that a sentence or idea that happens to fall right at a chunk boundary isn't cut in a way that destroys its meaning in *both* resulting chunks — the overlap gives each chunk a little of the neighboring context.
- `separator="\n"` — when possible, prefer splitting at newlines rather than mid-word or mid-sentence, so chunks tend to break at natural boundaries.

`CharacterTextSplitter` is the simplest splitter: it just counts characters and cuts at the nearest allowed separator. The lab's Exercise 3 also introduces `RecursiveCharacterTextSplitter`, which is smarter — it tries a *list* of separators in priority order (paragraph breaks, then sentence breaks, then word breaks, then raw characters) and only falls back to a cruder split when a nicer one isn't available nearby. This tends to produce chunks that respect the document's natural structure better than the plain character splitter.

Critically, `split_documents()` **preserves metadata** — every chunk produced from a given source document still carries that document's original metadata (like which PDF page it came from), even though the chunk itself is now a small fragment of that page's text.

## 8. Embeddings — turning text into vectors

```python
from langchain_core.embeddings import Embeddings  # abstract base class

watsonx_embedding = WatsonxEmbeddings(...)  # original lab
# vs., in the local variant:
embedding_model = OllamaEmbeddings(model="nomic-embed-text")

texts = [text.page_content for text in chunks]
embedding_result = watsonx_embedding.embed_documents(texts)
embedding_result[0][:5]  # first 5 numbers of the first chunk's vector
```

An embedding model converts a piece of text into a **vector** — a long list of numbers (hundreds to thousands of dimensions) that represents the text's *meaning* in a mathematical space. The specific numbers are meaningless on their own; what matters is that texts with *similar meaning* get mapped to vectors that are mathematically *close together* in that space (by some distance measure), while texts about unrelated topics end up far apart.

This is the entire trick that makes semantic search possible: instead of matching keywords, you can measure the distance between the embedding of a search query and the embeddings of your document chunks, and the closest ones are the most semantically relevant — even if they don't share a single literal word with the query.

`embed_documents()` embeds a whole list of texts at once (used for building your searchable corpus). `embed_query()` (used later, inside a retriever) embeds a single piece of text — typically the user's search query — the same way, so the two can be compared apples-to-apples in that same vector space.

## 9. Vector stores — Chroma

```python
from langchain.vectorstores import Chroma

docsearch = Chroma.from_documents(chunks, watsonx_embedding)

query = "Langchain"
docs = docsearch.similarity_search(query)
print(docs[0].page_content)
```

A vector store is a database purpose-built for the "store lots of vectors, then quickly find the closest ones to a new vector" operation. `Chroma.from_documents(chunks, embedding_model)` does two things in one call: it runs every chunk's text through the embedding model, *and* it stores the resulting `(vector, original Document)` pairs so they can be searched later.

`.similarity_search(query)` is the read side: it takes your query string, embeds it (using the same embedding model, automatically), and returns the `Document`s whose stored vectors are closest to the query's vector — i.e., the chunks that are most semantically related to what you asked, regardless of exact wording.

## 10. Retrievers — vector-store-backed and parent-document

```python
retriever = docsearch.as_retriever()
docs = retriever.invoke("Langchain")
```

A **retriever** is a thin, standardized interface: "give me a query string, get back a list of relevant `Document`s." `docsearch.as_retriever()` wraps the vector store so it exposes this generic interface — the point being that *many* different underlying mechanisms (not just vector similarity) can implement the same retriever interface, so the rest of your application (like `RetrievalQA` in Section 11) can work with any of them interchangeably without caring which one is plugged in underneath.

### Parent document retriever

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore

parent_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
child_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=20)

vectorstore = Chroma(collection_name="split_parents", embedding_function=watsonx_embedding)
store = InMemoryStore()

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)
retriever.add_documents(document)
```

This solves a genuine tension in RAG design: **small chunks embed more precisely** (a short, focused passage's vector accurately represents its narrow meaning), but **small chunks lose surrounding context** when you hand them to the LLM to answer a question (a 400-character fragment might not contain enough of the surrounding explanation to be useful on its own).

`ParentDocumentRetriever` gets both: it splits each document twice — into large "parent" chunks (2000 characters, stored as plain text in `InMemoryStore`, never embedded) and small "child" chunks (400 characters, embedded and stored in the vector store, each one tagged with which parent it came from). When you search, the *similarity search happens on the small, precise child chunks* — but the retriever then looks up and returns the *larger parent chunk* that child came from, giving the LLM more surrounding context to work with than the tiny fragment alone would have provided.

## 11. RetrievalQA — putting it all together into a QA bot

```python
from langchain.chains import RetrievalQA

qa = RetrievalQA.from_chain_type(
    llm=llama_llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(),
    return_source_documents=False
)
qa.invoke("what is this paper discussing?")
```

`RetrievalQA` is a pre-built chain that wires together everything from Sections 6–10 into one call: given a question, it (1) uses the retriever to find relevant chunks, (2) combines them with the question into a prompt, (3) sends that to the LLM, and (4) returns the answer. This *is* what "RAG" (Retrieval-Augmented Generation) means in practice — the model's answer is "augmented" by real document content that was "retrieved" moments before, rather than relying purely on what the model happened to memorize during training.

`chain_type="stuff"` names the strategy for combining retrieved chunks into the prompt: "stuff" means the simplest approach — just concatenate all the retrieved chunks together and stuff them into the prompt alongside the question. (Other chain types exist for when there are too many chunks to fit in one prompt at once, but "stuff" is the default starting point and what's used throughout this lab.)

## 12. Memory — `ChatMessageHistory` and `ConversationBufferMemory`

Recall from Section 2: the model has no memory of its own; the application has to resend prior turns as part of each new call. This section automates that.

```python
from langchain.memory import ChatMessageHistory

history = ChatMessageHistory()
history.add_ai_message("hi!")
history.add_user_message("what is the capital of France?")

ai_response = chat.invoke(history.messages)
history.add_ai_message(ai_response)
```

`ChatMessageHistory` is just a list of messages with two convenience methods for appending to it (`add_ai_message`, `add_user_message`). `.messages` gives you back that list in the `[SystemMessage, HumanMessage, AIMessage, ...]` form the chat model expects (Section 2) — so instead of manually building that list by hand every time, you build it up incrementally as the conversation happens, one `.add_*_message()` call per turn.

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

conversation = ConversationChain(
    llm=llama_llm,
    verbose=True,
    memory=ConversationBufferMemory()
)
conversation.invoke(input="Hello, I am a little cat. Who are you?")
conversation.invoke(input="Who am I?")
```

`ConversationChain` + `ConversationBufferMemory` is a higher-level convenience over `ChatMessageHistory`: you no longer manage the message list yourself at all. Every time you call `.invoke(input=...)`, the chain automatically (1) reads everything said so far from memory, (2) builds the full prompt including that history, (3) sends it to the model, (4) reads the response, and (5) writes both your new input and the model's response back into memory for next time. This is why, after telling it "I am a little cat," asking "Who am I?" a few turns later correctly gets "You said you are a little cat" — the memory object has been silently accumulating the whole exchange behind the scenes.

`verbose=True` is purely a debugging aid — it prints the *entire* prompt (including the full accumulated history) that actually gets sent to the model on each turn, so you can see exactly how large and how repetitive that prompt becomes as a conversation grows (this is also why buffer memory doesn't scale forever — eventually the accumulated history would exceed the model's context window, which is what alternatives like `ConversationSummaryMemory`, used in this notebook's Exercise 5, are for: instead of keeping the full verbatim history, it periodically asks the LLM to *summarize* the conversation so far, and carries forward a much shorter summary instead of the raw transcript).

## 13. Chains, revisited — `LLMChain`/`SequentialChain` vs. LCEL

`07c` already introduced the pipe-operator (`|`) LCEL pattern. This lab is where you see the *older*, pre-LCEL way of doing the same thing, side by side with the modern equivalent — useful because a lot of real-world LangChain code and tutorials still use the older style.

```python
from langchain.chains import LLMChain

prompt_template = PromptTemplate(template=template, input_variables=["location"])
location_chain = LLMChain(llm=llama_llm, prompt=prompt_template, output_key="meal")
location_chain.invoke(input={'location': 'China'})
```

`LLMChain` bundles a prompt template and a model into one object, same conceptual job as `prompt | llm` in LCEL. The notable difference is `output_key="meal"` — `LLMChain` (and `SequentialChain`, below) are built around named dictionary keys for their outputs, so that when you chain multiple `LLMChain`s together, each one's result gets stored under a specific name that the *next* chain in the sequence can refer to.

```python
from langchain.chains import SequentialChain

overall_chain = SequentialChain(
    chains=[location_chain, dish_chain, recipe_chain],
    input_variables=['location'],
    output_variables=['meal', 'recipe', 'time'],
    verbose=True
)
overall_chain.invoke(input={'location': 'China'})
```

`SequentialChain` runs a list of `LLMChain`s one after another, automatically threading each chain's named output into the next chain's expected input (matched by name — `location_chain` produces `meal`, and `dish_chain`'s prompt template expects a `{meal}` placeholder, so the wiring is implicit through matching key names). You have to explicitly declare, up front, which variables go in (`input_variables`) and which should be included in the final combined output (`output_variables`).

The **LCEL equivalent** of this same three-step pipeline:

```python
from langchain_core.runnables import RunnablePassthrough

overall_chain_lcel = (
    RunnablePassthrough.assign(meal=lambda x: location_chain_lcel.invoke(x))
    | RunnablePassthrough.assign(recipe=lambda x: dish_chain_lcel.invoke(x))
    | RunnablePassthrough.assign(time=lambda x: time_chain_lcel.invoke(x))
)
result = overall_chain_lcel.invoke({"location": "China"})
```

`RunnablePassthrough.assign(key=function)` takes whatever dictionary is flowing through the chain so far, runs `function` on it, and adds the result under `key` **without discarding the existing keys** — so after all three steps, `result` is a dictionary containing `location`, `meal`, `recipe`, *and* `time`, because each `.assign()` step only ever adds to the dictionary, never replaces it. This is the LCEL way of achieving the same "each step's output becomes available to the next step, and everything is visible at the end" behavior that `SequentialChain`'s `output_variables` list achieves through separate, explicit bookkeeping.

Functionally these two approaches produce the same result; LCEL is simply more composable (you can rearrange, insert, or test any single step independently) and doesn't require the somewhat rigid up-front declaration of every input/output variable name that `SequentialChain` does.

## 14. Tools — giving the model the ability to act

Everything up to this point — even RAG — is still fundamentally "the model reads text and generates text." A **tool** is how a LangChain application lets a model trigger real code execution, not just generate more words.

```python
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL

python_repl = PythonREPL()
python_calculator = Tool(
    name="Python Calculator",
    func=python_repl.run,
    description="Useful for when you need to perform calculations or execute Python code."
)
python_calculator.invoke("a = 3; b = 1; print(a+b)")
```

A `Tool` is just three things bundled together: a `name` (an identifier the model can refer to), a `func` (the actual Python function that gets called when the tool is used), and a `description` (plain-English text explaining what the tool does and when to use it). That `description` is not decoration — it's the *only* information the agent (Section 15) has to decide, on its own, whether this tool is relevant to a given question. A vague or missing description means the agent won't reliably pick the right tool.

```python
@tool
def search_weather(location: str):
    """Search for the current weather in the specified location."""
    return f"The weather in {location} is currently sunny and 72°F."
```

`@tool` is a decorator shortcut for the exact same thing: it turns an ordinary Python function into a usable `Tool` automatically, using the function's name as the tool name and its docstring as the description. Both styles (explicit `Tool(...)` and `@tool`) produce the same kind of object; which one you reach for is mostly a matter of whether you already have a function you're wrapping (use `@tool`) or you're wrapping something else's existing method, like `python_repl.run` (use `Tool(...)` directly).

A **toolkit** is nothing more elaborate than a plain Python list of `Tool` objects — `tools = [python_calculator, search_weather]` — grouped together because an agent typically needs access to *several* tools at once and picks whichever one fits the current question.

## 15. Agents — the ReAct reasoning loop

```python
from langchain.agents import create_react_agent, AgentExecutor

prompt_template = """You are an agent who has access to the following tools:
{tools}
The available tools are: {tool_names}
To use a tool, please use the following format:
```
Thought: I need to figure out what to do
Action: tool_name
Action Input: the input to the tool
```
...
"""
prompt = PromptTemplate.from_template(prompt_template)

agent = create_react_agent(llm=llama_llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

result = agent_executor.invoke({"input": "What is the square root of 245?"})
```

This is the payoff of everything in Section 14. **ReAct** ("Reasoning + Acting") is a specific prompting strategy — not a special model feature — where the prompt instructs the model to output its response in a very particular, structured text format: a `Thought` (its reasoning about what to do), then an `Action` (which tool to use) and `Action Input` (what to pass that tool), and to stop there rather than continuing to write more text.

The `AgentExecutor` is the piece of code that makes this loop actually *do* something, rather than just being text the model wrote:

1. It sends the question to the model with the ReAct prompt.
2. The model responds with a `Thought`/`Action`/`Action Input` block (and nothing more — it stops after `Action Input`).
3. `AgentExecutor` **parses** that text, finds the named tool in its `tools` list, and actually calls that tool's function with the given input — this is genuine Python code execution, not the model "pretending" to run something.
4. The tool's real return value gets fed back into the prompt as an `Observation`.
5. The model is called *again*, now seeing its own previous thought/action plus the real observation, and either takes another action or, once it has enough information, writes a `Final Answer` instead of another `Action` — at which point the loop stops and that final answer is returned.

This is why running an agent produces multiple model calls per question, not just one — each `Thought → Action → Observation` cycle is a separate round-trip to the LLM. `handle_parsing_errors=True` matters in practice because smaller local models (like the `qwen2.5:7b` used in this local variant) don't always format their `Thought`/`Action`/`Final Answer` output perfectly on the first try — this flag tells `AgentExecutor` to feed the model a corrective nudge and retry rather than crashing outright when its output doesn't parse cleanly, which is genuinely what happens a few times when running this lab's Exercise 7 locally.

---

## Part 2 — The Theory Behind It All

Part 1 explained *what the code does* and *how the LangChain pieces fit together*. This part steps back and explains *why any of it actually works* — the underlying mechanics that are true regardless of which library or vendor you use, because they're properties of how language models and vector math actually behave.

## 16. What is actually happening when you call `.invoke()`?

Every single `.invoke()` call anywhere in this lab — on `llama_llm`, on a chain, on an agent — ultimately bottoms out in the exact same operation: **the model is predicting the next token, one token at a time, based on everything that came before it.**

A "token" is roughly a word or word-fragment (not always a whole word — "unbelievable" might be three tokens: "un", "believ", "able"). The model has been trained on enormous amounts of text to get very good at one narrow skill: given a sequence of tokens so far, estimate the probability of every possible next token, then pick one (usually one of the more likely ones, with some randomness controlled by `temperature`), append it, and repeat. A whole paragraph of output is just this one-token-at-a-time process run over and over until the model produces a special "stop" token or hits your `max_tokens` limit.

This single fact explains several things that otherwise seem mysterious:

- **Why the model can't "revise" earlier words once written** — it never goes back and edits; it only ever appends. If it starts an answer badly, it's often stuck continuing from that bad start (this is part of why chain-of-thought prompting, from Module 1, helps: reasoning out loud step-by-step gives the model a chance to "correct course" in a later token, informed by its own earlier tokens, rather than committing to a wrong answer immediately).
- **Why `temperature` changes creativity vs. consistency** — at each step, temperature controls how "flat" or "peaked" the probability distribution over next-tokens is sampled from. Low temperature almost always picks the single most likely next token (consistent, deterministic-feeling output); high temperature gives real weight to less-likely-but-plausible tokens too (more variety, more surprises, occasionally less coherent).
- **Why everything in this lab — chat messages, retrieved document chunks, conversation memory — ultimately gets flattened into one long text prompt before the model ever sees it.** There is no special "memory channel" or "document channel" into the model. `SystemMessage`/`HumanMessage`/`AIMessage` objects, retrieved chunks in `RetrievalQA`, and buffered conversation history in `ConversationBufferMemory` are all, by the time they reach the model, just... more text, concatenated together in a specific format the model was trained to expect. LangChain's objects are a *convenience for you*, the developer, to build that text correctly — the model itself just sees one long string of tokens either way.

## 17. Why embeddings work: geometry, not understanding

Section 8 (in Part 1) described embeddings as vectors that place similar-meaning text close together. The theoretical "why" behind this: an embedding model is trained so that, over a vast number of examples, texts that tend to appear in similar contexts, or that were labeled/curated as similar in meaning, end up with vectors close together — and it captures this "closeness" using the *geometry* of many-dimensional space.

Concretely, "how close" two vectors are is usually measured with **cosine similarity** — the cosine of the angle between the two vectors, ranging from -1 (opposite meaning) to 1 (identical meaning), with 0 meaning unrelated. Two vectors pointing in almost the same direction (small angle between them) get a cosine similarity near 1, regardless of how long the vectors are — this matters because it means the comparison is purely about *direction* (meaning), not magnitude (something like text length), which is exactly the property you want for semantic search.

It's worth being precise about what this is *not*: an embedding model has no understanding of truth, logic, or facts. It only encodes **statistical patterns of what kind of text tends to co-occur with what other kind of text**. Two sentences can have very similar embeddings while one is true and one is false, because "sounds similar" and "is factually equivalent" are different properties — this is exactly why RAG (Section 19 below) still needs the LLM's generation step on top of retrieval, rather than just returning the closest chunk verbatim as "the answer."

## 18. Why chunking is a trade-off, not a solved problem

Section 7 mentioned that small chunks embed more precisely, but this deserves the "why" spelled out:

An embedding vector is a single fixed-size summary of *everything* in the text you feed it. If you embed a huge chunk covering five different subtopics, the resulting vector is forced to average/blend all five topics into one point in vector space — and averaging five different things together tends to produce something that isn't a strong, precise match for a search query about *any one* of them specifically. This is why very large chunks tend to retrieve poorly: the embedding is "diluted."

But make chunks too small, and you hit the opposite problem: a two-sentence fragment might embed very precisely (because it really is about one narrow thing), but when the LLM receives it, it may lack the surrounding context needed to actually answer the question well — a chunk that says "the temperature was set to 0.1" is a precise match for a query about model temperature, but useless to the LLM without the preceding sentence explaining *which* parameter that's even referring to.

There's no universally "correct" chunk size — it depends on your documents' structure and how self-contained a typical passage is. The `ParentDocumentRetriever` pattern (Section 10) exists specifically because this trade-off has no single right answer: it lets you optimize the *search* step and the *context* step independently by using two different chunk sizes for two different jobs.

## 19. Why RAG works — and where it breaks

The theoretical case for RAG: an LLM's knowledge is frozen at training time and is a statistical compression of its training data — it did not "read and file away" your specific PDF, and it has no way to look things up on demand from a plain `.invoke()` call. RAG's fix is to sidestep training entirely: instead of trying to get facts *into* the model's weights, you fetch the facts fresh at *question time* and hand them to the model as part of the prompt, where the model's genuinely strong ability (reading and synthesizing text it's given) does the actual answering.

This is why RAG can answer questions about a document a model has never been trained on, and why it tends to reduce (but never fully eliminate) **hallucination** — the phenomenon where a model states something false with full confidence, because generating fluent, plausible-sounding text is what it was trained to do, and "plausible-sounding" and "true" aren't the same target. Grounding the answer in retrieved, real source text gives the model something true to work from — but if the retriever returns the *wrong* chunk (Section 18's chunking trade-off, or simply because the vector space doesn't perfectly capture your query's intent), the model will still confidently generate an answer, just now confidently built on the wrong source material. RAG reduces one failure mode (making things up from nothing) but doesn't remove the risk of the retrieval step itself being wrong.

## 20. Why "memory" is really just a context-window budgeting problem

Every model has a maximum number of tokens it can accept in a single call — a hard ceiling baked into how it was trained (this is the model's "context window"). `ConversationBufferMemory` (Section 12) works by re-sending the *entire* prior conversation as part of the prompt on every single turn. This means the prompt gets strictly longer every turn, and there is nothing conceptually stopping it from eventually exceeding the model's context window if a conversation runs long enough — at which point either older messages must be dropped, or the call fails outright.

This is the real reason alternatives like `ConversationSummaryMemory` (mentioned in this lab's Exercise 5) exist: instead of keeping the verbatim transcript growing without bound, it periodically asks the LLM itself to compress the conversation so far into a shorter summary, and that summary (not the full transcript) is what gets resent going forward. It trades some fidelity (fine details from early in the conversation may get lost in the summary) for a bounded, roughly constant prompt size — a direct, practical answer to the fact that "remembering everything, forever" is not actually free when the underlying mechanism is "resend it all, every time."

## 21. Why agents can "reason" — and the real limits of that reasoning

The ReAct loop (Section 15) can look like the model is "deciding" to use a calculator the same way a person would. What's actually happening, mechanically: the model has been trained (or, for larger models, prompted effectively enough) to recognize that *text describing a plan* (a `Thought`/`Action` block) is often a highly probable continuation when the preceding text describes a task that benefits from a tool — because its training data contains huge amounts of text where humans describe exactly this kind of step-by-step problem-solving. The "reasoning" is the model continuing a very learned *pattern of what reasoning-shaped text looks like*, not a separate logical-inference engine bolted on underneath.

This distinction matters practically, not just philosophically: it's why smaller models (like the `qwen2.5:7b` used in the local variant of this lab) are noticeably less reliable at strictly following the `Thought → Action → Action Input` format than a larger model would be — producing that exact structured format under all conditions is itself a skill the model has to have learned well, and smaller models are more prone to blending a `Final Answer` into the same turn as an `Action` (which is exactly the "Parsing LLM output produced both a final answer and a parse-able action" retries you'll see if you run this notebook's Exercise 7 yourself). The model isn't "confused" in a human sense — it's just that the probability mass at that point slightly favors a format that doesn't perfectly match what `AgentExecutor`'s parser is strictly expecting, and `handle_parsing_errors=True` exists specifically to paper over that gap by asking the model to try again.

It's also worth being clear about what an agent *cannot* do that this might make you assume it can: it cannot verify a tool's output is correct beyond what the tool itself reports, it cannot reliably know when it's stuck in a repeating loop without an explicit iteration limit, and it has no persistent goal or intention between separate `.invoke()` calls — every property that looks like "wanting" to solve the problem is, underneath, the same one-token-at-a-time continuation described in Section 16, just applied across a multi-step Thought/Action/Observation transcript instead of a single response.

## 22. Putting the theory back into the lab

Tying this back to what you actually ran in `05b`:

- When Exercise 1 showed different creativity at different temperatures, that's Section 16's sampling behavior directly, not the model "trying harder" to be creative.
- When the retriever in Exercise 4 returned relevant chunks for "What is LangChain?", that's Section 17's cosine similarity in action — the query's embedding vector landed close to chunks whose embeddings encode similar statistical context, not because anything "understood" the question.
- When the two splitters in Exercise 3 produced different chunk counts and statistics, that's Section 18's chunk-size trade-off made concrete — neither splitter's output is "more correct," they just sit at different points on the precision-vs-context trade-off.
- When `qa.invoke("what is this paper discussing?")` correctly summarized the arXiv paper's real content, that's Section 19's RAG mechanism — the model wasn't trained on that specific paper; it was handed relevant real chunks of it moments before answering.
- When the chatbot in Exercise 5 correctly recalled "my favorite color is blue" several turns later, that's Section 20 — the entire conversation, including that fact, was silently re-sent as part of every subsequent prompt.
- When the agent in Exercise 7 correctly chose the Calculator tool for "What is 25 + 63?" and the Text Formatter for the uppercase request, and occasionally needed a retry to get the output format exactly right, that's Section 21 — pattern-continuation that looks like decision-making, running up against the real limits of how reliably a 7B-parameter local model can hit an exact structured format every time.

## Why This Matters

This lab is where the pieces of the certificate's later courses start to visibly connect. RAG (Sections 6–11, and the theory in Sections 17–19) is the entire subject of Courses 2–4 in this certificate — everything here (loaders, splitters, embeddings, vector stores, retrievers) is the exact same machinery, just introduced here at a smaller scale before those courses go deeper into more advanced retrieval strategies and dedicated vector databases like Pinecone and FAISS. Tools and agents (Sections 14–15, and the theory in Section 21) are the foundation for Courses 6–9, which build out far more sophisticated agent orchestration (LangGraph, multi-agent systems, CrewAI, MCP) on top of exactly this same core idea: a model that reasons about which action to take, takes it via real code, and incorporates the result before deciding what to do next.

The single most important mental model from this whole lab — and the thread running through all of Part 2 — is that an LLM by itself is *only* a text-in, text-out, one-token-at-a-time function with no memory and no ability to act. Everything covered here (chat message roles, memory objects, retrievers, tools, the agent executor loop) is application-level scaffolding built *around* that one narrow capability, to make it behave like something with memory, access to external knowledge, and the ability to take real actions in the world — not because the model gained new abilities, but because the surrounding code keeps re-feeding it exactly the right text, at exactly the right moment, to produce that appearance.
