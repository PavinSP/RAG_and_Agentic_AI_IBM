# Understanding the Code: The Simple English Version

This is the plain-language version of [05c_Understanding Coding.md](<05c_Understanding Coding.md>). Same lab, same 15 concepts, same depth — but written the way you'd explain it to a friend over coffee, not the way you'd write documentation.

If a sentence here feels "too simple," that's on purpose. You can always go back to `05c` for the more technical version once the idea clicks.

## Table of Contents

**Part 1 — What the Code Actually Does**

1. Two ways to talk to a model
2. Who said what — labeling messages
3. Fill-in-the-blank prompts, for conversations
4. Making the AI answer in a specific shape
5. A "Document" is just text plus a sticky note
6. Getting text out of a PDF or a webpage
7. Why we chop documents into pieces
8. Turning words into numbers (embeddings)
9. A database built for those numbers
10. "Find me the relevant bit" — retrievers
11. The full "read the doc, then answer" bot
12. Giving the chatbot a memory
13. Two ways to chain steps together
14. Giving the AI hands — tools
15. Agents: the AI that decides what to do

**Part 2 — Why Any of This Actually Works**

16. What is the model actually doing, underneath?
17. Why "similar meaning" numbers work
18. Why chopping documents is a trade-off
19. Why "look it up first" (RAG) helps
20. Why memory is really just "say it all again"
21. Why agents seem to think — and where that breaks down
22. Connecting the theory back to what you ran

23. Why This Matters

---

## Part 1 — What the Code Actually Does

## 1. Two ways to talk to a model

There are two ways to send text to an AI model in this lab.

The plain way: you send one string of text, you get one string of text back. Like sending a text message to someone who has no memory of you — every message is a fresh start.

The "chat" way: instead of one plain string, you send a *list* of labeled messages — this part was said by the system, this part was said by the human, this part was said by the AI. It's the difference between shouting a sentence into a room versus handing someone a script with each line labeled "Narrator," "You," "Them."

In the real IBM version of this lab, these are two separate tools (`ModelInference` for the plain way, `WatsonxLLM` for the chat way). In our local version, one tool (`OllamaLLM`) does both jobs, because the model underneath doesn't actually care — it's still just reading text either way. The "chat" idea is really just a *convention* for organizing that text, not a different kind of AI.

## 2. Who said what — labeling messages

```python
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
```

Three labels you'll see everywhere:

- **`SystemMessage`** — instructions you give the AI before the conversation starts. Like handing an actor their character notes before the scene begins. The user never sees this; it just shapes how the AI behaves.
- **`HumanMessage`** — something a real person typed.
- **`AIMessage`** — something the AI said, earlier in the conversation.

Here's the important, slightly surprising bit: **the AI has no memory of its own.** Every time you call it, it's starting from zero. If you want it to "remember" what it said three messages ago, *you* have to physically include that old message again, every single time, as part of what you send it. `AIMessage` exists so you have a labeled way to hand back its own old words to it.

Think of it like talking to someone with short-term memory loss, where you're allowed to hand them a written transcript of the conversation so far before they answer. They're not "remembering" — you're reminding them, every time.

## 3. Fill-in-the-blank prompts, for conversations

You already know about fill-in-the-blank templates for a single string (`"Tell me a {adjective} joke"`). This lab shows the version for a whole *list* of labeled messages:

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("user", "Tell me a joke about {topic}")
])
```

Same idea, just one template *per message* instead of one template total.

There's also a special slot called `MessagesPlaceholder`. Normal blanks hold one piece of text. This one holds an *entire list of messages* — because sometimes you don't want to fill in one word, you want to slot in a whole chunk of prior conversation at once. Think of it as a placeholder that says "insert the whole conversation-so-far right here," rather than "insert one word right here."

## 4. Making the AI answer in a specific shape

An AI only ever gives you back plain text. If your program needs that text to actually be a real, structured piece of data — a proper list, a proper JSON object you can pull fields out of — something has to convert the text into that shape. That "something" is called an output parser.

### Getting back a proper JSON object

```python
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

output_parser = JsonOutputParser(pydantic_object=Joke)
format_instructions = output_parser.get_format_instructions()
```

Think of `Joke` as a form with two labeled boxes: "setup" and "punchline." You're not filling the form in yourself — you're describing the shape of the form so the parser knows what to look for.

`get_format_instructions()` turns that form-shape into plain English instructions that get slipped into the prompt, basically saying "please answer using exactly this JSON shape." Then when the AI's text comes back, the parser reads through it, finds the JSON, and hands you back a real Python dictionary — not text that *looks* like a dictionary, an actual one you can grab `result['setup']` from.

### Getting back a simple list

```python
output_parser = CommaSeparatedListOutputParser()
```

Same idea, much simpler target: "please answer with items separated by commas," and the parser splits that response into a real Python list.

## 5. A "Document" is just text plus a sticky note

```python
Document(
    page_content="Python is an interpreted...",
    metadata={'my_document_id': 234234, 'my_document_source': "About Python"}
)
```

A `Document` is nothing fancy. It's a piece of text (`page_content`) with a sticky note attached (`metadata`) — extra facts about where that text came from, like a page number or a source name. The sticky note doesn't change the text; it just travels along with it so later steps in the pipeline can say "oh, this chunk came from page 3 of that PDF."

Every tool later in this lab — the loaders, the splitters, the search engine — works on lists of these `(text + sticky note)` pairs. Once you see that, the rest of the "RAG" pipeline is just: "a bunch of tools that take a list of these and hand back a modified list of these."

## 6. Getting text out of a PDF or a webpage

```python
loader = PyPDFLoader("https://arxiv.org/pdf/2403.05568")
document = loader.load()
```

A loader's only job: go get some text from somewhere (a PDF, a webpage, whatever) and hand it back as a list of `Document`s. The PDF loader gives you one `Document` per page. The webpage loader (`WebBaseLoader`) scrapes a page and hands back its readable text the same way.

The whole point of loaders is that everything *after* this step doesn't need to know or care where the text originally came from — a chunk of PDF text and a chunk of webpage text look identical to the rest of the pipeline.

> **Local-variant note:** the PDF link the original lab used is dead outside IBM's own training environment (we checked — it really does return a "not found" error). This local version fetches the real paper the lab was talking about, straight from its actual public home on arXiv, and says so clearly in the notebook.

## 7. Why we chop documents into pieces

A whole PDF is too big to hand to an AI usefully — both because there's a limit to how much text you can send at once, and because later, when you're searching for something, you want to find *the specific relevant paragraph*, not "somewhere in this entire 40-page document."

```python
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20, separator="\n")
```

- `chunk_size=200` — aim for roughly 200-character pieces.
- `chunk_overlap=20` — each new piece repeats the last 20 characters of the piece before it. This is so a sentence that happens to land right on the cut line doesn't get chopped in half and ruined in both resulting pieces — the overlap gives each piece a little breathing room from its neighbor.
- `separator="\n"` — prefer cutting at a line break rather than mid-sentence, when possible.

There's a smarter splitter too (`RecursiveCharacterTextSplitter`) that tries paragraph breaks first, then sentence breaks, then word breaks, only resorting to a rough cut if it has to. Think of the difference as "cut wherever, every 200 characters" versus "try to cut at a natural pause point first, and only cut mid-sentence as a last resort."

## 8. Turning words into numbers (embeddings)

```python
embedding_result = watsonx_embedding.embed_documents(texts)
embedding_result[0][:5]  # first 5 numbers of the first chunk's vector
```

An embedding model reads a piece of text and spits out a long list of numbers — a "vector." That list of numbers isn't meaningful to look at directly, but here's the trick: text with *similar meaning* gets turned into number-lists that are mathematically *close together*. Text about unrelated topics ends up far apart.

Picture a giant map where every sentence ever written gets a dot somewhere on it. Sentences about cooking cluster in one area. Sentences about outer space cluster somewhere else, far away. An embedding model's whole job is deciding where on that map any given sentence belongs.

This "closeness on the map" is what lets you search by *meaning* instead of by matching exact words — you can ask about "cooking" and still find a passage that talks about "recipes" and "the kitchen," even though it never uses the word "cooking" at all.

## 9. A database built for those numbers

```python
docsearch = Chroma.from_documents(chunks, watsonx_embedding)
docs = docsearch.similarity_search("Langchain")
```

Chroma is a database, but instead of being built for "find the row where name = Alice," it's built for "find the dots on that meaning-map that are closest to this new dot." `.from_documents(...)` does two jobs at once: it turns every chunk into a number-list (Section 8), and it stores those number-lists so you can search them later.

`.similarity_search("Langchain")` takes your search text, turns it into a number-list the same way, and returns whichever stored chunks landed closest to it on the map.

## 10. "Find me the relevant bit" — retrievers

```python
retriever = docsearch.as_retriever()
docs = retriever.invoke("Langchain")
```

A retriever is a simple, standard shape: "give me a question, I'll give you back relevant text." `docsearch.as_retriever()` just wraps the Chroma database so it fits that standard shape — the benefit being that other parts of your program (like the QA bot in Section 11) don't need to know or care *how* the retriever finds its answers underneath, only that it follows this same simple "ask, get text back" pattern.

### The "small pieces for searching, big pieces for reading" trick

Remember from Section 7: small chunks are easier to search precisely, but they can be missing context once you actually try to *read* them. `ParentDocumentRetriever` solves this by keeping two versions of every document — small pieces (for the searching step) and big pieces (for the reading step) — and it's set up so that searching happens on the small ones, but once it finds a match, it hands you back the *big* piece that small piece came from. Best of both: precise search, full context in the answer.

## 11. The full "read the doc, then answer" bot

```python
qa = RetrievalQA.from_chain_type(
    llm=llama_llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(),
)
qa.invoke("what is this paper discussing?")
```

This wires together everything above into one simple call. Ask it a question, and behind the scenes it: finds the relevant chunks (Section 10), stuffs them together with your question into one prompt, sends that to the AI, and returns the answer. This *is* what "RAG" means in practice — the AI's answer is backed by real text it just read seconds ago, not just whatever it happened to memorize while it was being trained.

`chain_type="stuff"` is just the name for "the simplest strategy: literally stuff all the found chunks together into the prompt." There are fancier strategies for when there's too much found text to fit in one prompt, but this is the basic starting point.

## 12. Giving the chatbot a memory

Same idea as Section 2 (the AI has no memory of its own) — this section is about tools that automate the "remind it every time" trick, so you don't have to do it by hand.

```python
history = ChatMessageHistory()
history.add_ai_message("hi!")
history.add_user_message("what is the capital of France?")
ai_response = chat.invoke(history.messages)
history.add_ai_message(ai_response)
```

`ChatMessageHistory` is just a growing list of messages with two easy "add to the list" buttons. You build it up one message at a time, and it hands you back the whole list in the exact shape the chat model wants (Section 2).

```python
conversation = ConversationChain(llm=llama_llm, memory=ConversationBufferMemory())
conversation.invoke(input="Hello, I am a little cat. Who are you?")
conversation.invoke(input="Who am I?")
```

This is the "I don't even want to manage the list myself" version. Every time you call it, it quietly: reads everything said so far, builds the full prompt including that history, sends it, reads the answer, and saves both your new message and the AI's answer for next time. That's the entire trick behind why, a few messages later, asking "Who am I?" correctly gets "you're a little cat" back — nothing was truly *remembered*; the whole conversation so far was just quietly resent, every time, behind the scenes.

One catch worth knowing: this means the "conversation so far" text you're resending just keeps growing and growing, forever, the longer you chat. Eventually that could get too big. That's what a fancier memory type (`ConversationSummaryMemory`, used in this lab's Exercise 5) is for — instead of keeping the whole word-for-word transcript, it periodically asks the AI to boil the conversation down into a short summary, and carries forward *that* instead, so it doesn't keep growing forever.

## 13. Two ways to chain steps together

You already know the modern way to link steps (`prompt | model | parser` with the pipe symbol). This lab shows you the *older* style too, because a lot of real-world code still uses it.

```python
location_chain = LLMChain(llm=llama_llm, prompt=prompt_template, output_key="meal")
```

`LLMChain` does the same job as `prompt | model`, just with an older-style wrapper. The one new idea: `output_key="meal"` — it names its result "meal," so a later step in a multi-step chain can refer to that name directly.

```python
overall_chain = SequentialChain(
    chains=[location_chain, dish_chain, recipe_chain],
    input_variables=['location'],
    output_variables=['meal', 'recipe', 'time'],
)
```

`SequentialChain` runs a list of these named-output steps one after another, automatically feeding each one's named result into the next step that's expecting a value with that same name. You have to explicitly list, up front, what goes in and what should come out at the end.

The modern (pipe-operator) way of doing the exact same three-step job:

```python
overall_chain_lcel = (
    RunnablePassthrough.assign(meal=lambda x: location_chain_lcel.invoke(x))
    | RunnablePassthrough.assign(recipe=lambda x: dish_chain_lcel.invoke(x))
    | RunnablePassthrough.assign(time=lambda x: time_chain_lcel.invoke(x))
)
```

`RunnablePassthrough.assign(name=...)` means "take whatever's flowing through so far, calculate one more thing, and add it to the pile under this name — without throwing away anything that was already there." Do that three times in a row, and by the end you've got a single bundle holding the location, the meal, the recipe, *and* the cooking time, all at once. Same end result as `SequentialChain`, just built up piece by piece instead of declared all at once up front.

## 14. Giving the AI hands — tools

Everything so far is still just "the AI reads text, the AI writes text." A tool is how you let it actually *do* something real — run code, fetch a real answer — instead of only generating more words.

```python
python_calculator = Tool(
    name="Python Calculator",
    func=python_repl.run,
    description="Useful for when you need to perform calculations or execute Python code."
)
```

A tool is just three things stuck together: a name, the actual function that runs when it's used, and a description explaining what it's for. That description matters a lot more than it looks — it's the *only* information an agent has to decide "should I use this tool right now?" A vague description means the agent will guess wrong more often.

```python
@tool
def search_weather(location: str):
    """Search for the current weather in the specified location."""
    return f"The weather in {location} is currently sunny and 72°F."
```

`@tool` is just a shortcut that turns an ordinary function into that same three-part package automatically, using the function's name and its description-comment.

A "toolkit" is just a plain list of these tools, handed to an agent so it has several options to choose from.

## 15. Agents: the AI that decides what to do

```python
agent = create_react_agent(llm=llama_llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
result = agent_executor.invoke({"input": "What is the square root of 245?"})
```

"ReAct" is short for "Reasoning + Acting." It's a specific style of prompt that tells the AI: "write your thinking out loud, then name one tool you want to use and what to give it — and then stop." The AI isn't actually running anything itself; it just writes that plan down as text.

The `AgentExecutor` is the part that turns that written plan into something real:

1. It sends your question to the AI.
2. The AI writes back a "Thought" and an "Action" (which tool, with what input) and stops.
3. The executor reads that text, finds the named tool, and *actually runs it for real* — genuine code execution, not the AI pretending.
4. Whatever that tool really returns gets fed back to the AI as an "Observation."
5. The AI is asked again, now seeing its own earlier plan plus the real result, and either takes another action or, once it has enough, writes a "Final Answer" and the loop stops.

This is why using an agent quietly makes *several* calls to the AI behind one question, not just one — each round of thinking → acting → observing is its own trip to the model. `handle_parsing_errors=True` exists because smaller models (like the one used locally here) sometimes don't format their "Thought/Action/Final Answer" text perfectly on the first attempt — this setting tells the executor to nudge it and try again instead of just crashing.

---

## Part 2 — Why Any of This Actually Works

Part 1 was about what the code does. This part is about the actual machinery underneath — the stuff that's true no matter which company's model or which library you're using.

## 16. What is the model actually doing, underneath?

Every single "ask the AI something" moment in this whole lab boils down to one repeated action: **the model guesses the single most likely next word-piece, adds it, and then guesses the next one, over and over.**

That's genuinely it. A "token" is roughly a word or a piece of a word. The model has seen an enormous amount of text during training and has become very good at one narrow skill: "given everything written so far, what word-piece is most likely to come next?" It picks one (sometimes the most likely one, sometimes something a little more surprising, depending on the `temperature` setting), tacks it on, and repeats — a whole paragraph is just this one small step, done thousands of times in a row.

This one fact explains a bunch of things that would otherwise seem mysterious:

- **It can't go back and fix an earlier sentence.** It only ever adds new words at the end. If it starts an answer badly, it's often stuck building on that bad start. This is part of why "think step by step" prompts help — writing the reasoning out loud gives it a chance to correct course in a *later* word, based on its own earlier words, instead of committing to a wrong answer in one shot.
- **`temperature` controls how safe or adventurous each guess is.** Low temperature: almost always pick the single most likely next word (feels consistent, predictable). High temperature: sometimes pick a less-likely-but-still-reasonable word on purpose (feels more varied, more surprising, occasionally a little less coherent).
- **Everything in this lab — labeled chat messages, chunks pulled from a document, the whole conversation history — eventually just becomes one long string of plain text before the model ever sees it.** There's no special "memory slot" or "document slot" wired into the model. All the fancy-sounding objects in this lab are there to help *you*, the programmer, correctly assemble that one long piece of text — the model itself is just reading text and guessing the next word, exactly the same way, no matter what kind of object that text started out as.

## 17. Why "similar meaning" numbers work

An embedding model turns text into a list of numbers such that similar-meaning text ends up with similar number-lists. Why does that actually work? Because during its own training, it saw huge amounts of text and learned patterns of "what kind of text tends to show up in similar situations as what other kind of text" — and it encodes that pattern using *position* in a giant, many-dimensional space.

The way "how similar are these two number-lists" gets measured is usually something called cosine similarity — basically, how close in *direction* two arrows are pointing, on a scale from "pointing the exact same way" to "pointing the exact opposite way." Two sentences with similar meaning end up as arrows pointing in nearly the same direction, and that's what "close together" really means here.

Important thing to keep in mind: **the model doesn't actually understand anything true or false here — it only knows what tends to sound similar.** Two sentences can land right next to each other on the meaning-map even if one of them is completely wrong, because "sounds like it's about the same topic" and "is factually correct" are two different things. This is exactly why the "look it up first" system (RAG) still needs the AI to write a real answer afterward, instead of just handing you the closest-matching sentence and calling that "the answer."

## 18. Why chopping documents is a trade-off

A number-list from an embedding model is a single, fixed-size summary of *everything* in the text you gave it. If you hand it a giant chunk covering five different topics, that one number-list has to try to represent all five topics blended together — and a blend of five things is rarely a sharp, precise match for a search about any *one* of them. That's why huge chunks tend to search badly: the summary gets watered down.

But go too small, and you hit the opposite problem: a tiny two-sentence fragment might match a search really precisely, but once the AI actually reads it, it might be missing the context needed to make sense of it — like getting handed the sentence "the setting was 0.1" with no idea what that number is even a setting *for*.

There's no single perfect chunk size — it depends on the document. The "small pieces for searching, big pieces for reading" trick from Section 10 exists specifically because nobody's solved this trade-off with one universal number; instead, it just uses two different chunk sizes for two different jobs.

## 19. Why "look it up first" (RAG) helps

Here's the core problem RAG solves: an AI model's knowledge got locked in whenever its training finished. It didn't "read your PDF and file it away" — it has no way to look anything up on its own when you just ask it a plain question. RAG's fix: instead of trying to somehow teach the model your specific facts, just go fetch the real facts fresh, right when the question is asked, and hand them to the model as part of the question. The model's genuinely good skill — reading text and writing a sensible answer based on it — does the rest.

This is why RAG can correctly answer questions about a document the model has literally never seen before, and why it tends to cut down on the AI just making things up (this "making things up confidently" problem has a name: **hallucination**). Sounding fluent and confident is what the model was trained to do — being *correct* is a separate goal that doesn't always line up with "sounds confident." Handing it real, true source text to work from gives it something solid to answer from. But if the search step (Section 10) hands back the *wrong* chunk, the model will still answer confidently — just now confidently wrong, based on the wrong source. RAG fixes one kind of mistake (making things up from nothing) but doesn't fully protect you from a different kind (searching for the wrong thing).

## 20. Why memory is really just "say it all again"

Every AI model has a hard limit on how much text it can be handed in one go — its "context window." The chatbot memory trick from Section 12 works by literally resending the *entire* conversation so far, every single time you ask something new. That means the message you're sending gets a little bit bigger every single turn, forever, with nothing stopping it from eventually going past that hard limit if the conversation runs long enough.

That's the real reason a fancier memory type exists that periodically asks the AI to summarize the conversation instead of keeping every word. You lose a little detail (some small things from early on might get smoothed out of the summary), but in exchange, what you're resending stays roughly the same size instead of growing without end. It's a very direct, practical answer to a very simple problem: "remembering everything forever" isn't free when the actual mechanism behind it is "just say the whole thing again."

## 21. Why agents seem to think — and where that breaks down

Watching an agent pick a calculator tool for a math question can feel like watching it genuinely decide something, the way a person would. What's really happening: the model has learned that "a written-out plan" (a Thought, followed by an Action) is often a very likely thing to come next, right after text describing a task that clearly needs a tool — because it saw tons of human-written examples of exactly this kind of step-by-step problem-solving during training. It's not running a separate "logic engine" underneath. It's continuing a pattern of "what does reasoning-shaped text usually look like," the same one-word-at-a-time way described in Section 16 — just applied across several rounds instead of one.

This matters in a very concrete way: it's exactly why a smaller model (like the one used in this local version of the lab) sometimes fumbles the exact "Thought / Action / Final Answer" format it's supposed to follow — nailing that exact structure every time is itself a skill some models are just better at than others. When that happens, you'll see a "couldn't quite parse that, trying again" retry — that's not the AI being confused in a human sense, it's just that its best guess for the next few words didn't land in *exactly* the format the code was strictly expecting, and the retry setting exists specifically to smooth that over.

Worth being honest about the real limits here too: an agent can't actually check whether a tool's answer is correct beyond just trusting what the tool reported back. It has no built-in sense of "wait, I'm going around in circles" without someone explicitly capping how many rounds it's allowed. And it has no ongoing goal that persists between separate questions — anything that looks like "wanting" to solve the problem is, underneath, the exact same next-word-guessing from Section 16, just stretched out across a longer back-and-forth transcript instead of one single answer.

## 22. Connecting the theory back to what you ran

Tying this straight back to the actual notebook:

- Exercise 1's different creativity at different temperatures — that's Section 16's word-guessing behavior, not the model "trying harder."
- The retriever in Exercise 4 finding relevant chunks for "What is LangChain?" — that's Section 17's meaning-map matching, not real understanding.
- The two splitters in Exercise 3 giving different chunk counts — that's Section 18's trade-off, made visible; neither one is "more correct."
- `qa.invoke("what is this paper discussing?")` correctly describing the real arXiv paper — that's Section 19's RAG trick, working exactly as intended.
- The chatbot in Exercise 5 correctly recalling "my favorite color is blue" several turns later — that's Section 20; the whole conversation was quietly resent every time, nothing was "remembered" in the way a person remembers.
- The agent in Exercise 7 correctly picking the calculator for "What is 25 + 63?" and occasionally needing a retry to get its formatting exactly right — that's Section 21, pattern-continuation that looks like a decision, bumping into the real limits of a small model's formatting reliability.

## Why This Matters

This lab is where the pieces of the later courses in this certificate start clicking together. The "look it up first" idea (RAG) is the entire subject of courses 2 through 4 — everything you just learned here (loading text, chopping it up, turning it into numbers, storing it, searching it) is the exact same machinery, just introduced small before those courses go deeper with fancier search tricks and dedicated number-databases like Pinecone and FAISS. Giving the AI tools and letting it act (Sections 14–15) is the foundation for courses 6 through 9, which build much more elaborate versions of this same idea — multiple AI "workers" coordinating together, using different frameworks that all solve this same underlying problem.

If there's one idea to walk away with from this whole lab: an AI model, by itself, is only ever a "read text in, guess the next word out" machine, one word at a time, with no memory of its own and no ability to actually do anything. Every single thing covered here — labeled messages, memory objects, document search, tools, the whole agent loop — is scaffolding built *around* that one narrow skill, to make it *feel* like something with memory, real knowledge, and the ability to act in the world. Not because the model itself changed or gained new powers, but because the code around it keeps feeding it exactly the right words, at exactly the right moment, to create that illusion convincingly.
