# Video Note: (Optional) LangChain LCEL Chaining Method

**Video length:** 5 min

## This is the same video as Module 1's

Coursera reuses this lecture in both modules — it appears in Module 1's "Working with Prompt Engineering and Prompt Templates" lesson and again here, marked **(Optional)**, in "LangChain Core Components and Advanced Features." The two source video files are byte-for-byte identical, and so are their transcripts.

**Full note:** [Module 1 → Video Notes → 09_LangChain LCEL Chaining Method.md](<../../Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/09_LangChain LCEL Chaining Method.md>)

## Quick reference

The Module 1 note covers this in full. In brief, the video establishes:

- **LCEL** (LangChain Expression Language) — building chains with the pipe operator `|`, the modern replacement for the older `LLMChain` approach.
- **The four-step pattern** — define a template with `{variables}` → create a `PromptTemplate` → build a chain with `|` → invoke with input values.
- **Two composition primitives** — `RunnableSequence` (sequential, output feeds the next input) and `RunnableParallel` (concurrent, all components get the same input).
- **Automatic type coercion** — a dictionary becomes a `RunnableParallel`; a function becomes a `RunnableLambda`.
- **When not to use it** — LCEL suits simpler orchestration; reach for LangGraph on complex workflows, using LCEL inside individual nodes.

## Why It's Placed Here

Its optional placement in this module is a sequencing decision worth noticing. Module 2's other lecture teaches chains via `LLMChain` and `SequentialChain` — the older API, where you wire steps together by matching output keys to input variables by hand. This video is the modern counterpart to that lecture: the same composition idea, expressed as `template | model | parser`.

Seeing them side by side in one module is genuinely useful. The output-key plumbing that `SequentialChain` makes explicit is what the pipe operator does implicitly, so watching both makes it clear what LCEL is actually abstracting away rather than treating `|` as magic syntax. Every lab in this course uses the LCEL form.
