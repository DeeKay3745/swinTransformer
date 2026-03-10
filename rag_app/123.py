import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from pypdf import PdfReader

# -----------------------------
# CONFIG
# -----------------------------

DATA_FOLDER = "Researchpaper"
INDEX_FILE = "vector_db.faiss"
CHUNK_SIZE = 200
TOP_K = 5

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# -----------------------------
# LOAD EMBEDDING MODEL
# -----------------------------

print("Loading embedding model...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# TEXT CHUNKING
# -----------------------------

def chunk_text(text, chunk_size=200):

    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


# -----------------------------
# LOAD TXT FILE
# -----------------------------

def load_txt(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# -----------------------------
# LOAD PDF FILE
# -----------------------------

def load_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# -----------------------------
# LOAD ALL DOCUMENTS
# -----------------------------

def load_documents(folder):

    documents = []

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        if file.endswith(".txt"):

            text = load_txt(path)

        elif file.endswith(".pdf"):

            text = load_pdf(path)

        else:
            continue

        documents.append({
            "text": text,
            "source": file
        })

    return documents


# -----------------------------
# BUILD CHUNKS
# -----------------------------

def build_chunks(documents):

    chunks = []

    for doc in documents:

        text_chunks = chunk_text(doc["text"], CHUNK_SIZE)

        for chunk in text_chunks:

            chunks.append({
                "text": chunk,
                "source": doc["source"]
            })

    return chunks


# -----------------------------
# BUILD VECTOR INDEX
# -----------------------------

def build_index(chunks):

    texts = [c["text"] for c in chunks]

    print("Generating embeddings...")

    embeddings = embed_model.encode(
        texts,
        show_progress_bar=True
    )

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)

    print("Vector index saved.")

    return index


# -----------------------------
# RETRIEVE DOCUMENTS
# -----------------------------

def retrieve(query, chunks, index):

    query_embedding = embed_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, TOP_K)

    results = []

    for i in indices[0]:

        results.append(chunks[i])

    return results


# -----------------------------
# ASK GPT
# -----------------------------

def ask_gpt(query, retrieved):

    context = ""

    for r in retrieved:

        context += f"\nSource: {r['source']}\n{r['text']}\n"

    prompt = f"""
You are a research assistant.

Use ONLY the context below to answer.

{context}

Question:
{query}

Provide a clear answer and cite sources.
"""

    response = client.chat.completions.create(

        model="gpt-4o",

        messages=[
            {"role": "user", "content": prompt}
        ]

    )

    return response.choices[0].message.content


# -----------------------------
# MAIN PIPELINE
# -----------------------------

print("Loading research papers...")

documents = load_documents(DATA_FOLDER)

print("Total documents:", len(documents))

print("Creating chunks...")

chunks = build_chunks(documents)

print("Total chunks:", len(chunks))


# -----------------------------
# LOAD OR BUILD INDEX
# -----------------------------

if os.path.exists(INDEX_FILE):

    print("Loading FAISS index...")

    index = faiss.read_index(INDEX_FILE)

else:

    print("Building FAISS index...")

    index = build_index(chunks)


# -----------------------------
# QUERY LOOP
# -----------------------------

print("\nResearch RAG system ready.\n")

while True:

    query = input("Ask question (or type exit): ")

    if query.lower() in ["exit", "quit"]:
        break

    retrieved = retrieve(query, chunks, index)

    print("\nRetrieved Sources:")

    for r in retrieved:
        print("-", r["source"])

    answer = ask_gpt(query, retrieved)

    print("\nAnswer:\n")
    print(answer)

    print("\n---------------------------------\n")