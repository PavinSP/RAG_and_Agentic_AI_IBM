# Video Note: LangChain LCEL Chaining Method

**Video length:** 5 min

## Overview

Introduces LangChain Expression Language (LCEL) as the modern, recommended way to build chains — replacing the older `LLMChain` approach. Covers the four-step LCEL pattern, the two runnable composition primitives (`RunnableSequence` and `RunnableParallel`), automatic type coercion, and two worked chain examples.

## Learning Objectives

- Describe how to build flexible, composable chains using LangChain's modern approach to prompt engineering.
- Structure prompts effectively using templates.
- Connect components using the pipe operator to streamline workflows.
- Develop reusable patterns for a variety of AI applications.

## What LCEL Is

**LangChain Expression Language (LCEL)** is a pattern for building LangChain applications that uses the **pipe operator (`|`)** to connect components, producing a clean, readable flow of data from input to output.

An important framing note from the instructor: LangChain has evolved significantly, and this video deliberately teaches the **newer, recommended LCEL pattern rather than the traditional `LLMChain` approach**. LCEL provides:

- Better composability
- Clearer visualization of data flow
- Greater flexibility when constructing complex chains

## The Four-Step LCEL Pattern

1. Define a template with variables in curly braces.
2. Create a `PromptTemplate` instance.
3. Build a chain using the pipe operator to connect components.
4. Invoke the chain with input values.

## Runnables

In LangChain, **runnables** serve as both an interface and the building blocks that connect components — LLMs, retrievers, tools — into a pipeline.

There are **two main runnable composition primitives**:

- **`RunnableSequence`** — chains components sequentially, passing the output of one component as the input to the next.
- **`RunnableParallel`** — runs multiple components **concurrently**, giving each of them the *same* input.

### The syntax shortcut

Instead of explicitly using `RunnableSequence`, the same sequential chain can be built by simply connecting components with a pipe:

```python
chain = runnable_1 | runnable_2
```

This makes the structure more readable and intuitive.

## Automatic Type Coercion

LCEL converts ordinary Python into runnable components for you, behind the scenes:

- Use a **dictionary** → it becomes a **`RunnableParallel`** (runs multiple tasks simultaneously).
- Use a **function** → it becomes a **`RunnableLambda`** (transforms inputs).

You never handle the conversion manually.

### The parallel example

In the video's example, a dictionary structure creates a `RunnableParallel` that processes three tasks at once. Each task receives the **same** input (`text`) but does something different with it. The result contains three keys — `summary`, `translation`, and `sentiment` — each holding the output of its respective LLM call.

## Worked Example: A Sequential Joke Chain

The second example builds a chain where a `RunnableLambda` wraps a `format_prompt` function, turning it into a component LangChain can work with. When the chain runs:

1. `RunnableLambda` takes the input dictionary (containing `adjective` and `content` keys).
2. It passes that dictionary to the `format_prompt` function.
3. The function formats the prompt template with those variables.
4. The pipe operator passes the formatted prompt to the **LLM**.
5. Another pipe passes the LLM's response to the **`StrOutputParser`**.

So the full shape is:

```python
chain = RunnableLambda(format_prompt) | llm | StrOutputParser()
```

The pipe operator is what creates the sequence, connecting runnable components together end to end.

## When to Use LCEL — and When Not To

The instructor is explicit about the boundary: **LCEL is best suited for simpler orchestration tasks.** For more complex workflows, consider **LangGraph**, while still using LCEL *within* individual nodes.

LCEL's strengths worth taking advantage of:

- Parallel execution
- Async support
- Simplified streaming
- Automatic tracing

## Recap

- The LCEL pattern structures workflows using the pipe operator for clear data flow.
- Prompts are defined using templates with variables in curly braces.
- Components can be linked with `RunnableSequence` for sequential execution.
- `RunnableParallel` allows multiple components to run concurrently on the same input.
- LCEL provides more concise syntax by replacing `RunnableSequence` with the pipe operator.
- Type coercion automatically converts functions and dictionaries into compatible components.

## Why This Matters

This video explains the single most recognizable piece of syntax in the whole certificate. Every chain built from here on is an LCEL chain: `template | model` in the Module 1 lab, `template | model | json_parser` in the Module 3 Flask app, and the retrieval chains in Module 2. Understanding that `|` is literally `RunnableSequence` with nicer syntax — and that each stage just hands its output to the next — is what makes those one-liners readable rather than magic.

The **type coercion** rule is the practically important detail that's easy to miss: it's why you can drop a bare dictionary or a plain Python function into the middle of a chain and it simply works. That's the mechanism behind `RunnablePassthrough.assign` patterns in Module 2's RAG chains.

`RunnableParallel` is worth remembering for a specific reason: it's the efficient way to run several independent prompts on one input. The Module 3 lab's model-comparison exercise (calling several models with the same prompt to compare their answers) is exactly this shape — and the local Ollama version's `llm_test.py` calls both models on the same input, which is the same idea done sequentially.

Note this same topic reappears as a dedicated lesson in Module 2, so this is the introduction and Module 2 is the deeper pass.
