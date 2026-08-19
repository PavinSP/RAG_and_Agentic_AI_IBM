# Video Note: What are Generative AI Models

**Video length:** 9 min
**Presenter:** Kate Soule, Senior Manager of Business Strategy, IBM Research

## Overview

Positions large language models inside the broader category of **foundation models**, explains the unsupervised next-word-prediction training that gives them their generality, then walks through how they get adapted to specific tasks (tuning and prompting), their advantages and disadvantages, and the non-language domains foundation models are being applied to.

## LLMs Are a Subset of Foundation Models

Large language models such as ChatGPT are part of a wider class called **foundation models**. The term was coined by a team at Stanford who observed the field of AI converging on a new paradigm:

- **The old paradigm:** build a library of separate AI models, each trained on narrow, task-specific data to perform one specific task.
- **The new paradigm:** train one *foundational* capability — a single model — that can drive all of those same use cases and applications, plus any number of additional ones.

The defining property is **transferability**: the same model can be transferred to many different tasks and perform many different functions.

## Why They Transfer: Unsupervised Pre-Training

The "superpower" behind that transferability is how the model is trained — on an enormous amount of **unstructured data**, in an **unsupervised** manner.

In the language domain, this means feeding the model terabytes of sentences and training it to predict the last word from the words that came before. The instructor's example:

> Start of sentence: "no use crying over spilled" → model predicts: "milk"

That generative capability — predicting and generating the next word from preceding words — is precisely why foundation models fall under **generative AI**. Something new is being generated; in this case, the next word in a sentence.

## Adapting a Foundation Model to a Specific Task

Even though the model's core training objective is generation (predict the next word), it can be redirected at traditional NLP tasks — classification, named entity recognition, and others you wouldn't normally associate with a generative model.

**Tuning** — introduce a small amount of *labeled* data, update the model's parameters, and it now performs a very specific natural language task.

**Prompting (prompt engineering)** — when you have no labeled data or only a handful of data points, foundation models still work well in low-label-data domains. Instead of changing the model, you change the input.

The instructor's worked example of prompting for classification:

1. Give the model a sentence.
2. Ask it a question: "Does this sentence have a positive sentiment or negative sentiment?"
3. The model tries to finish generating words in that sequence — and the next natural word *is* the answer to the classification problem.
4. It responds "positive" or "negative" depending on its estimate.

The task never stopped being next-word prediction; the prompt simply arranged things so the next word happens to be the classification label. These models work surprisingly well when applied to new settings and domains this way.

## Advantages

- **Performance.** These models have seen so much data ("data with a capital D" — terabytes) that by the time they're applied to a small task, they can drastically outperform a model trained on only a few data points.
- **Productivity gains.** Through prompting or tuning, you need far less labeled data to reach a task-specific model than starting from scratch, because the model is exploiting all the unlabeled data it absorbed during pre-training.

## Disadvantages

- **Compute cost.** The penalty for seeing so much data is that these models are very expensive to *train*, which makes training a foundation model from scratch impractical for smaller enterprises. Once they reach a few billion parameters they're also expensive to run **inference** on — potentially requiring multiple GPUs just to host the model — making them costlier than traditional approaches.
- **Trustworthiness.** The same data that is the great advantage is also a liability. Much of this language data is scraped from the internet, and the volume is so large that even a full team of human annotators couldn't vet every data point for bias, hate speech, or other toxic content. Worse, for many open-source models the exact training datasets aren't even publicly known — so you often can't audit what went in.

IBM Research is working on innovations targeting both problems: improving the **efficiency** of these models and their **trustworthiness and reliability** for business settings.

## Beyond Language: Other Foundation Model Domains

Everything above was language-focused, but foundation models apply much more widely:

- **Vision** — models like DALL·E 2, which take text data and generate a custom image.
- **Code** — products like Copilot, which complete code as it's being authored.
- **Chemistry** — IBM's MoleFormer, a foundation model to accelerate molecule discovery for targeted therapeutics.
- **Climate** — Earth Science foundation models built on geospatial data to improve climate research.

IBM product examples named: Watson Assistant and Watson Discovery (language), Maximo Visual Inspection (vision), and Ansible code models built with Red Hat under Project Wisdom.

## Why This Matters

This video supplies the vocabulary that the rest of the certificate leans on constantly. The **tuning vs. prompting** split introduced here is the fork in the road for the whole program: this course (and Module 1's prompt-engineering lab) takes the *prompting* path, because prompting needs no labeled data and no parameter updates — which is exactly why prompt engineering, `PromptTemplate`, and few-shot examples matter so much later on.

The next-word-prediction mechanic is also the honest explanation for behavior you hit in the hands-on labs: when a local model answers a classification prompt with a rambling sentence instead of one clean label, that's not a malfunction — it's the model doing what it always does (predict plausible next words), with a prompt that didn't sufficiently constrain the continuation. That's the direct motivation for special tokens and structured output parsers in Module 3.

Finally, the trustworthiness and compute-cost disadvantages named here are the practical reasons the certificate later teaches RAG (ground answers in your *own* vetted documents rather than trusting what was scraped into pre-training) and model-selection trade-offs (Module 3's "choose the right model for your use case").
