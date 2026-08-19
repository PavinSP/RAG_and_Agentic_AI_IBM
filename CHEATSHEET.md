# Cheatsheet

Formulas, code patterns, and architecture patterns extracted directly from course notes, organized by topic. Anything the course discusses only conceptually (no concrete values/code given) is flagged rather than filled in.

## Course 1: Develop Generative AI Applications — Get Started

### Module 1: Foundations of Generative AI and Prompt Engineering

See [Cheat Sheet: Foundations of Generative AI and LangChain](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/04_Module Summary and Evaluation/02_Cheat Sheet: Foundations of Generative AI and LangChain.md>) for the module's own cheat sheet, covering:

- Setup (`pip install`, `warnings`, `WatsonxLLM`, `llm_model`, `GenParams`)
- Prompting techniques (Basic, Zero-shot, One-shot, Few-shot, Chain-of-thought, Self-consistency)
- LangChain building blocks (`PromptTemplate`, `RunnableLambda`, `StrOutputParser`)
- LCEL pattern (the `|` pipe operator for chaining)

### Module 2: Introduction to LangChain in GenAI Applications

See [Cheat Sheet: Introduction to LangChain in GenAI Applications](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/02_Module Summary and Evaluation/02_Cheat Sheet.md>) for the module's own cheat sheet, covering:

- Chat models & message types (`WatsonxLLM`, `SystemMessage`/`HumanMessage`/`AIMessage`)
- Prompt templates (`PromptTemplate`, `ChatPromptTemplate`, `MessagesPlaceholder`)
- Output parsers (`JsonOutputParser`, `CommaSeparatedListOutputParser`)
- RAG pipeline (`Document`, `PyPDFLoader`, `WebBaseLoader`, `CharacterTextSplitter`, `RecursiveCharacterTextSplitter`, `WatsonxEmbeddings`, `Chroma`, retrievers, `ParentDocumentRetriever`, `RetrievalQA`)
- Memory (`ChatMessageHistory`, `ConversationBufferMemory`)
- Chains (`LLMChain`, `SequentialChain`, `RunnablePassthrough`)
- Tools & agents (`Tool`, `@tool`, `create_react_agent`, `AgentExecutor`)

### Module 3: Build a Generative AI Application with LangChain

See [Cheat Sheet: Web Development using Flask](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/01_Application Development Workflow with Generative AI/06_Cheat Sheet: Web Development using Flask.md>) for the module's own cheat sheet, covering:

- Flask app instantiation (`Flask(__name__)`)
- Routing (`@app.route` decorator)
- Response status codes (200 OK, 4xx client errors, 500 server error)
- Error handling (`@app.errorhandler`)
