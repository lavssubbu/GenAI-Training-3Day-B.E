# We will build a Python RAG app that does this:
- Read a PDF
- Split it into chunks
- Convert chunks into embeddings
- Store embeddings in FAISS
- Retrieve the best chunks for a question
- Send retrieved text + question to an LLM
- Return the final answer

---

## 2) Install packages
```bash
pip install pypdf sentence-transformers faiss-cpu numpy transformers torch
```

---

## 3) Folder structure
```text
rag_project/
│
├── data/
│   └── employee_leave_policy.pdf
│
└── app.py
```

---

## 4) Full Python code
```python
import os
import numpy as np
import faiss
import torch
torch.set_num_threads(1)
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


PDF_PATH = "data/Employee-Handbook.pdf"


def load_pdf_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)
    result = "\n".join(text)
    print(result)
    return result


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    print("================================")
    print(chunks)
    return chunks


def build_faiss_index(chunks, embed_model):
    embeddings = embed_model.encode(chunks, convert_to_numpy=True)

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    return index, embeddings


def retrieve_chunks(query, chunks, index, embed_model, top_k=3):
    query_embedding = embed_model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(query_embedding, top_k)

    results = []
    for i in indices[0]:
        if i != -1:
            results.append(chunks[i])

    print("================================")
    print(results)
    return results


def answer_question(question, retrieved_chunks, generator):
    tokenizer, model = generator
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are a helpful assistant.
Answer the question using only the context below.
If the answer is not in the context, say you do not know.

Context:
{context}

Question:
{question}

Answer:
"""

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=150, do_sample=False)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def main():
    if not os.path.exists(PDF_PATH):
        print(f"PDF not found at: {PDF_PATH}")
        return

    print("Loading PDF...")
    text = load_pdf_text(PDF_PATH)

    print("Chunking text...")
    chunks = chunk_text(text, chunk_size=250, overlap=50)

    print(f"Created {len(chunks)} chunks.")

    print("Loading embedding model...")
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Building FAISS index...")
    index, _ = build_faiss_index(chunks, embed_model)

    print("Loading generation model...")
    # You can replace this model with any local or hosted LLM later
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    generator = (tokenizer, model)

    try:
        while True:
            question = input("\nAsk a question (type 'exit' to stop): ").strip()
            if question.lower() == "exit":
                break

            relevant_chunks = retrieve_chunks(question, chunks, index, embed_model, top_k=3)
            answer = answer_question(question, relevant_chunks, generator)

            print("\nAnswer:")
            print(answer)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting...")


if __name__ == "__main__":
    main()
```

---

## 5) Code-Wise Step-by-Step Explanation

Following the RAG architecture outlined in the RAG System [README.md](file:///Users/harinikesh/Downloads/Project/gen-ai-notebook/day4_beyond_llm/RAG_system/README.md), let's trace how the Python code implements each of the **6 core steps** of RAG:

---

### Step 1 — Load Documents (`load_pdf_text`)
*   **The Code:**
    ```python
    def load_pdf_text(pdf_path: str) -> str:
        reader = PdfReader(pdf_path)
        ...
        result = "\n".join(text)
        print(result)
        return result
    ```
*   **High-Level Explanation:** Opens and reads the local PDF file (`Employee-Handbook.pdf`) page-by-page using the `pypdf` library. It extracts raw text from each page, combines them using newlines, prints it for visual verification, and returns the full aggregated document string.

---

### Step 2 — Chunking (`chunk_text`)
*   **The Code:**
    ```python
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
        ...
        print("================================")
        print(chunks)
        return chunks
    ```
*   **High-Level Explanation:** Splits the raw aggregated text into manageable, smaller segments of words (chunks).
    *   `chunk_size = 250` words ensures each piece stays well within the LLM's context window.
    *   `overlap = 50` words acts as a sliding window buffer, ensuring sentences are not awkwardly split at hard boundaries and context is preserved between consecutive chunks.

---

### Step 3 — Generate Embeddings (`SentenceTransformer`)
*   **The Code:**
    ```python
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embed_model.encode(chunks, convert_to_numpy=True)
    ```
*   **High-Level Explanation:** Converts our textual document chunks into dense mathematical vectors (embeddings) using the `all-MiniLM-L6-v2` transformer model. Each embedding captures the semantic meaning of its chunk, allowing the system to understand *concepts* rather than just keyword matches.

---

### Step 4 — Store in FAISS (`build_faiss_index`)
*   **The Code:**
    ```python
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    ```
*   **High-Level Explanation:** Stores the generated vectors into an in-memory vector database using FAISS (Facebook AI Similarity Search). Before indexing, we perform L2 normalization to convert standard distance search into Cosine Similarity matching. The `IndexFlatIP` (Flat Inner Product) index allows exact brute-force similarity lookup.

---

### Step 5 — Query Retrieval (`retrieve_chunks`)
*   **The Code:**
    ```python
    def retrieve_chunks(query, chunks, index, embed_model, top_k=3):
        query_embedding = embed_model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        scores, indices = index.search(query_embedding, top_k)
        ...
        print("================================")
        print(results)
        return results
    ```
*   **High-Level Explanation:** When a user enters a query:
    1.  The query is converted into an embedding using the same `SentenceTransformer`.
    2.  `index.search()` does a vector search in FAISS to find the top `top_k` (3) most semantically similar chunks.
    3.  The raw text contents of these matching chunks are retrieved and displayed on the terminal.

---

### Step 6 — LLM Generation (`answer_question` & Flan-T5)
*   **The Code:**
    ```python
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    ...
    outputs = model.generate(**inputs, max_new_tokens=150, do_sample=False)
    ```
*   **High-Level Explanation:** Combines the retrieved context chunks and the user's question into a strict instruction template (Prompt). This prompt is sent to `google/flan-t5-base` (loaded locally with tokenizer/model). The local sequence-to-sequence model performs autoregressive token generation to draft a grounded response using *only* the retrieved context, eliminating hallucinations.

---

### 🛠️ The macOS Threading Fix & Interactive Loop
*   **Environment Workaround:** On macOS environments running Python 3.13, PyTorch's OpenMP backend can segfault when deserializing large weight files. Adding `torch.set_num_threads(1)` limits loading to a single stable thread, avoiding this conflict completely.
*   **Interactive Input Loop:** A simple CLI `while True` loop keeps the application active for multiple questions. Wrapping the input in a `try...except (EOFError, KeyboardInterrupt)` block gracefully handles program interrupts (e.g. `Ctrl+C` or piped EOF) by printing `Exiting...` rather than raising a long, intimidating python stack trace.

---


## 6) Example of a good test document

Create a PDF with sections like:
1. Leave Policy
2. Casual Leave Rules
3. Sick Leave Rules
4. Holiday Policy
5. Attendance Rules
6. Leave Approval Process

That will make it very easy to test retrieval.

---

## 7) Example questions to test
- What is the leave approval process?
- How many sick leaves are allowed?
- Can leave be carried forward?
- What happens if I am absent without notice?

---

## 8) When this setup is enough

This is good for:
- learning RAG
- small PDFs
- proof of concept
- internal demos

For bigger systems later, you can add:
- better chunking
- metadata
- reranking
- chat memory
- Streamlit UI
- FastAPI backend
- multiple PDFs

I can turn this into a Streamlit chatbot app next, using the same PDF example.

---

## Get me an example PDF from internet to download

Here are some excellent PDFs you can directly download and use for your first RAG project:

### Recommended PDF (Best for Beginners)
**Employee Handbook PDF**

This is the best one to start with because:
- structured sections
- policies and FAQs
- easy retrieval testing
- realistic enterprise use case

#### Download Link
- **Employee Handbook PDF**

*Source overview:* contains employment basics, policies, conduct rules, leave information, and company procedures.

### Alternative PDFs

#### HR Policy PDF
*Good for:*
- policy retrieval
- leave rules
- compliance chatbot

- **HR Policy PDF**

#### Sample Employee Handbook Template
*Good for:*
- multi-section retrieval
- chunking experiments
- metadata filtering

- **Sample Employee Handbook Template PDF**

### Questions You Can Test in Your RAG

After downloading the PDF, try queries like:
- What is the leave approval process?
- What happens during probation?
- How are holidays handled?
- What is the attendance policy?
- Can employees work remotely?
