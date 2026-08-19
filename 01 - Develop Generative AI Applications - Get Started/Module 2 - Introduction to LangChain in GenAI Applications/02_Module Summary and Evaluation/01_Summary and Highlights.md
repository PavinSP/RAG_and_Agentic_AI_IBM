# Summary and Highlights: Introduction to LangChain in GenAI Applications

Congratulations! You have completed this module. At this point in the course, you know:

- LangChain is an open-source interface that simplifies the application development process using LLMs.
- The core components of LangChain are:
  - The language models that use text input to generate text output.
  - The chat models that understand questions or prompts and respond like a human.
  - The chat models that handle chat messages such as `HumanMessage`, `AIMessage`, `SystemMessage`, `FunctionMessage`, and `ToolMessage`.
  - The prompt templates that translate a user's question or messages into clear instructions.
  - The example selector that informs the model about the input context and guides the LLM to generate the desired output.
  - The output parsers that transform the output from an LLM into a suitable format.
- LangChain is a platform that embeds APIs for the development of applications.
- Chains are the sequence of calls in LangChain, and the output for one step becomes the input for the next step.
- Chains first define the template string for the prompt, then create a prompt template using the defined template, and then create an `LLMChain` object.
- Memory storage is important for reading and writing historical data.
- Agents are dynamic systems where the language model determines the sequence of actions.
- Agents integrate with tools such as search engines, databases, and websites to fulfill user requests.
