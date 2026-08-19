# Video Note: LangChain Chains and Agents for Building Applications

**Video length:** 7 min

## Overview

Covers three of LangChain's application-building tools: **chains** (built up through a full three-step sequential-chain worked example), **memory** (how conversation history is read and written), and **agents** (dynamic systems where the LLM decides which actions to take, demonstrated with a Pandas DataFrame agent).

> Transcription note: the automatic transcript repeatedly renders "LangChain" as "LLM chain." The correct term — LangChain — is used throughout this note.

## Learning Objectives

- Describe chains in LangChain for generating responses.
- Describe how LangChain stores memory.
- Define agents used in LangChain.

## Chains

In LangChain, **chains are a sequence of calls**. A **sequential chain** consists of basic steps where each step takes one input and generates one output, creating a seamless flow of information — **the output from step one becomes the input for step two**.

### The worked example: dish → recipe → cooking time

The goal: given a location, identify the famous dish there, its recipe, and the estimated cooking time. This is built from three individual chains wired together.

**Chain 1 — location → dish**

Takes the user's specified location as input and returns a famous dish from there. Given `China`, the output should be *Peking duck*.

Code steps:
1. Define a template string asking for a specific dish from a specified location.
2. Create a `PromptTemplate` object from that template, with `location` as the input variable.
3. Create an `LLMChain` object named `location_chain` using an LLM (Mixtral), assuming a chat model object already exists.
4. The output is stored under the key **`meal`**.

**Chain 2 — dish → recipe**

Takes the output of chain 1 (the dish name) as its input; outputs the recipe itself.

1. Define a template asking for a simple recipe for a given meal.
2. Create a `PromptTemplate` with `meal` as the input variable.
3. Create an `LLMChain` named `dish_chain` with output key **`recipe`**.

**Chain 3 — recipe → cooking time**

Takes the recipe from chain 2 and estimates the cooking time.

1. Define a template to estimate cooking time for a given recipe.
2. Create a `PromptTemplate` with `recipe` as the input variable.
3. Create an `LLMChain` named `recipe_chain` with output key **`time`**.

**Combining them**

A `SequentialChain` wraps all three individual chains into one unified process. Invoking a query through the combined chain lets you trace the flow of information from start to end.

Setting **`verbose=True`** displays the overall output — a clear, detailed view of how each input is transformed through the chain into the final output.

Note the key-passing mechanism: each chain declares an output key (`meal` → `recipe` → `time`), and the next chain consumes it as its input variable. That naming is what stitches the sequence together.

## Memory

Memory storage matters for **reading and writing historical data**. Each chain relies on specific inputs — from the user, and from memory.

The two-phase pattern per run:

1. The chain **reads** from memory to enhance the user's inputs, *before* executing its core logic.
2. After execution, the chain **writes** the current run's inputs and outputs back to memory.

This is what ensures continuity and context preservation across interactions.

### `ChatMessageHistory`

The **`ChatMessageHistory`** class manages and stores conversation histories, including both human and AI messages, letting you append messages from either side.

The example:

1. Instantiate `ChatMessageHistory`.
2. Add the AI message `"hi"` — memory appends it as an AI message.
3. Add the user message `"what is the capital of France"` — memory appends it as a human message.
4. Subsequent responses are generated based on the stored memory.

## Agents

**Agents** are dynamic systems where a language model **determines and sequences actions**, such as predefined chains.

The crucial distinction: the model **generates text outputs to guide actions but does not execute them directly.** Agents integrate with tools — search engines, databases, websites — to actually fulfill requests.

The illustrative example: if a user asks for the population of Italy, the agent uses the language model to work out its options, queries a database for details, and returns a curated list. This shows the agent autonomously combining **LLM reasoning with external tools**.

### The Pandas DataFrame agent

This agent lets users query and visualize data using natural language.

1. Instantiate `create_pandas_dataframe_agent`.
2. Pass in the LLM chat model and the DataFrame.
3. Set `verbose=True` to watch how the LLM reasons.
4. Invoke a query — *"how many rows in the DataFrame"*.

The LLM transforms the natural-language query into **Python code**, which is executed in the background, producing a precise answer. In the example, the response reports **139 rows**.

## Recap

- LangChain is a platform that embeds APIs for developing applications.
- Chains are a sequence of calls; the output from one step becomes the input for the next.
- Building a chain: define the template string, create a prompt template from it, then create the chain object.
- Memory storage is important for reading and writing historical data.
- Agents are dynamic systems where a language model determines and sequences actions.
- Agents integrate with tools such as search engines, databases, and websites to fulfill requests.

## Why This Matters

The read-then-write memory pattern described here is the honest mechanical explanation of how a chatbot "remembers" anything: nothing is stored inside the model, so the framework re-injects prior turns into each new prompt. That's worth internalizing because it explains the cost — every remembered turn consumes context window on every subsequent call, which is exactly why `ConversationSummaryMemory` (compress old turns) exists alongside `ConversationBufferMemory` (keep them verbatim) in the module's lab.

The **agent** distinction — the model *decides* actions but does not *execute* them — is the single most important idea for the back half of this certificate. It's the foundation of the ReAct Thought→Action→Observation loop in the Module 2 lab, and Courses 6 through 9 are built entirely on it. The Pandas agent example also quietly demonstrates why agents are powerful *and* risky: the LLM writes Python that then actually runs, which is real capability and real exposure in equal measure.

One historical note worth carrying forward: this video teaches `LLMChain` and `SequentialChain`, the **older** LangChain API. Module 1's LCEL video explicitly recommends the pipe-operator pattern instead, and the labs use LCEL (`template | model | parser`). Both appear in this course, so it's useful to recognize `LLMChain` in older code and know the modern equivalent — the output-key plumbing done manually here is what LCEL's piping handles implicitly.
