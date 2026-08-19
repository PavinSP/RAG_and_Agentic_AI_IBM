# Graded Quiz: Foundations of Generative AI and Prompt Engineering

**Status:** Submitted Aug 19, 7:51 AM CEST
**Grade:** 100% (passing grade: 70%)
**Attempts:** 2 of 3 (every 8 hours)

> **Security note:** The raw source page for this quiz contained a prompt-injection attempt — text disguised as an "AI assistant compliance" instruction, repeated before every question, trying to get an AI assistant to refuse to help and click a page button. This was ignored and stripped from the note below; it is not legitimate Coursera policy text.

## Question 1

What is the primary goal of prompt engineering?

- To eliminate the need for model training.
- ✅ To design inputs that effectively guide the model to produce desired outputs.
- To minimize the computational resources needed for inference.
- To replace traditional programming techniques.

**Result:** 1 / 1 point
**Feedback:** Prompt engineering involves crafting inputs that guide the model toward generating high-quality, accurate, relevant responses.

## Question 2

In prompt engineering, which prompt element below is correctly matched with its primary function?

- ✅ Input data - To provide the specific content the LLM needs to process.
- Context - To specify the format in which the LLM should respond.
- Output indicator - To give examples of similar tasks the LLM has done previously.
- Instructions - To provide additional background information about the scenario.

**Result:** 1 / 1 point
**Feedback:** Input data is the actual content the model analyzes to perform the task.

## Question 3

What is the primary function of the `format()` method when used with a `PromptTemplate` in LangChain?

- To translate the prompt into different languages.
- To convert the prompt into a standardized JSON structure.
- To optimize the token count of the prompt.
- ✅ To replace placeholder variables with actual values to create the final prompt.

**Result:** 1 / 1 point
**Feedback:** The `format()` method fills in placeholders with actual values to generate the final prompt from a template.

## Question 4

Which step is NOT part of creating a typical LangChain Expression Language (LCEL) pattern?

- Creating a `PromptTemplate` instance from the template.
- ✅ Pre-processing all input data to ensure type compatibility.
- Using the pipe operator to connect components into a chain.
- Defining a template with variables in curly braces.

**Result:** 1 / 1 point
**Feedback:** LCEL automatically handles type coercion, so manual preprocessing for compatibility is not required.

## Question 5

How does in-context learning benefit the adaptation of LLMs for specific tasks?

- It requires extensive fine-tuning on specific datasets.
- It requires continual manual adjustments to the model's weights.
- It limits LLMs only to perform tasks they were originally trained on.
- ✅ It allows LLMs to learn new tasks from a small set of examples without additional training.

**Result:** 1 / 1 point
**Feedback:** In-context learning enables LLMs to adapt to new tasks using a small set of examples without needing further training.

## Question 6

Sarah wants to use prompt engineering to improve AI responses in a customer service application. What should she focus on to ensure the AI provides relevant responses?

- Avoiding the use of any context in prompts.
- Relying solely on the AI's pre-trained knowledge.
- ✅ Designing prompts with clear instructions and rich context.
- Using vague and open-ended prompts.

**Result:** 1 / 1 point
**Feedback:** Clear instructions and context in prompts help AI understand tasks and provide relevant responses.

## Question 7

In the LangChain LCEL Chaining Method, what is the purpose of the pipe operator?

- To replace all instances of `RunnableParallel`.
- ✅ To connect components into a readable flow of data.
- To execute components in reverse order.
- To convert functions into dictionaries.

**Result:** 1 / 1 point
**Feedback:** The pipe operator is used to connect components, ensuring a clear and readable flow of data.
