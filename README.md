# The Unofficial Guide — Project 1

## Domain

My system covers student reviews of Computer Science professors at the University of Maryland. This knowledge is valuable because students often want to know about teaching style, workload, grading, exams, projects, and course difficulty before registering for a class.

This information is hard to find through official channels because official course descriptions usually only explain course content. They do not describe what students experienced in the class. Student opinions are also scattered across PlanetTerp, Rate My Professors, official course pages, and other informal sources.

---

## Document Sources

| #  | Source                                   | Type                          | URL or file path                                   |
| -- | ---------------------------------------- | ----------------------------- | -------------------------------------------------- |
| 1  | PlanetTerp CMSC132 Reviews               | Review page                   | https://planetterp.com/course/CMSC132/reviews      |
| 2  | PlanetTerp CMSC216 Reviews               | Review page                   | https://planetterp.com/course/CMSC216/reviews      |
| 3  | PlanetTerp CMSC250                       | Course/professor ratings page | https://planetterp.com/course/CMSC250              |
| 4  | PlanetTerp CMSC330 Reviews               | Review page                   | https://planetterp.com/course/CMSC330/reviews      |
| 5  | PlanetTerp CMSC351                       | Course/professor ratings page | https://planetterp.com/course/CMSC351              |
| 6  | PlanetTerp Justin Wyss-Gallifent         | Professor review page         | https://planetterp.com/professor/wyss-gallifent    |
| 7  | PlanetTerp Larry Herman                  | Professor review page         | https://planetterp.com/professor/herman_larry      |
| 8  | Rate My Professors Fawzi Emad            | Professor review page         | https://www.ratemyprofessors.com/professor/313062  |
| 9  | Rate My Professors Ilchul Yoon           | Professor review page         | https://www.ratemyprofessors.com/professor/2327417 |
| 10 | Christopher Kauffman CMSC216 Course Page | Official course page          | https://www.cs.umd.edu/~profk/216/                 |

---

## Chunking Strategy

**Chunk size:** One student review per chunk for review pages. For longer course pages or syllabi, I used about 800–1,000 tokens per chunk.

**Overlap:** 0 overlap for individual reviews. For longer course pages, I used about 100–150 tokens of overlap.

**Why these choices fit your documents:** Most of my documents are review-heavy, so each review should stay together as one chunk. A single review usually contains one complete student opinion about a professor, course, workload, grading, or teaching style. For longer official pages, bigger chunks with overlap help keep course policies and grading details together.

Before chunking, I stripped HTML, removed scripts, headers, footers, navigation text, form/filter text, and other boilerplate. I also filtered out empty chunks and fake chunks such as grade dropdown text from PlanetTerp.

**Final chunk count:** 1833 chunks.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` from `sentence-transformers`.

I chose this model because it runs locally, does not need an API key, is fast enough for a small project, and works well for short pieces of text like student reviews. I stored the embeddings in ChromaDB with source metadata including source name, URL, chunk ID, chunk type, token count, and position.

**Production tradeoff reflection:** If this system were deployed for real users and cost was not a constraint, I would compare stronger embedding models for better retrieval accuracy. I would consider context length, latency, cost, and whether the model handles informal student language well. I would also consider hybrid retrieval, combining keyword search with vector search, because professor names and course numbers often need exact matching.

---

## Grounded Generation

**System prompt grounding instruction:** My system passes only the retrieved chunks into the LLM prompt. The prompt tells the model:

```text
Answer using ONLY the provided retrieved context.
Do not use outside knowledge.
If the retrieved context does not contain enough information, say:
"I don't have enough information on that."
Do not invent professor names, ratings, course facts, or policies.
Keep the answer concise.
Mention the source names that support the answer.
```

This prevents the model from answering based on general knowledge. I also tested an out-of-scope question about UMD dining hall sushi, and the system correctly responded that it did not have enough information.

**How source attribution is surfaced in the response:** Source attribution is shown using metadata from ChromaDB. The interface displays the retrieved source names, URLs, and distance scores separately from the generated answer. This means sources are attached programmatically instead of relying only on the LLM to invent citations.

---

## Evaluation Report

| # | Question                                                                                                              | Expected answer                                                                                                                                                       | System response (summarized)                                                                                                                                                                                                                                                                  | Retrieval quality  | Response accuracy  |
| - | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------ |
| 1 | What CMSC courses expect a heavy workload or mention specifically difficult projects?                                 | The system should identify courses like CMSC216, CMSC330, or CMSC351 if reviews mention demanding projects, exams, or high time commitment.                           | The system identified CMSC330 as having a heavy workload and difficult projects. It cited reviews saying students should start projects early, set aside a lot of time, and that some projects may take over 20 hours. It also mentioned CMSC216 as manageable if projects are started early. | Relevant           | Accurate           |
| 2 | What official course policies from Christopher Kauffman’s CMSC216 page might explain student comments about workload? | The system should mention official course details such as projects, assignments, exams, grading policies, or course expectations that relate to workload.             | The system said it did not have enough information because the retrieved context contained student reviews, not official course policies from Kauffman’s CMSC216 page.                                                                                                                        | Partially relevant | Partially accurate |
| 3 | What do students say about Larry Herman’s teaching style in CMSC132 or CMSC216?                                       | Students generally describe him as knowledgeable and experienced, but some reviews may mention that his courses can be strict, demanding, or fast-paced.              | The system said students describe Larry Herman as strict, sometimes abrasive, monotone, and not very approachable. It also mentioned that some students say he teaches the material well, is detailed, and uses funny analogies.                                                              | Relevant           | Accurate           |
| 4 | What do students say about Justin Wyss-Gallifent’s CMSC351 or CMSC420 courses?                                        | Students often describe him as clear, organized, and helpful, especially for difficult theoretical material, though the courses themselves may still be challenging.  | The system said students describe Wyss-Gallifent’s CMSC351 as high quality, with useful notes for interview preparation. It also mentioned that a student described his CMSC420 class as great, with in-depth lectures and fairly high averages.                                              | Relevant           | Accurate           |
| 5 | Which professors receive mixed or polarizing reviews?                                                                 | The system should identify professors who have both positive and negative comments, especially where students disagree about teaching style, difficulty, or fairness. | The system identified only one unnamed CMSC216 lecturer as receiving mixed reviews. It described the lecturer as “decent” but also “condescending” with poor project management.                                                                                                              | Partially relevant | Inaccurate         |

**Retrieval quality:** Relevant / Partially relevant / Off-target
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:** What official course policies from Christopher Kauffman’s CMSC216 page might explain student comments about workload?

**What the system returned:** The system said it did not have enough information because the retrieved context did not include official course policies from Christopher Kauffman’s CMSC216 page. Instead, the retrieved sources were mostly student reviews about CMSC216 workload, projects, and exams.

**Root cause (tied to a specific pipeline stage):** This failed during the retrieval stage. The official Kauffman CMSC216 page produced only a few large chunks, while the PlanetTerp CMSC216 review page produced many smaller chunks. Because the student review chunks mention words like “Kauffman,” “projects,” “exams,” and “workload” more directly, the embedding search ranked those review chunks higher than the official course page chunks. As a result, the generation step did not receive the official policy context it needed, so it correctly refused to answer.

**What you would change to fix it:** I would improve the pipeline by adding metadata filtering for source type. If a question asks for “official course policies,” the retriever should prioritize or filter for official course pages instead of student reviews. I would also chunk the official CMSC216 page into smaller sections, such as projects, exams, grading, office hours, and policies, so those official-policy chunks are easier for the retriever to match.

---

## Spec Reflection

**One way the spec helped you during implementation:** The spec helped me by making me define my chunking strategy before writing code. Since my documents were mostly student reviews, I knew that one review per chunk would be better than splitting everything into fixed-size blocks. This made most chunks readable and self-contained.

The spec also helped me test each pipeline stage separately. I tested ingestion and chunking before embedding, then tested retrieval before generation. This made it easier to find problems, such as boilerplate chunks and high retrieval distance scores.

**One way your implementation diverged from the spec, and why:** My original plan included Rate My Professors and official course pages as major sources, but the final system relied more heavily on PlanetTerp. Rate My Professors was harder to scrape cleanly, and the official Kauffman course page produced fewer useful chunks than the PlanetTerp review pages.

Another divergence was that the broad comparison question did not work as well as expected. The system could answer specific questions about Larry Herman, Justin Wyss-Gallifent, CMSC330, and CMSC216, but it struggled with questions that required aggregating opinions across many professors.

---

## AI Usage

**Instance 1**

* *What I gave the AI:* I gave ChatGPT my Documents section, Chunking Strategy section, and Architecture diagram from `planning.md`.
* *What it produced:* It produced a Python ingestion script that loaded my 10 URLs, saved raw HTML, cleaned text with BeautifulSoup, and produced chunks.
* *What I changed or overrode:* I inspected the chunks and noticed fake chunks from PlanetTerp form text, such as grade dropdown options. I added filters to remove non-review boilerplate and changed the sample output to print random chunks for inspection.

**Instance 2**

* *What I gave the AI:* I gave ChatGPT my `chunks.json` format and asked it to create embedding and retrieval code using `all-MiniLM-L6-v2` and ChromaDB.
* *What it produced:* It produced code that loaded chunks, embedded them, stored them in ChromaDB, and returned top-k retrieved chunks with distance scores.
* *What I changed or overrode:* The first retrieval scores were too high, so I changed the ChromaDB collection to use cosine distance. After that change, the top retrieval scores were mostly below 0.5 and the chunks were more relevant.

**Instance 3**

* *What I gave the AI:* I asked ChatGPT to help connect retrieval to a Groq LLM and create a Gradio interface.
* *What it produced:* It produced `query.py` for grounded generation and `app.py` for the Gradio interface.
* *What I changed or overrode:* I tested the grounding behavior with an out-of-scope question about UMD dining hall sushi. The system correctly said it did not have enough information, so I kept the grounding prompt and source display structure.
