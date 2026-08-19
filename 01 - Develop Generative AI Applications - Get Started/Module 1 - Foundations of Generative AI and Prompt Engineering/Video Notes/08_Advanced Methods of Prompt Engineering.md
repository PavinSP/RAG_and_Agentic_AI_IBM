# Video Note: Advanced Methods of Prompt Engineering

**Video length:** 6 min

## Overview

Walks through five prompting techniques in ascending order of sophistication — zero-shot, one-shot, few-shot, chain-of-thought, and self-consistency — each with a concrete worked example. Then covers the tooling landscape for prompt engineering, LangChain's `PromptTemplate` (with code), and the concept of agents.

## Learning Objectives

- Apply advanced methods of prompt engineering to enhance prompt design.
- Discuss the effective implementation of the tools and applications of prompt engineering in real-world scenarios.

## Zero-Shot Prompting

Instructs an LLM to perform a task **without any prior specific training or examples**.

The example: the LLM is asked to classify a statement as true or false —

> "The Eiffel Tower is located in Berlin."

The model responds directly. This requires the LLM to understand the context and the information without any previous tuning for that specific query.

## One-Shot Prompting

Gives the LLM **a single example** to help it perform a similar task.

The example given is a translation task. The prompt first demonstrates translating one English sentence to French:

> "How was the weather today?" → *(French translation)*

That demonstration serves as a **template**. Then a new sentence is supplied:

> "Where is the nearest supermarket?"

The LLM is expected to translate it into French using the learned format — using the initial example to correctly perform the new translation.

## Few-Shot Prompting

The AI learns from **a small set of examples** before tackling a similar task, which helps it generalize from a few instances to new data.

The example: the LLM is shown three statements, each labeled with an emotion. Those examples teach it to classify emotions based on context. Then it's given a new statement:

> "That movie was so scary I had to cover my eyes."

...and outputs the emotion.

## Chain-of-Thought (CoT) Prompting

A technique to guide the LLM through complex reasoning **step by step**. Highly effective for problems requiring multiple intermediate steps, or reasoning that mimics human thought processes.

The arithmetic example: a store initially had **22 apples**, sold **15**, then received a new delivery of **8**. How many apples are there now?

Rather than answering in one jump, the model breaks the calculation into clear, sequential steps. Two benefits result: it arrives at the correct answer, **and** it provides a transparent explanation of how it got there.

## Self-Consistency

A technique for enhancing the reliability and accuracy of outputs. It works by **generating multiple independent answers to the same question**, then evaluating them to determine the most consistent result.

The example is an age-calculation problem:

> "When I was 6, my sister was half my age. Now I am 70 — what age is my sister?"

The model is prompted to produce **three independent calculations and explanations**. You can then compare the three different routes and identify the consistent answer. This cross-verifies multiple paths to the same answer, which is what makes the final result trustworthy.

## Tools for Prompt Engineering

Tools that facilitate interaction with LLMs include **OpenAI's Playground**, **LangChain**, **Hugging Face's Model Hub**, and **IBM's AI Classroom**.

What they provide:

- Develop, experiment with, evaluate, and deploy prompts.
- Real-time tweaking and testing, so you see the immediate effect on outputs.
- Access to various pre-trained models suited to different tasks and languages.
- Sharing and collaborative editing of prompts across teams or communities.
- Tracking changes, analyzing results, and optimizing prompts against performance metrics.

## LangChain Prompt Templates

LangChain uses **prompt templates** — predefined recipes for generating effective prompts. A template can include:

- Instructions for the language model,
- Few-shot examples to help the model understand context and expected responses,
- A specific question directed at the model.

The code walked through in the video:

```python
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("Tell me a {adjective} joke about {content}.")
prompt_template.format(adjective="funny", content="chickens")
# -> "Tell me a funny joke about chickens."
```

The template has placeholders for an **adjective** and the **content**; calling `.format()` with `funny` and `chickens` produces the finished prompt. This simplifies prompt creation and makes prompts consistent and adaptable across different contexts.

## Agents

In prompt applications, an **agent** is a crucial concept. Powered by LLMs and integrated tools like LangChain, agents perform complex tasks across domains using different prompts.

Transformative applications named:

- **Q&A agents** with sources
- **Content agents** for creation and summarization
- **Analytic agents** for data analysis and business intelligence
- **Multilingual agents** for context-aware translation and communication

## Recap

- Advanced prompt engineering methods: zero-shot, one-shot, few-shot, chain-of-thought, and self-consistency.
- Tools facilitate interactions with LLMs.
- LangChain uses prompt templates to generate effective prompts.
- An agent can perform complex tasks across domains using different prompts.

## Why This Matters

This video is the practical core of Module 1 — the five techniques here are exactly what the module's hands-on lab (`07_Master Prompt Engineering and LangChain PromptTemplates`) implements one by one, and what the Module 1 cheat sheet tabulates. The progression is not arbitrary: each technique buys you something the previous one couldn't, at the cost of more prompt real estate. Zero-shot is free but fragile; few-shot costs tokens but pins down the output format; CoT costs many more tokens but fixes multi-step reasoning; self-consistency costs *multiple full generations* but catches the cases where a single CoT run reasons plausibly to a wrong answer.

The `PromptTemplate` code shown here is the same class used in every lab from this point forward, including the Module 3 Flask app's `qwen_template`. Worth connecting: the "few-shot examples" that a template can hold are just in-context learning from the previous video, packaged into a reusable object.

The **agents** section is a forward pointer rather than something used here — it becomes concrete in Module 2 (`create_react_agent`, `AgentExecutor`, the ReAct Thought→Action→Observation loop) and is the entire subject of Courses 6–9 of this certificate.
