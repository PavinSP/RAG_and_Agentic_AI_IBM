# Video Note: Choose the Right AI Model for Your Use Case

**Video length:** 4 min
**Presenter:** Nicholas Renaud, Chief AI Engineer, IBM Client Engineering (AI Academy)

## Overview

Frames model selection through an extended gardening analogy, then lays out a concrete five-stage process: write a specific prompt, research available models, evaluate them against that prompt, test large-then-small, and govern continuously. Closes on the organizational side — the cross-functional team implementation requires.

## The Gardening Analogy

The framing the whole video runs on: **an AI model is like a vegetable you want to grow in your garden.**

- Before buying the seeds, you research the weather and water requirements — otherwise the plant dies before it ever flowers.
- As it grows, you evaluate and re-optimize the care you provide so it can thrive.
- For an entire garden you must do that for *every* vegetable, and make sure none of them interact harmfully.
- And you need the variety: **"You can't live on carrots alone."**

## The Multi-Model Approach

That last point is the actual thesis. To make an AI garden grow you need a **variety of models**, not one.

A **multi-model approach** means keeping a range of models available for your AI use cases, so you can pick and choose the right one for the right use case. That in turn gives you the opportunity to examine how each model is designed as you look for the right fit.

### Questions to ask of any model

- **Who built it?**
- **What data was it trained on?**
- **What guardrails are in place for it?**
- **What risks and regulations** do you need to consider and account for?

## The Process

### 1. Write a very specific prompt

A **prompt** is a textual input or instruction given to a large language model that sets up the basics of the AI. A good prompt **clearly articulates your use case and the problem you're solving**.

The first step in choosing a model is writing a prompt that captures four things:

- The **use case**
- The **user problem**
- The **ask of the technology**
- The **guardrails** — what "good" looks like

Note the reframing here: the prompt isn't just how you talk to a model, it's the *specification* you evaluate candidate models against.

### 2. Research the available models

Look at model **size, performance, costs, risks, and deployment methods**.

### 3. Evaluate models against your prompt

Use the information gathered to identify which models you want to test first.

### 4. Test large first, then work down

**Start with a large model** and work with it until it satisfies your original prompt. **Then try to duplicate that result using smaller models.**

You're passing the same prompt through different models to experiment and see which works best. (The logic: prove the task is achievable at all with the most capable model, then find the cheapest model that still clears the bar — rather than starting small and never knowing whether a failure was the model's fault or the prompt's.)

### 5. Continually evaluate and govern

Choosing a model is not the end of the process. Ongoing testing assesses how it's working against **performance and cost benchmarks**.

Back to the garden: you need to tend it, not just plant the seeds and hope for the best. Part of that ongoing care is to:

- Continually **update the data and the prompt** to keep it relevant.
- **Test new models** as they become available.

The explicit warning: don't stick with one model forever and get locked in, because situations change both inside and outside your business.

## Factors Affecting Model Choice

Throughout the process, keep these in view:

- **Performance**
- **Accuracy**
- **Reliability**
- **Speed**
- **Size**
- **Deployment method**
- **Transparency**
- **Potential risks**

## The Team

Implementation requires a team that crosses **both disciplines and lines of business**. Don't treat it as proprietary to any one department — treat it as a distinctly collaborative project needing multiple teams to get running.

That team must be able to **diagnose performance benchmarks**, each of which measures something unique and produces a dataset showing how everything is calculated. Without that, you can't make informed decisions about future models and use cases.

## Closing

Even once the model is running well: continuous **testing, governance, and optimization** are essential to keep it up to date and performing. Models evolve, so your strategy and choices need to evolve too — *"keep growing towards the sun instead of withering on the vine."*

## Why This Matters

This video is the conceptual justification for the module's hands-on lab, and the two map onto each other directly. "Pass the same prompt through different models and compare" is literally what the lab's `llm_test.py` does — calling several models with one identical prompt and printing their answers side by side. The local Ollama version makes the size trade-off tangible too: `qwen2.5:7b` versus `qwen2.5:14b` is exactly the "start large, then try to duplicate with something smaller" experiment, on hardware you control.

The **"what data was it trained on / what guardrails"** questions also connect back to the trustworthiness disadvantage raised in Module 1's foundation-models video, and forward to why RAG matters: when you can't audit a model's training data, grounding its answers in documents you *have* vetted is the practical mitigation.

Two points here are easy to skim past but genuinely load-bearing. First, treating the prompt as a **written specification with guardrails** — not just a question — is what makes model comparison meaningful, since without a fixed definition of "good" you have nothing to score candidates against. Second, the **governance** emphasis is why the certificate later covers evaluation and monitoring rather than stopping at "it works on my machine": a model that was the right choice at selection time can quietly stop being the right choice as data, costs, and available models shift.
