# Video Note: Introduction to In-Context Learning

**Video length:** 6 min

## Overview

Defines in-context learning as a form of prompt engineering that teaches a model a new task purely through examples in the prompt — no retraining. Then builds up prompt engineering from first principles: what a prompt is, why prompt design matters, and the four structural elements of a well-formed prompt.

## Learning Objectives

- Describe in-context learning.
- Explain the fundamentals of prompt engineering.

## In-Context Learning

**In-context learning** is a specific method of prompt engineering where **demonstrations of the task are provided to the model as part of the prompt, in natural language**.

The defining property: **it requires no additional training.** A new task is learned from a small set of examples presented within the context (the prompt) **at inference time** — the moment the model is asked, not during some earlier training run.

### Advantages

- No fine-tuning on task-specific datasets required.
- Drastically reduces the resources and time needed to adapt an LLM to a specific task.
- Improves performance on that task at the same time.

### Disadvantages

- Constrained by **what can realistically fit in a context**. You only have so much room.
- Complex tasks may still require gradient steps or traditional ML training approaches — adjusting the model's actual weights based on error gradients — rather than examples in a prompt.

## What Is a Prompt?

**Prompts** are instructions or inputs given to an LLM, designed to guide it toward performing a specific task or generating a desired output.

Two main components:

- **Instructions** — clear, direct commands telling the AI what to do. They must be specific enough that the LLM understands the task.
- **Context** — the necessary information or background that helps the LLM make sense of the instruction. Can be data, parameters, or any relevant details that shape the response.

Combining these effectively is what lets you tailor LLMs — from IBM, OpenAI, Google, Meta, and others — to tasks ranging from answering queries to analyzing data to generating content.

## Prompt Engineering

**Prompt engineering** is the specialized process of designing and refining the questions, commands, or statements you use to interact with AI systems, particularly LLMs.

The framing the instructor uses: *the goal is not just about asking a question — it's about how to ask it in the best way possible.* That means carefully crafting clear, contextually rich prompts tailored to get the most relevant and accurate responses.

### Why it's crucial

- **Boosts effectiveness and accuracy** — directly influences how well the LLM functions.
- **Ensures relevance** — enables precise responses suited to the context.
- **Meets user expectations** — clearer prompts mean fewer misunderstandings.
- **Eliminates the need for continual fine-tuning** — the model adapts and learns within its context instead.

### A minimal example

Prompt given to GPT-3.5:

> The wind is

Response:

> blowing gently through the trees, whispering secrets and stories to anyone who cares to listen.

This shows how an open-ended prompt can guide the LLM toward imaginative, detailed output — demonstrating its capacity for creative and engaging content.

## The Four Elements of a Well-Structured Prompt

The instructor breaks a complete prompt into four parts, using a sentiment-classification example throughout:

1. **Instructions** — what needs to be done.
   *"Classify the following customer review into neutral, negative or positive sentiment."*
2. **Context** — the scenario or background the LLM operates in.
   *This review is part of feedback for a recently launched product* — which helps the LLM weigh the sentiment in light of the product's novelty.
3. **Input data** — the actual data to be processed.
   *"The product arrived late, but the quality exceeded my expectations."*
4. **Output indicator** — a clear marker showing where the LLM's response is expected.
   *`Sentiment:`* — signalling that the model should append its classification right there.

## Recap

- In-context learning is a method of prompt engineering where task demonstrations are provided as part of the prompt.
- Prompts are inputs given to an LLM to guide it toward a specific task; they consist of instructions and context.
- Prompt engineering is the process of designing and refining prompts to get relevant, accurate responses.
- Its advantages: boosts effectiveness and accuracy, ensures relevant responses, helps meet user expectations, and removes the need for continual fine-tuning.
- A prompt has four key elements: **instructions, context, input data, and output indicator**.

## Why This Matters

This is the video that turns the abstract "prompting vs. tuning" fork from the foundation-models lecture into an actual technique with named parts. The four-element breakdown is the template the rest of the course builds on: it's exactly the structure LangChain's `PromptTemplate` formalizes, where instructions and context become the fixed template text and input data becomes the `{variable}` slots filled at runtime.

The **output indicator** in particular is the seed of a lot of later material. Ending a prompt with a marker like `Sentiment:` so the model's next-token prediction lands on the answer is the same mechanism behind Module 3's special tokens (`<|im_start|>assistant` left deliberately unfinished) and behind structured JSON output, where `JsonOutputParser.get_format_instructions()` is essentially a very elaborate output indicator telling the model what shape to produce.

The stated disadvantage — being limited by what fits in the context — is also the constraint that motivates most of the rest of the certificate: chunking, retrieval, and memory strategies all exist because you cannot simply paste everything you'd like the model to know into the prompt.
