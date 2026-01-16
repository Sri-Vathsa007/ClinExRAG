# ClinExRAG 🩺  
### Explainable Clinical Decision Support using Retrieval-Augmented Generation

ClinExRAG is a **Clinical Decision Support (CDS) Explainer** that helps clinicians make **safe, guideline-based decisions** by retrieving official clinical guidelines and **explaining recommendations with evidence-backed citations**.

This project demonstrates how **Retrieval-Augmented Generation (RAG)** can be applied responsibly in healthcare by combining:
- deterministic safety guardrails
- official medical guidelines
- transparent, auditable LLM outputs

---

## 🚩 Problem Statement

Clinical guidelines (e.g., NICE, CDC, WHO) are:
- lengthy and complex
- frequently updated
- difficult to reference during real-time clinical workflows

Traditional LLMs are **not safe** for clinical use because they can:
- hallucinate medical facts
- rely on outdated knowledge
- fail to cite authoritative sources

**ClinExRAG solves this by grounding every response in retrieved guideline evidence and refusing to answer when unsafe.**

---

## 🎯 What This Project Does

ClinExRAG provides **decision support and explanation**, not diagnosis.

For a given patient context, it:
1. Retrieves relevant sections from official clinical guidelines
2. Explains whether a recommendation applies
3. Highlights contraindications and red flags
4. Identifies missing critical information
5. Cites exact guideline passages used

---

## 🧪 MVP Clinical Scope

**Domain:**  
Uncomplicated lower urinary tract infection (cystitis)

**Evidence Source:**  
NICE Guideline NG109 (visual summary)

**Why this scope?**
- Narrow, well-defined clinical rules
- Clear escalation criteria
- Widely used in real-world CDS systems

---

## 🧠 System Architecture

```text
Clinical Guidelines (PDF/HTML)
        ↓
Parse & Clean
        ↓
Chunk into Sections
        ↓
OpenAI Embeddings
        ↓
FAISS Vector Index
──────────────────────────
Patient Context + Question
        ↓
Safety Guardrails (Rules)
        ↓
Relevant Guideline Retrieval
        ↓
LLM Explanation with Citations
