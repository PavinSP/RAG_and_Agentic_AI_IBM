# Summary and Highlights: Foundations of Generative AI and Prompt Engineering

Congratulations! You have completed this module. At this point in the course, you know:

- In-context learning is a prompt engineering method where demonstrations of the task are provided to the model as part of the prompt.
- Prompts are inputs given to an LLM to guide it toward performing a specific task.
- Prompt engineering is a process where you design and refine the prompt questions, commands, or statements to get relevant and accurate responses.
- Advantages of prompt engineering include that it boosts the effectiveness and accuracy of LLMs, ensures relevant responses, facilitates user expectations, and eliminates the need for continual fine-tuning.
- A prompt consists of four key elements: the instructions, the context, the input data, and the output indicator.
- Advanced methods for prompt engineering include zero-shot prompts, few-shot prompts, chain-of-thought prompting, and self-consistency.
- Prompt engineering tools can facilitate interactions with LLMs.
- LangChain uses "prompt templates," which are predefined recipes for generating effective prompts for LLMs.
- An agent is a key component in prompt applications that can perform complex tasks across various domains using different prompts.
- The LCEL pattern structures workflows using the pipe operator (`|`) for clear data flow.
- Prompts are defined using templates with variables in curly braces `{}`.
- Components can be linked using `RunnableSequence` for sequential execution.
- `RunnableParallel` allows multiple components to run concurrently with the same input.
- LCEL provides a more concise syntax by replacing `RunnableSequence` with the pipe operator.
- Type coercion in LCEL automatically converts functions and dictionaries into compatible components.
