---
name: memora
description: >
  Memora — A self-hosted RAG (Retrieval-Augmented Generation) personal knowledge base.
  Built with FastAPI + Qdrant + DashScope/OpenAI Embedding + DeepSeek/OpenAI LLM.
  Supports semantic vector search, AI-powered Q&A with source citations, hybrid retrieval (dense + BM42 sparse + rerank),
  and full document management (upload PDF/DOCX/TXT/MD, create, list, detail).
  Use when: user asks about stored documents, wants to search/upload/create documents, or needs AI-organized answers from their knowledge base.
  NOT for: general chat, real-time news, tasks unrelated to the knowledge base.
metadata:
  openclaw:
    requires:
      env:
        - KB_API_BASE
---

# Memora — Personal Knowledge Base (RAG)

A self-hosted **Retrieval-Augmented Generation (RAG)** personal knowledge base that lets your AI assistant search, query, and manage your private documents.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Vector Database**: Qdrant (dense + sparse vectors)
- **Embedding**: DashScope `text-embedding-v4` / OpenAI compatible
- **LLM**: DeepSeek / OpenAI compatible
- **Retrieval**: Hybrid search (dense vectors + BM42 sparse vectors + Qwen3 Rerank)
- **Metadata Store**: MySQL
- **Skill Client**: Zero-dependency Python (stdlib only — `urllib`, `json`)

## Features

- **Semantic Search** — Find documents by meaning using vector similarity, not just keywords
- **AI-Powered Q&A** — Ask a question, get an LLM-generated answer grounded in your documents with source citations
- **Hybrid Retrieval** — Dense embedding + BM42 sparse vectors + reranking for optimal recall and precision
- **Document Upload** — Ingest PDF, DOCX, TXT, and Markdown files with automatic chunking and vectorization
- **Document Creation** — Create text documents directly from the agent
- **Document Management** — List, view details, and organize your knowledge base

## When to Run

- User asks a question that may be answered by stored documents
- User wants to search the knowledge base
- User wants to list documents or view document details
- User wants to upload a file or create a new document
- User needs AI-organized answers on a topic from their personal knowledge

## Workflow

### Upload a File

1. Get the file path and title from the user
2. Run:
   ```
   python scripts/kb_api.py upload "{absolute_file_path}" "{document_title}"
   ```
3. Supported formats: `.txt` `.pdf` `.docx` `.md`
4. Returns upload result with `document_id`

### Create a Text Document

1. Get the title and text content from the user
2. Run:
   ```
   python scripts/kb_api.py create "{title}" "{content}"
   ```
3. Returns creation result with `document_id`

### Search with AI Answer (RAG)

1. Extract the user's query
2. Run:
   ```
   python scripts/kb_api.py search_answer "{query}"
   ```
3. Parse the returned JSON: extract `answer` and source documents from `sources`
4. Present the answer with source citations

### Search Documents Only

1. Extract the user's search keywords
2. Run:
   ```
   python scripts/kb_api.py search "{keywords}"
   ```
3. Parse and display the ranked search results

### List All Documents

1. Run:
   ```
   python scripts/kb_api.py list
   ```
2. Display the document list

### View Document Details

1. Get the document ID
2. Run:
   ```
   python scripts/kb_api.py detail "{document_id}"
   ```
3. Display the document content

## Output Format

### Upload / Create:
Document "{title}" has been added to the knowledge base (ID: {document_id})

### Search with AI Answer:
**Knowledge Base Query Result**

{AI-generated answer based on retrieved documents}

**Sources:**
- {document_title} (relevance: {score})

### List Documents:
**Documents** ({n} total)
1. {title} — {created_at}
2. ...

## Configuration

Set the environment variable `KB_API_BASE` to point to the Memora backend.
Default: `http://127.0.0.1:8080`

Source code & setup guide: https://github.com/zzlzzlzzl15/Memora
