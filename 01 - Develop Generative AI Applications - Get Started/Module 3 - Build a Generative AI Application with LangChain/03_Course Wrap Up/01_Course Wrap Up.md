# Course Wrap-up

## AI Q&A: Course Wrap-up

> Raw prompts and AI responses from the course reading, preserved and organized into Q&A form.

### Combining self-consistency and few-shot prompting improves AI reliability by:

1. Using few-shot prompting to give the AI clear examples, helping it understand the task and expected output patterns.
2. Then applying self-consistency, where the AI generates multiple answers based on those examples.
3. The AI compares these multiple answers and selects the one that appears most often or is most consistent.

This process reduces the chance of random or incorrect outputs, making the AI's responses more dependable and accurate.

### What is the role of LangChain in building Gen AI applications?

LangChain plays a key role in building Generative AI applications by providing a framework that simplifies working with large language models (LLMs). Its main contributions are:

- **Modular components** — building blocks like language models, chat models, prompt templates, output parsers, and chains to structure AI workflows.
- **Chains** — enable creating sequences of steps where the output of one step feeds into the next, allowing complex multi-step tasks.
- **Agents** — support dynamic decision-making where the AI chooses actions or tools (like databases or search engines) to fulfill user requests.
- **Readable syntax** — its expression language (LCEL) uses a pipe operator to connect components cleanly, making code easier to write and understand.

Overall, LangChain helps developers build flexible, context-aware, and powerful Gen AI applications more efficiently.

### How does LangChain's agent system improve AI application flexibility?

LangChain's agent system improves AI application flexibility by allowing the AI to:

- **Dynamically decide actions** — instead of following a fixed sequence, the agent chooses what steps or tools to use based on the current task or user input.
- **Integrate external tools** — agents can access databases, search engines, or APIs to gather information or perform tasks beyond just generating text.
- **Adapt to complex requests** — by combining language understanding with tool usage, agents handle diverse and changing user needs more effectively.

This makes AI applications smarter and more responsive, able to handle a wider range of real-world scenarios.
