# How the RAG Code Works

You are now entering the core engineering layer of RAG systems.

A beginner usually sees:

$$\text{Question} \rightarrow \text{AI Answer}$$

But internally, a RAG system performs multiple AI engineering operations.

We will break the entire code into:
1. **PDF Reading**
2. **Chunking**
3. **Embeddings**
4. **Vector Database (FAISS)**
5. **Retrieval**
6. **Prompt Construction**
7. **LLM Generation**
8. **Final Response**

This directly aligns with your AI syllabus **Module 5 on RAG Systems**.

---

## FULL RAG FLOW

```text
       [ PDF Document ]
              │
              ▼
       Text Extraction
              │
              ▼
           Chunking
              │
              ▼
          Embeddings
              │
              ▼
     FAISS Vector Storage
              ▲
              │ (Similarity Search)
              ▼
        User Question
              │
              ▼
      Question Embedding
              │
              ▼
      Similarity Search
              │
              ▼
     Top Relevant Chunks
              │
              ▼
          LLM Prompt
              │
              ▼
       Final AI Answer
```

---

## STEP 1 — Reading the PDF

### Code
```python
from pypdf import PdfReader

reader = PdfReader(pdf_path)
```

### What happens internally?

The PDF contains:
*   text
*   formatting
*   positions
*   images
*   metadata

The library extracts raw text from pages.

### Code
```python
text = []

for page in reader.pages:
    page_text = page.extract_text()
    text.append(page_text)
```

### Internal Thinking

Suppose the PDF contains:
> "Employees are entitled to 12 casual leaves annually. Unused leaves cannot be carried forward."

The extracted text becomes:
```python
[
 "Employees are entitled to 12 casual leaves annually.",
 "Unused leaves cannot be carried forward."
]
```
Then, it is joined into one large string.

### Why This Step Is Needed
*   LLMs cannot directly read PDF binary files.
*   We must:
    1. extract text
    2. clean text
    3. prepare text
    before AI processing.

### Real Industry Problem Solved
Companies store knowledge in:
*   PDFs
*   Word docs
*   policies
*   manuals

RAG converts them into searchable AI knowledge.

---

## STEP 2 — Chunking

### Code
```python
def chunk_text(text, chunk_size=500, overlap=100):
```

### Why Chunking Exists
LLMs have token limits. A 300-page PDF:
*   cannot fit into one prompt
*   becomes too expensive
*   slows retrieval

So we split it into smaller semantic blocks.

### Example

Original document:
*   **Page 1:** Leave policy
*   **Page 2:** Sick leave
*   **Page 3:** Attendance
*   **Page 4:** Holidays

After chunking:
```python
[
 "Leave policy ...",
 "Sick leave ...",
 "Attendance rules ...",
 "Holiday details ..."
]
```

### Code Logic

#### Splitting into words
```python
words = text.split()
```
*Example:*
`["Employees", "are", "entitled", "to", "12", "casual", "leaves"]`

#### Sliding Window Logic
```python
start = 0
end = start + chunk_size
```
This creates chunks like:
*   **Chunk 1** $\rightarrow$ words 0–500
*   **Chunk 2** $\rightarrow$ words 400–900

### Why Overlap Is Needed

Without overlap:
*   **Chunk 1:** `"Employees are entitled"`
*   **Chunk 2:** `"to 12 casual leaves"`

Meaning breaks! Overlap preserves semantic continuity.

### Industry Insight
Chunking strategy is one of the **MOST IMPORTANT** parts of RAG systems. Bad chunking leads to:
*   poor retrieval
*   hallucinations
*   irrelevant answers

---

## STEP 3 — Embeddings

This is the **MOST IMPORTANT** concept in RAG.

### What Is an Embedding?
*   Embedding converts text into numbers.
*   AI cannot understand raw text; it understands vectors.

### Example
Sentence:
> "Employee leave policy"

becomes a mathematical vector:
`[0.12, -0.55, 0.91, 0.44, ...]`

This vector captures semantic meaning.

### Embedding Code
```python
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
```
*This loads a pretrained embedding model.*

Then:
```python
embeddings = embed_model.encode(chunks)
```
Each chunk becomes a vector.

### Semantic Meaning
The AI learns:
$$\text{"leave policy"} \approx \text{"vacation rules"}$$
because their vectors become close in mathematical space.

### Visualization (Vector Space)
```text
     Sick Leave
         ●

Leave Policy ●

Vacation Rules ●
```
Similar meanings cluster together.

### Why Embeddings Matter
*   **Without embeddings:** keyword search only (poor semantic understanding).
*   **With embeddings:** meaning-based retrieval (intelligent search).

### Real Industry Usage
Embeddings power:
*   ChatGPT memory
*   recommendation systems
*   semantic search
*   enterprise AI assistants

---

## STEP 4 — FAISS Vector Database

### Code
```python
index = faiss.IndexFlatIP(dimension)
```

### What Is FAISS?
*   **FAISS** = Facebook AI Similarity Search.
*   It stores vectors efficiently.

### Why Normal Databases Fail
Traditional SQL databases search using queries like:
```sql
SELECT * FROM documents WHERE text LIKE '%leave%';
```
This is keyword matching. But semantic search requires:
*   vector mathematics
*   similarity calculations

### What FAISS Does
It stores:
$$\text{Chunk} \rightarrow \text{Vector}$$

Then performs:
*   nearest neighbor search
*   cosine similarity
*   semantic retrieval

### Vector Storage
```python
index.add(embeddings)
```
Now FAISS contains all knowledge vectors.

---

## STEP 5 — User Question Embedding

Suppose the user asks:
> "How many leaves are allowed?"

### Code
```python
query_embedding = embed_model.encode([query])
```
The question becomes a vector.

### IMPORTANT CONCEPT
Now, both items are in the same format:
*   **document chunks** = vectors
*   **question** = vector

AI compares vector similarity mathematically.

---

## STEP 6 — Similarity Search

### Code
```python
scores, indices = index.search(query_embedding, top_k)
```

### What Happens Internally
FAISS computes similarity:
$$\text{Question Vector} \quad \text{vs} \quad \text{Chunk Vectors}$$
using cosine similarity.

### Cosine Similarity
Measures the angle between vectors.

#### Formula
$$\cos(\theta) = \frac{A \cdot B}{\|A\| \|B\|}$$

#### Meaning
*   Closer angle $\rightarrow$ higher semantic similarity.

### Retrieval Example

Suppose we have these chunks:
*   **Chunk 1** $\rightarrow$ Leave policy
*   **Chunk 2** $\rightarrow$ Salary policy
*   **Chunk 3** $\rightarrow$ Attendance rules

For the question:
> "How many leaves?"

FAISS returns:
`[Chunk 1]`
because its semantic meaning is the closest.

---

## STEP 7 — Prompt Construction

Now the retrieved chunks are injected into the prompt.

### Code
```python
prompt = f"""
Context:
{context}

Question:
{question}
"""
```

### Why This Matters
This is the **“Retrieval-Augmented”** part. Instead of the LLM guessing, we provide actual document knowledge.

### Real Internal Prompt
```text
Context:
Employees are entitled to 12 casual leaves annually.

Question:
How many leaves are allowed?
```

---

## STEP 8 — LLM Generation

### Code
```python
generator(prompt)
```

The LLM:
1. reads the context
2. understands the question
3. generates a grounded answer

### Final Output
> "Employees are entitled to 12 casual leaves annually."

### WHY RAG IS POWERFUL
*   **Without RAG:** LLM may hallucinate.
*   **With RAG:** answers are grounded in documents.

---

## FULL INTERNAL ENGINEERING VIEW

```text
                 [ PDF ]
                    │
                    ▼
              Extract Text
                    │
                    ▼
               Chunk Text
                    │
                    ▼
       Convert Chunks → Embeddings
                    │
                    ▼
             Store in FAISS
                    │
                    ▼
              User Question
                    │
                    ▼
            Question Embedding
                    │
                    ▼
            Similarity Search
                    │
                    ▼
          Retrieve Best Chunks
                    │
                    ▼
     Send Context + Question to LLM
                    │
                    ▼
           Generate Final Answer
```

---

## Common Beginner Confusions

1. **“Why embeddings if we already have text?”**
   Because AI compares numbers mathematically, not raw language.

2. **“Why FAISS?”**
   Because vector search is computationally expensive. FAISS optimizes:
   *   nearest neighbor search
   *   high-dimensional vector retrieval

3. **“Why chunking?”**
   Because:
   *   LLM context windows are limited.
   *   Retrieval works better on smaller semantic units.

4. **“Why overlap?”**
   To preserve meaning between adjacent chunks.

5. **“Does FAISS understand language?”**
   No. The Embedding model understands language. FAISS only performs mathematical similarity search.

---

## REAL INDUSTRY ARCHITECTURE

Modern enterprise RAG systems use:

| Layer | Technologies |
| :--- | :--- |
| **Embeddings** | OpenAI / BGE / E5 |
| **Vector DB** | Pinecone / Weaviate / FAISS |
| **Orchestration** | LangChain / LlamaIndex |
| **LLM** | GPT / Claude / Llama |
| **Backend** | FastAPI |
| **Memory** | Redis |
| **UI** | React / Streamlit |

---

## Where This Is Used In Real Companies

*   **Enterprise AI Assistants:**
    *   HR assistants
    *   legal document search
    *   technical support bots
*   **Software Engineering:**
    *   codebase assistants
    *   architecture documentation AI
*   **Healthcare:**
    *   medical guideline retrieval
*   **Finance:**
    *   policy compliance assistants

---

## Common Production Problems

1. **Bad Chunking:** Causes irrelevant retrieval.
2. **Weak Embeddings:** Poor semantic understanding.
3. **Hallucinations:** LLM ignores context.
4. **Retrieval Failure:** Wrong chunks returned.
