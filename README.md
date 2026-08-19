# IBM RAG and Agentic AI — Study Notes

Study notes for IBM's **RAG and Agentic AI Professional Certificate** (10 courses).

## Two kinds of notes

- **Course-text notes** — inside each numbered lesson folder, based on Coursera's own lesson text, readings, quizzes, and labs.
- **Video Notes** — one file per lecture video, in each module's `Video Notes/` folder. Audio is extracted with `ffmpeg`, transcribed locally with `mlx-whisper` (`whisper-large-v3-turbo`), then written up in depth. The raw transcripts are tracked alongside them in each module's `Videos/` folder (one sentence per line, for readability); the source `.mp4` files are gitignored.

> Whisper sometimes emits degenerate output over trailing silence — a phrase repeated dozens of times, runs of `.`/`?`, or non-English fragments. Where that happened, the artifacts were trimmed and the transcript ends with a `[Trailing Whisper transcription artifacts on silence removed.]` marker, so the edit is visible rather than silent.
- **Audio Notes** — one narrated MP3 per lesson, in each module's `Audio Notes/` folder, synthesized from that lesson's markdown notes with Kokoro-82M (`af_heart` voice). Gitignored (local only). Course 1 is fully covered — 9 lessons, ~3 hours of narration. Code-heavy companion files (the "Understanding Coding" walkthroughs) are skipped, since code doesn't narrate usefully.

> Reproducing the pipelines: `mlx-whisper` and `kokoro` need **separate virtualenvs** — mlx-whisper requires numpy ≥ 2 while this repo's `langchain 0.2.x` stack requires numpy < 2, so installing them together breaks the labs. Kokoro also ships a broken bundled `espeak-ng` (its dylib has a hardcoded CI build path); fix it by copying `/opt/homebrew/lib/libespeak-ng.1.dylib` and `/opt/homebrew/Cellar/espeak-ng/*/share/espeak-ng-data` over the files in `espeakng_loader/`.

## Courses

1. **[Develop Generative AI Applications: Get Started](01%20-%20Develop%20Generative%20AI%20Applications%20-%20Get%20Started/)**
2. Build RAG Applications: Get Started
3. Vector Databases for RAG: An Introduction
4. Advanced RAG with Vector Databases and Retrievers
5. Build Multimodal Generative AI Applications
6. Fundamentals of Building AI Agents
7. Agentic AI with LangChain and LangGraph
8. Agentic AI with LangGraph, CrewAI, AutoGen and BeeAI
9. Build AI Agents using MCP
10. RAG and Agentic AI Capstone Project

## Course 1: Develop Generative AI Applications: Get Started

### Module 1 - Foundations of Generative AI and Prompt Engineering

- **01_Welcome to the Course**
  - [01_Course Introduction.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/01_Welcome to the Course/01_Course Introduction.md>)
  - [02_RAG and Agentic AI Professional Certificate Overview.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/01_Welcome to the Course/02_RAG and Agentic AI Professional Certificate Overview.md>)
  - [03_Course Overview.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/01_Welcome to the Course/03_Course Overview.md>)
  - [04_Helpful Tips for Course Completion.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/01_Welcome to the Course/04_Helpful Tips for Course Completion.md>)
- **02_Generative AI Essentials**
  - [01_About This Optional Lesson.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/02_Generative AI Essentials/01_About This Optional Lesson.md>)
  - [02_Introduction to Generative AI.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/02_Generative AI Essentials/02_Introduction to Generative AI.md>)
  - [03_What are Generative AI Models.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/02_Generative AI Essentials/03_What are Generative AI Models.md>)
  - [04_What is NLP.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/02_Generative AI Essentials/04_What is NLP.md>)
  - [05_Comprehensive Guide to Generative AI.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/02_Generative AI Essentials/05_Comprehensive Guide to Generative AI.md>)
  - [06_Practice Quiz: Generative AI Essentials.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/02_Generative AI Essentials/06_Practice Quiz: Generative AI Essentials.md>)
- **03_Working with Prompt Engineering and Prompt Templates**
  - [01_Introduction to In-Context Learning.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/03_Working with Prompt Engineering and Prompt Templates/01_Introduction to In-Context Learning.md>)
  - [02_Introduction to LangChain.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/03_Working with Prompt Engineering and Prompt Templates/02_Introduction to LangChain.md>)
  - [03_Advanced Methods of Prompt Engineering.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/03_Working with Prompt Engineering and Prompt Templates/03_Advanced Methods of Prompt Engineering.md>)
  - [04_LangChain LCEL Chaining Method.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/03_Working with Prompt Engineering and Prompt Templates/04_LangChain LCEL Chaining Method.md>)
  - [05_What is Prompt Engineering, and Why Do We Care.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/03_Working with Prompt Engineering and Prompt Templates/05_What is Prompt Engineering, and Why Do We Care.md>)
  - [06_Choosing the Right Prompt Strategy: A Pre-Lab Readiness Check.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/03_Working with Prompt Engineering and Prompt Templates/06_Choosing the Right Prompt Strategy: A Pre-Lab Readiness Check.md>)
  - [07_Master Prompt Engineering and LangChain PromptTemplates.ipynb](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/03_Working with Prompt Engineering and Prompt Templates/07_Master Prompt Engineering and LangChain PromptTemplates.ipynb>) — hands-on lab notebook (faithful copy, uses IBM watsonx.ai)
  - [07b_Master Prompt Engineering and LangChain PromptTemplates (Local Ollama).ipynb](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/03_Working with Prompt Engineering and Prompt Templates/07b_Master Prompt Engineering and LangChain PromptTemplates (Local Ollama).ipynb>) — same lab, rewired to run locally via Ollama (tested working end-to-end)
  - [07c_Understanding Coding.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/03_Working with Prompt Engineering and Prompt Templates/07c_Understanding Coding.md>) — beginner-to-notebook-level walkthrough of every line of code in the lab
  - [08_Practice Assignment.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/03_Working with Prompt Engineering and Prompt Templates/08_Practice Assignment.md>)
- **04_Module Summary and Evaluation**
  - [01_Foundations of Generative AI and Prompt Engineering.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/04_Module Summary and Evaluation/01_Foundations of Generative AI and Prompt Engineering.md>)
  - [02_Cheat Sheet: Foundations of Generative AI and LangChain.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/04_Module Summary and Evaluation/02_Cheat Sheet: Foundations of Generative AI and LangChain.md>)
  - [03_Practice Quiz.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/04_Module Summary and Evaluation/03_Practice Quiz.md>)
  - [04_Graded Quiz.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/04_Module Summary and Evaluation/04_Graded Quiz.md>)
- **Video Notes** — one note per lecture video, written up from local Whisper transcripts
  - [01_Course Introduction.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/01_Course Introduction.md>)
  - [02_RAG and Agentic AI Professional Certificate Overview.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/02_RAG and Agentic AI Professional Certificate Overview.md>)
  - [03_Introduction to Generative AI.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/03_Introduction to Generative AI.md>)
  - [04_What are Generative AI Models.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/04_What are Generative AI Models.md>)
  - [05_What is NLP.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/05_What is NLP.md>)
  - [06_Introduction to In-Context Learning.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/06_Introduction to In-Context Learning.md>)
  - [07_Introduction to LangChain.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/07_Introduction to LangChain.md>)
  - [08_Advanced Methods of Prompt Engineering.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/08_Advanced Methods of Prompt Engineering.md>)
  - [09_LangChain LCEL Chaining Method.md](<01 - Develop Generative AI Applications - Get Started/Module 1 - Foundations of Generative AI and Prompt Engineering/Video Notes/09_LangChain LCEL Chaining Method.md>)

### Module 2 - Introduction to LangChain in GenAI Applications

- **01_LangChain Core Components and Advanced Features**
  - [01_Recap - Introduction to LangChain.md](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/01_LangChain Core Components and Advanced Features/01_Recap - Introduction to LangChain.md>)
  - [02_LangChain Core Concepts.md](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/01_LangChain Core Components and Advanced Features/02_LangChain Core Concepts.md>)
  - [03_LangChain Chains and Agents for Building Applications.md](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/01_LangChain Core Components and Advanced Features/03_LangChain Chains and Agents for Building Applications.md>)
  - [04_LangChain LCEL Chaining Method.md](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/01_LangChain Core Components and Advanced Features/04_LangChain LCEL Chaining Method.md>)
  - [05_Build Smarter AI Apps Empower LLMs with LangChain.ipynb](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/01_LangChain Core Components and Advanced Features/05_Build Smarter AI Apps Empower LLMs with LangChain.ipynb>) — hands-on lab notebook (faithful copy, uses IBM watsonx.ai)
  - [05b_Build Smarter AI Apps Empower LLMs with LangChain (Local Ollama).ipynb](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/01_LangChain Core Components and Advanced Features/05b_Build Smarter AI Apps Empower LLMs with LangChain (Local Ollama).ipynb>) — same lab, rewired to run locally via Ollama, all 7 exercises filled in and verified end-to-end
  - [05c_Understanding Coding.md](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/01_LangChain Core Components and Advanced Features/05c_Understanding Coding.md>) — exhaustive walkthrough of every LangChain concept in the lab (chat messages, RAG pipeline, memory, chains, tools, agents)
  - [05d_Understanding Coding (Simple English).md](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/01_LangChain Core Components and Advanced Features/05d_Understanding Coding (Simple English).md>) — same walkthrough as 05c, rewritten in plain, everyday language
  - [06_Practice Assignement.md](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/01_LangChain Core Components and Advanced Features/06_Practice Assignement.md>)
- **02_Module Summary and Evaluation**
  - [01_Summary and Highlights.md](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/02_Module Summary and Evaluation/01_Summary and Highlights.md>)
  - [02_Cheat Sheet.md](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/02_Module Summary and Evaluation/02_Cheat Sheet.md>)
  - [03_Graded Quiz.md](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/02_Module Summary and Evaluation/03_Graded Quiz.md>)
- **Video Notes**
  - [01_LangChain Core Concepts.md](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/Video Notes/01_LangChain Core Concepts.md>)
  - [02_LangChain Chains and Agents for Building Applications.md](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/Video Notes/02_LangChain Chains and Agents for Building Applications.md>)
  - [03_LangChain LCEL Chaining Method.md](<01 - Develop Generative AI Applications - Get Started/Module 2 - Introduction to LangChain in GenAI Applications/Video Notes/03_LangChain LCEL Chaining Method.md>) — same video as Module 1's; points to that note

### Module 3 - Build a Generative AI Application with LangChain

- **01_Application Development Workflow with Generative AI**
  - [01_Choose the Right AI Model for Your Use Case.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/01_Application Development Workflow with Generative AI/01_Choose the Right AI Model for Your Use Case.md>)
  - [02_ From Idea to AI: Building Applications with Generative AI.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/01_Application Development Workflow with Generative AI/02_ From Idea to AI: Building Applications with Generative AI.md>)
  - [03_Introduction to Flask.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/01_Application Development Workflow with Generative AI/03_Introduction to Flask.md>)
  - [04_Flask: A Gateway to Web Development in Python.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/01_Application Development Workflow with Generative AI/04_Flask: A Gateway to Web Development in Python.md>)
  - [05_Python with Flask for Large Scale Projects.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/01_Application Development Workflow with Generative AI/05_Python with Flask for Large Scale Projects.md>)
  - [06_Cheat Sheet: Web Development using Flask.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/01_Application Development Workflow with Generative AI/06_Cheat Sheet: Web Development using Flask.md>) — cheat sheet: Flask basics, routing, status codes, error handling
  - [07_Choosing the Right Model for Your Application.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/01_Application Development Workflow with Generative AI/07_Hands On Lab: Choosing the Right Model for Your Application/07_Choosing the Right Model for Your Application.md>) — hands-on lab: LLM internals, IBM watsonx.ai (Llama/Granite/Mistral), special tokens, JSON structured outputs, full Flask + LangChain chat app
    - [local_ollama_app/](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/01_Application Development Workflow with Generative AI/07_Hands On Lab: Choosing the Right Model for Your Application/local_ollama_app/README.md>) — same lab, rewired to run locally via Ollama (`qwen2.5:7b`/`qwen2.5:14b`), including the JSON-structured chain and full browser chat UI, verified end-to-end
  - [08_Understanding Coding (Simple English).md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/01_Application Development Workflow with Generative AI/07_Hands On Lab: Choosing the Right Model for Your Application/08_Understanding Coding (Simple English).md>) — full plain-language walkthrough of the lab and every file in `local_ollama_app/`, how they connect, and why port 5000 hit a 403 (macOS AirPlay Receiver conflict)
  - [08_Practice Assignment.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/01_Application Development Workflow with Generative AI/08_Practice Assignment.md>)
- **02_Summary and Evaluation**
  - [01_Summary and Highlights.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/02_Summary and Evaluation/01_Summary and Highlights.md>)
  - [02_Cheat Sheet.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/02_Summary and Evaluation/02_Cheat Sheet.md>)
  - [03_Graded Assignment.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/02_Summary and Evaluation/03_Graded Assignment.md>)
- **03_Course Wrap Up**
  - [01_Course Wrap Up.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/03_Course Wrap Up/01_Course Wrap Up.md>)
  - [02_Congratulations and Next Step.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/03_Course Wrap Up/02_Congratulations and Next Step.md>)
  - [03_Team and Acknowledgement.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/03_Course Wrap Up/03_Team and Acknowledgement.md>)
- **Video Notes**
  - [01_Choose the Right AI Model for Your Use Case.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/Video Notes/01_Choose the Right AI Model for Your Use Case.md>)
  - [02_From Idea to AI - Building Applications with Generative AI.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/Video Notes/02_From Idea to AI - Building Applications with Generative AI.md>)
  - [03_Introduction to Flask.md](<01 - Develop Generative AI Applications - Get Started/Module 3 - Build a Generative AI Application with LangChain/Video Notes/03_Introduction to Flask.md>)

**Course 1 complete.** ✅

_(Index updated as notes are added.)_
