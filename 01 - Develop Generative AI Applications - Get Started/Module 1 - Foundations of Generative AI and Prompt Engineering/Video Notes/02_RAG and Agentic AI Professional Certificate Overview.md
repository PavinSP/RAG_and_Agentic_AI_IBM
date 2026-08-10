# Video Note: RAG and Agentic AI Professional Certificate Overview

**Video length:** 5 min

## Overview

Program-level overview video introducing the three pillars of the certificate — Retrieval Augmented Generation (RAG), Multimodal AI, and Agentic AI — and walking through what each of the program's courses covers.

## The Three Pillars

- **Retrieval Augmented Generation (RAG)** — enhances AI's ability to provide accurate, context-aware responses by integrating real-time information retrieval.
- **Multimodal AI** — allows systems to process and integrate various types of data (text, images, audio, video), enabling more dynamic and interactive user experiences.
- **Agentic AI** — equips systems with the ability to reason, plan, and autonomously execute tasks.

These three approaches can work independently, but can also be combined to build more powerful and adaptable AI systems.

## Program Structure

The certificate consists of several short courses, each corresponding to an online course completable independently. Each course has 2-3 modules. Completing the courses and required projects earns the completion certificate.

### Course 1 — Generative AI Applications (this course)

- Basics of Generative AI, prompt engineering, in-context learning, and prompt templates.
- Introduction to the LangChain framework for building generative AI applications, which streamlines AI workflows through structured, efficient prompt chaining.

### Course 2 — RAG Applications

- Key components of Retrieval Augmented Generation (RAG).
- Implementing RAG using LangChain.
- Introduction to **Gradio** for setting up an interface to interact with AI models.
- Working with **LlamaIndex** as an alternative to LangChain — hands-on building a bot with LlamaIndex and IBM's **Granite** model.

### Course 3 — Vector Databases for RAG

- The role of vector databases in modern data management systems.
- **ChromaDB**'s architecture and common coding practices for its operations.
- Hands-on basic vector operations and similarity search labs.
- Building a recommendation system using a vector database and an embedding model.

### Course 4 — Advanced RAG with Vector Databases and Retrievers

- Advanced retrievers and retrieval patterns; implementing and optimizing retrieval strategies within a RAG system.
- Working with **FAISS**, a vector database for efficient similarity search.
- Building a RAG application using FAISS, LangChain, and Gradio.

### Course 5 — Multimodal Generative AI Applications

- Introduction to Multimodal AI — how AI systems process and integrate multiple data types.
- Evaluating speech recognition and text-to-speech technologies, and computer vision.
- Working with tools such as **OpenAI Whisper** and **Mistral** to build multimodal applications.
- How models like **DALL-E** ("DALI" in the transcript — likely a Whisper mis-transcription) generate images, and the fundamentals of image captioning.
- Multimodal retrieval and search, multimodal question answering, and chatbots — how cross-modal retrieval techniques enhance search engines and recommendation systems.

### Course 6 — Fundamentals of Building AI Agents

- Function calling, chaining, and tool orchestration for AI systems to interact with external tools and execute tasks.
- Manually handling tool calls by parsing language model outputs.
- Using LangChain's built-in agents, including DataFrame and SQL agents, to analyze structured data, generate visualizations, and query databases via natural language.

### Course 7 — Agentic AI with LangChain and LangGraph

- Using LangGraph and LangChain to develop stateful workflows.
- Key architectures such as agents and ReAct agents, applied to real-world applications.
- Multi-agent system design and agentic RAG architecture.

### Course 8 — Agentic AI with LangGraph, CrewAI, AutoGen and BeeAI

- Designing AI workflows using multi-agent orchestration frameworks.
- Agentic frameworks such as **CrewAI** and **LangGraph**.
- Alternative agentic frameworks: IBM's **BeeAI** framework and **AG2** (formerly AutoGen), for multi-agent collaboration and conversation-driven systems.

> **Note:** The transcript names only 8 courses in detail, but the certificate's actual course list (per Coursera's own program page) has 10 courses, including *Build AI Agents using MCP* (Course 9) and the *RAG and Agentic AI Capstone Project* (Course 10). This video's narration appears to predate or simply omit those two — not an error in this note, just a gap in the source video itself.

## Assessment & Completion

- Practice and graded quizzes evaluate learning; graded quizzes carry weight toward course completion.
- Hands-on labs and projects contribute to course and program completion requirements.
- Completing all courses earns the IBM program completion certificate.

## Why This Matters

This overview is the map for the entire certificate — it's worth returning to whenever a later course references a tool or concept without introducing it, since this video is where it was first named (e.g., ChromaDB in Course 3, FAISS in Course 4, CrewAI/AG2/BeeAI in Course 8). It also clarifies the throughline of the whole program: each course adds one capability — retrieval, then vector search, then multimodality, then agency — and the later courses combine all of them. Course 1 (the one this note's module belongs to) is explicitly framed here as the foundation the rest of the program builds on, particularly the LangChain prompt-chaining concepts.
