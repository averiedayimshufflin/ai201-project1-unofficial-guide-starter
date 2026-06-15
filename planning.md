# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

I chose student reviews of CS professors at UMD because although we have a rate my professor-inspired website, it is difficult to find all possible student reviews because not everyone is inclined to post on that website regarding their personal experience. Instead you may find reviews on forums like reddit or even on various social media platforms. Furthermore, there is certain bias on more websites than one and some reviews are not as specific as others. 

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->
| #  | Source                                   | Description                                                                             | URL or location                                    |
| -- | ---------------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------- |
| 1  | PlanetTerp CMSC132 Reviews               | Student reviews for CMSC132 professors.                                                 | https://planetterp.com/course/CMSC132/reviews      |
| 2  | PlanetTerp CMSC216 Reviews               | Student reviews for CMSC216 professors and course workload.                             | https://planetterp.com/course/CMSC216/reviews      |
| 3  | PlanetTerp CMSC250                       | Ratings and professor history for CMSC250.                                              | https://planetterp.com/course/CMSC250              |
| 4  | PlanetTerp CMSC330 Reviews               | Student reviews for CMSC330 instructors.                                                | https://planetterp.com/course/CMSC330/reviews      |
| 5  | PlanetTerp CMSC351                       | Ratings and review counts for CMSC351 professors.                                      | https://planetterp.com/course/CMSC351              |
| 6  | PlanetTerp Justin Wyss-Gallifent         | Professor-level reviews for Justin Wyss-Gallifent across CMSC courses.                 | https://planetterp.com/professor/wyss-gallifent    |
| 7  | PlanetTerp Larry Herman                  | Professor-level reviews for Larry Herman across CMSC courses.                          | https://planetterp.com/professor/herman_larry      |
| 8  | Rate My Professors Fawzi Emad            | Student ratings and comments for Fawzi Emad.                                           | https://www.ratemyprofessors.com/professor/313062  |
| 9  | Rate My Professors Ilchul Yoon           | Student ratings and comments for Ilchul Yoon.                                          | https://www.ratemyprofessors.com/professor/2327417 |
| 10 | Christopher Kauffman CMSC216 Course Page | Official CMSC216 course page for comparing student reviews with actual course policies. | https://www.cs.umd.edu/~profk/216/                 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
