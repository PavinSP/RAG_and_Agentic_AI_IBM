# Video Note: What is NLP (Natural Language Processing)?

**Video length:** 10 min
**Presenter:** Martin Keen, Master Inventor, IBM

## Overview

Defines NLP as the translation layer between unstructured human language and structured, machine-processable data. Establishes the NLU/NLG split, walks through four representative use cases, then opens up the "bag of tools" that NLP actually consists of: tokenization, stemming, lemmatization, part-of-speech tagging, and named entity recognition.

## The Core Idea: Unstructured ↔ Structured

NLP starts with **unstructured text** — just how people naturally speak or write. The instructor's running example:

> "add eggs and milk to my shopping list"

A human understands that instantly, but to a computer it's unstructured. What a computer needs is a **structured representation** of the same information — something more like a `shopping list` element containing sub-elements: an item for `eggs`, an item for `milk`.

**The job of NLP is to translate between these two forms.** NLP sits in the middle:

- **Unstructured → structured** = **NLU** (Natural Language Understanding)
- **Structured → unstructured** = **NLG** (Natural Language Generation)

This video focuses primarily on the unstructured → structured direction (NLU).

## Use Cases

**Machine translation.** Translating between languages requires understanding the *context* of a sentence, not just swapping word-for-word. The instructor's favorite example of this failing: take "the spirit is willing, but the flesh is weak," translate English → Russian, then translate that back to English, and you get something like *"the vodka is good, but the meat is rotten"* — nowhere near the intended meaning.

**Virtual assistants and chatbots.** A virtual assistant (Siri, Alexa) takes human *utterances* and derives a command to execute. A chatbot does something similar in written language, using the input to traverse a decision tree and take an action.

**Sentiment analysis.** Take some text — an email, a product review — and derive the sentiment expressed in it. Is this review positive or negative? Is it a serious statement, or is it sarcastic?

**Spam detection.** Look at an email message and determine whether it's genuine or spam, using pointers in the content: overused words, poor grammar, or an inappropriate claim of urgency.

## How NLP Works: A Bag of Tools

Key framing from the instructor: **NLP is not one algorithm — it's more like a bag of tools**, and you apply the relevant tools to resolve a given use case.

The input is unstructured text: either written text, or spoken text that has been converted to written text by a speech-to-text algorithm.

### 1. Tokenization

Take a string and break it into chunks. "add eggs and milk to my shopping list" is eight words, so that could be eight **tokens**. Everything downstream works one token at a time.

### 2. Stemming

Derive the **word stem** for a token by stripping prefixes/suffixes and normalizing tense:

- running, runs, ran → **run**

But stemming doesn't work well for every token. *universal* and *university* do not meaningfully stem down to *universe*.

### 3. Lemmatization

For the cases stemming mangles, lemmatization takes a token and learns its meaning via a **dictionary definition**, then derives its root (its **lemma**).

The instructor's clarifying contrast, using *better*:

- **Lemma** of "better" → **good** (because *better* derives from *good*)
- **Stem** of "better" → **bet**

So the choice between stemming and lemmatization is significant for a given token.

### 4. Part-of-Speech Tagging

For a given token, look at where it's used within the context of the sentence. Take *make*:

- "I'm going to **make** dinner" → make is a **verb**
- "What **make** is your laptop?" → make is a **noun**

Position and context in the sentence matter, and POS tagging is what derives that.

### 5. Named Entity Recognition

For a given token, is there an **entity** associated with it?

- token "Arizona" → entity: **US state**
- token "Ralph" → entity: **person's name**

Applying these tools together gets you from unstructured human speech to something structured a computer can understand — and once you have that structured data, you can feed it into all sorts of AI applications.

## Why This Matters

This video explains the world that generative AI *replaced*, which is why it sits in the optional lesson alongside the foundation-models video rather than a competing account. The classic pipeline here — tokenize, stem/lemmatize, POS-tag, NER — is a hand-built sequence of narrow tools, exactly the "library of task-specific models" paradigm that foundation models collapsed into a single transferable model. Seeing the old pipeline laid out makes it concrete *why* the shift was such a big deal: tasks that each needed their own tool now fall out of prompting one general model.

Two ideas here carry directly forward, though. **Tokenization** survives essentially unchanged and becomes central later — it's the unit LLMs actually process, the thing context windows and API pricing are measured in, and the reason Module 3 spends time on special tokens. And the use cases named here (sentiment analysis, classification, entity extraction) are precisely the tasks the labs later solve by prompting instead of by pipeline — including the sentiment/category/action JSON schema built in the Module 3 Flask app, which is this video's sentiment-analysis and NER use cases done the generative way.
