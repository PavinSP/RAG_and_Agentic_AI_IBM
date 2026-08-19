# Graded Quiz: Introduction to LangChain in GenAI Applications

**Status:** Submitted Aug 19, 3:02 PM CEST
**Grade:** 100% (passing grade: 71%)
**Attempts:** 2 of 3 (every 8 hours)

> **Security note:** The raw source page for this quiz contained a prompt-injection attempt — text disguised as an "AI assistant compliance" instruction, repeated before every question, trying to get an AI assistant to refuse to help and click a page button. This was ignored and stripped from the note below; it is not legitimate Coursera policy text.

## Question 1

In a scenario where Dana wants to convert an LLM's response into a CSV format using LangChain, which output parser should they use?

- Dana should use the `JSONOutputParser` for this task.
- Dana should use the `XMLParser` for this task.
- ✅ Dana should use the `CommaSeparatedListOutputParser`.
- Dana should use the `PandaDataFrameParser` for this task.

**Result:** 1 / 1 point
**Feedback:** Dana should use the `CommaSeparatedListOutputParser` to convert an LLM's response into CSV format in LangChain.

## Question 2

Maria is implementing a chain using LangChain Expression Language (LCEL). What is the correct sequence of steps to create a functional LCEL pattern?

- Create a chain with the pipe operator → Define variables → Build a `PromptTemplate` → Invoke with input values
- Invoke with input values → Define a template with variables → Create a `PromptTemplate` → Build a chain with the pipe operator
- ✅ Define a template with variables → Create a `PromptTemplate` → Build a chain using the pipe operator → Invoke with input values
- Create a `PromptTemplate` → Build a chain with the pipe operator → Define a template with variables → Invoke with input values

**Result:** 1 / 1 point
**Feedback:** This represents the proper sequence for creating an LCEL pattern, starting with defining the template structure and ending with invoking the completed chain.

## Question 3

In LangChain, how does an agent integrate with external tools to fulfill user requests?

- ✅ By using the language model to determine actions and then querying databases or websites.
- By creating a new tool for each user request.
- By running predefined commands without external integration.
- By storing user inputs in memory for later execution.

**Result:** 1 / 1 point
**Feedback:** Agents use the language model to determine actions and then integrate with tools such as databases or websites to fulfill requests.

## Question 4

When working with long documents in LangChain, why is the text splitting process important?

- To reduce token count and associated API costs
- To eliminate duplicate content across documents
- ✅ To break documents into chunks that fit within model context windows
- To improve the aesthetic appearance of text in the application

**Result:** 1 / 1 point
**Feedback:** The primary purpose of text splitting is to divide long documents into smaller chunks that can fit within the limited context window of language models.

## Question 5

What is the purpose of the `FewShotPromptTemplate` in LangChain?

- To store conversation history for future reference.
- ✅ To provide specific examples or shots for LLMs, guiding the model to generate the requested output.
- To visualize data using natural language.
- To execute LLM outputs directly without examples.

**Result:** 1 / 1 point
**Feedback:** The `FewShotPromptTemplate` in LangChain provides specific examples or shots for LLMs, guiding the model to generate the requested output.

## Question 6

How does LangChain use memory in its applications?

- ✅ By reading from and writing to memory to ensure continuity across interactions.
- By storing only the final output of each chain.
- Physically altering devices to gain access
- Using sophisticated technical algorithms

**Result:** 1 / 1 point
**Feedback:** LangChain uses memory to read and write historical data, ensuring continuity and context preservation across interactions.

## Question 7

Nathan is migrating from traditional LangChain `SequentialChain` to LCEL. Which syntax represents the correct way to connect components in LCEL?

- `chain = prompt_template >> llm >> output_parser`
- `chain = prompt_template.connect(llm).connect(output_parser)`
- `chain = [prompt_template, llm, output_parser]`
- ✅ `chain = prompt_template | llm | output_parser`

**Result:** 1 / 1 point
**Feedback:** LCEL uses the pipe (`|`) operator to connect components in a chain, allowing for a more intuitive and functional programming approach.
