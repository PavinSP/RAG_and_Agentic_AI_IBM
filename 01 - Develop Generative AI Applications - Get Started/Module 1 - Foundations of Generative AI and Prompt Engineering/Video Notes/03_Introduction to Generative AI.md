# Video Note: Introduction to Generative AI

**Video length:** 7 min

## Overview

Introduces generative AI by contrasting it with discriminative AI, then traces the history of generative AI from its origins in machine learning through to today's foundation models and tools.

## Learning Objectives

- Describe generative AI and its evolution.
- Explain how generative AI differs from discriminative AI.

## AI: The Big Picture

AI is the simulation of human intelligence by machines. AI models learn from vast amounts of existing data — this process of learning from data is called **training**. There are two fundamental approaches to AI: **discriminative AI** and **generative AI**.

## Discriminative AI

- Learns to distinguish between different classes of data.
- Given training data where each data point is labeled with its class, the model predicts a new data point's class by finding which side of the **decision boundary** it falls on.
- Uses advanced algorithms to differentiate, classify, identify patterns, and draw conclusions from training data.
- **Example**: email spam filters differentiating spam from non-spam.
- Best applied to classification tasks — but cannot understand context or generate new content based on contextual understanding of the training data.

## Generative AI

- Learns to generate new content based on training data by capturing the underlying distribution of that data and generating novel instances.
- Starts with a **prompt** — text, an image, video, or any other input the model can process.
- Produces new content as output: text, images, audio, video, code, or data.
- Output form can match the prompt's form (text-to-text) or differ from it (text-to-image, image-to-video).

### Discriminative vs. Generative — A Simple Contrast

```
Discriminative AI: "Is this image a drawing of a nest or an egg?"
Generative AI:      "Draw an image of a nest with three eggs in it."
```

Discriminative AI mimics analytical and predictive skills. Generative AI goes further, mimicking creative skills — as the Harvard Business Review put it, "AI can not only boost our analytic and decision-making abilities but also heighten creativity." Generative models take what they've learned and create entirely new content from it.

## Deep Learning Foundation

Both discriminative and generative models are built using **deep learning** — training artificial neural networks on vast amounts of data. An artificial neural network is a collection of smaller computing units called **neurons**, modeled loosely on how the human brain processes information.

Generative AI's creative capability comes from specific generative model architectures, which act as its building blocks:

- Generative Adversarial Networks (GANs)
- Variational Autoencoders (VAEs)
- Transformers
- Diffusion models

## History of Generative AI

Generative AI is not new — its roots trace back to the origins of machine learning.

| Period | Development |
|---|---|
| Late 1950s | Scientists proposed machine learning; explored algorithms to create new data. |
| 1990s | Rise of neural networks drove advancements in generative AI. |
| Early 2010s | Deep learning advanced further, supported by large datasets and stronger computing power. |
| 2014 | GANs introduced by Ian Goodfellow and colleagues — a major turning point for generative AI. |
| 2018 | OpenAI introduced GPT (Generative Pre-trained Transformer), a transformer-based LLM. |

GANs, VAEs, and transformers set the stage for generative AI's growth and the development of **foundation models**.

## Foundation Models and LLMs

- **Foundation models**: AI models with broad capabilities that can be adapted into more specialized models or tools for specific use cases.
- **Large Language Models (LLMs)**: a specific category of foundation model trained to understand human language and process/generate text.

Notable LLMs and models mentioned:

- GPT-3, GPT-4 (OpenAI's GPT series)
- PaLM — Google's Pathways Language Model (spoken as "POM" in the video; likely a Whisper mis-transcription of "PaLM")
- LLaMA — Meta's Large Language Model Meta AI
- Stable Diffusion, DALL-E — image generation models

## Generative AI Tools by Use Case

| Use Case | Tools |
|---|---|
| Text generation | ChatGPT, Gemini |
| Image generation | DALL-E 2, MidJourney |
| Video generation | Synthesia |
| Code generation | Copilot, AlphaCode |

## Economic Impact

Quoting McKinsey's report on the economic potential of generative AI: "Generative AI has the potential to change the anatomy of work, augmenting the capabilities of individual workers by automating some of their individual activities." The report predicts generative AI's productivity impact could add trillions of dollars in value to the global economy.

## Key Takeaways

- Generative AI models generate new content based on the data they're trained on.
- The creative skills of generative AI are built from models such as GANs, VAEs, transformers, and diffusion models.
- Foundation models can be adapted into specialized models or tools for specific use cases.
- Generative AI models and tools have a wide scope for applications across domains and industries.

## Why This Matters

This video sets the conceptual foundation the rest of the course builds on: the discriminative-vs-generative distinction explains *why* a framework like LangChain is needed at all — generative models take open-ended prompts and produce novel output, which requires the kind of structured prompt engineering and chaining this course goes on to teach. The GANs/VAEs/transformers/diffusion-models taxonomy introduced here also resurfaces later in the certificate (e.g., diffusion models return in Course 5's image-generation content), so it's worth anchoring these definitions early.
