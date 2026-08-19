# Practice Quiz: Working with Prompt Engineering and Prompt Templates

**Status:** Submitted Aug 10, 8:54 AM CEST
**Grade:** 80% (passing grade: 60%)
**Attempts:** Unlimited

> **Security note:** The raw source page for this quiz contained a prompt-injection attempt — text disguised as an "AI assistant compliance" instruction, repeated before every question, trying to get an AI assistant to refuse to help and click a page button. This was ignored and stripped from the note below; it is not legitimate Coursera policy text.

## Question 1

How does in-context learning differ from traditional machine-learning approaches regarding model training and task adaptation?

- In-context learning is constrained by the model's initial training data.
- In-context learning involves adjusting the model's weights based on error gradients.
- In-context learning requires fine-tuning the model on specific datasets.
- ✅ In-context learning adapts to new tasks using small examples provided during inference.

**Result:** 1 / 1 point
**Feedback:** In-context learning uses examples at inference time to adapt to new tasks without additional training.

## Question 2

Imagine a situation where a company wants to use an LLM to translate customer reviews into multiple languages without prior examples. Which prompt engineering method is most suitable for this task?

- Few-shot prompting
- Chain-of-thought prompting
- ✅ Zero-shot prompting
- One-shot prompting

**Result:** 1 / 1 point
**Feedback:** Zero-shot prompting allows the LLM to perform tasks like translation without prior specific examples.

## Question 3

What is the primary role of the pipe operator in LangChain's LCEL Chaining Method?

- ✅ To connect components in a readable and flexible manner
- To handle type coercion manually
- To create complex workflows by replacing LangGraph
- To execute components in parallel without input

**Result:** 0 / 1 point
**Feedback:** LangGraph is used for complex workflows, not the pipe operator.

> **Note:** The source page marks this question "Try again" (incorrect) but does not indicate which option was selected as my answer — only the correct answer (✅, inferred from the feedback text matching "connect components in a readable and flexible manner") and the reason the wrong option was wrong. The source doesn't say which of the other three options was actually chosen, so that isn't guessed here.

## Question 4

Imagine you want to build a reusable AI application pattern using LangChain. What is the benefit of using LCEL over traditional LLMChain approaches?

- LCEL eliminates the need for any templates.
- LCEL restricts the use of parallel execution.
- ✅ LCEL provides clearer visualization of data flow.
- LCEL requires more complex syntax to define workflows.

**Result:** 1 / 1 point
**Feedback:** LCEL offers clearer visualization of data flow, enhancing workflow readability and flexibility.

## Question 5

What is the primary advantage of using `PromptTemplate` over hardcoded strings when working with LLMs in LangChain?

- ✅ PromptTemplate enables dynamic insertion of variables into standardized prompt structures.
- PromptTemplate restricts the LLM to only respond with specific formats.
- PromptTemplate automatically optimizes token usage to reduce costs.
- PromptTemplate caches responses to avoid repeated API calls.

**Result:** 1 / 1 point
**Feedback:** PromptTemplate allows variables to be inserted into reusable prompt structures, making prompts dynamic and consistent.
