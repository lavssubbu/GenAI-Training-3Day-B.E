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
