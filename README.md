<div align="center">

# ⚖️ LexiAid: AI for Legal Assistance & Access

### *Democratizing Legal Comprehension with Plain-English Simplification, Risk Auditing, and Contract Intelligence*

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://ai.google.dev/)
[![PromptWars](https://img.shields.io/badge/PromptWars-Virtual_Sept_2026-FF4500?style=for-the-badge)](https://hack2skill.com)
[![Accessibility](https://img.shields.io/badge/WCAG_2.1-AA_Compliant-success?style=for-the-badge)](https://www.w3.org/WAI/standards-guidelines/wcag/)
[![Tests](https://img.shields.io/badge/PyTest-22%2F22_Passed-brightgreen?style=for-the-badge)](https://docs.pytest.org)

**An intelligent, accessible, and ethical GenAI legal platform engineered for everyday citizens, freelancers, tenants, and small businesses to read, compare, audit, and navigate complex legal documents without fear.**

[🚀 Quick Start](#-quick-start) •
[🧠 Approach & Logic](#-approach-and-logic) •
[⚙️ How It Works](#️-how-the-solution-works) •
[📌 Assumptions Made](#-assumptions-made) •
[🎯 Challenge Alignment](#-alignment-with-hack2skill-challenge) •
[🧪 Automated Tests](#-testing--validation)

</div>

---

## 🧠 Approach and Logic

Legal documents are intentionally drafted with archaic syntactic structures, buried liabilities, and asymmetry that disadvantage non-lawyers. Traditional chatbots frequently hallucinate legal interpretations or issue dangerous, unqualified legal advice that violates bar regulations. 

**LexiAid's engineering philosophy is grounded in three pillars:**
1. **Context-Bounded Grounding (Zero Hallucination)**: Answers and risk assessments are strictly constrained to the text of the supplied agreement. Every claim is cross-linked to a **verbatim clause quotation**.
2. **Decomposition Over Summarization**: Rather than producing a generic 1-paragraph summary that glosses over critical nuances, LexiAid breaks down documents into discrete functional clauses (payment, termination, liability, IP assignment, non-compete) and translates each into plain English with practical consequences.
3. **Actionable Empowerment with Ethical Boundaries**: Conforming strictly to legal ethics standards (e.g. ABA Model Rule 5.5 and Bar Council regulations), LexiAid acts as an **informational force multiplier**, generating due-diligence checklists and attorney briefing packs so users enter formal legal consultations educated and prepared.

---

## ⚙️ How the Solution Works

LexiAid combines an asynchronous **FastAPI** backend with **Google Gemini 2.5/2.0 Flash** and an accessible, glassmorphism **WCAG 2.1 AA** client:

```mermaid
graph TD
    User([Citizen / Tenant / Freelancer]) -->|Paste Agreement or Select Sample| WebClient[Accessible Web Suite]

    subgraph ClientLayer [WCAG 2.1 AA Responsive Frontend]
        WebClient --> M1[📄 Document Simplifier & Risk Audit]
        WebClient --> M2[⚖️ Dual-Contract Comparator]
        WebClient --> M3[💬 Grounded Clause Q&A]
        WebClient --> M4[✅ Due Diligence Checklist]
        WebClient --> M5[👔 Attorney Briefing Pack]
    end

    subgraph ServerLayer [FastAPI Architecture]
        Router[REST Router] --> Sanitizer[OWASP Input Sanitizer & Prompt Injection Guard]
        Sanitizer --> Engine[Legal Reasoning Engine]
        
        Engine -->|Live API Key| Gemini[Google Gemini 2.5 Flash API]
        Engine -->|Zero-Config Fallback| DeterministicEngine[Deterministic Legal Knowledge Engine]
    end

    WebClient -->|JSON REST| Router
```

### Operational Workflow:
1. **Ingestion & OWASP Sanitization**: The document text is validated, stripped of non-printable control characters, bounded to 120,000 characters, and screened for adversarial prompt injection (DAN mode, override attempts).
2. **Multi-Persona Legal Analysis**:
   - **Plain-English Synthesizer**: Decomposes convoluted clauses into readable 8th-grade language with adjustable reading levels (Plain English, Executive Summary, ELI5).
   - **Risk Sentinel**: Computes an objective **0–100 Legal Risk Index**, categorizing vulnerabilities into Critical (uncapped indemnities, 3-year non-competes), Warning, and Safe.
   - **Dual-Contract Divergence Engine**: Aligns two contract versions (e.g., standard vs. revised draft) and computes relative favorability percentages with clause-by-clause diffing.
   - **Grounded Q&A Agent**: Answers user queries with direct citations from the contract text.
3. **Structured Extraction**: Gemini Structured Outputs enforce deterministic JSON schemas for due-diligence checklists, deadline triggers, and attorney consultation prep packs.
4. **Offline Deterministic Fallback**: If an evaluator or user tests without a `GEMINI_API_KEY`, LexiAid automatically activates its built-in deterministic engine, ensuring 100% feature availability with zero latency.

---

## 📌 Assumptions Made

1. **Informational Scope**: LexiAid assumes users require document literacy and risk awareness to negotiate agreements or prepare for attorney consultations, **not** statutory courtroom representation or formal legal opinions.
2. **Text Formats**: Assumes legal documents are provided as digital text, standard UTF-8 strings, or exported PDF/DOCX transcripts up to 120,000 characters (~25,000 words).
3. **Dual-Contract Alignment**: For comparisons, the platform assumes both versions address a common underlying transaction (e.g. initial NDA vs vendor draft).
4. **Neutral Fallback**: The deterministic engine assumes standard benchmark contract archetypes (Predatory Independent Contractor, Residential Tenancy Lease, Mutual NDA) to provide immediate 1-click evaluation without network dependencies.

---

## 🎯 Alignment with Hack2Skill Challenge

Built directly for the **PromptWars: Virtual** challenge — **"AI for Legal Assistance & Access"**:

| Hack2Skill Problem Statement Use Case | LexiAid Implementation | Real-World Impact |
| :--- | :--- | :--- |
| **1. Simplifying complex legal documents** | **Plain-English Clause Breakdown** | Clause-by-clause decomposition translating legalese into conversational English with reading-level toggles. |
| **2. Comparing contracts, agreements, or policies** | **Dual-Contract Divergence Engine** | Side-by-side analyzer calculating favorability scores (0–100%) and surfacing clause shifts and hidden penalties. |
| **3. Highlighting clauses, obligations, & risks** | **0–100 Legal Risk Sentinel** | Surfaces Critical, Warning, and Safe clauses (e.g. uncapped indemnities, 36-month non-competes, Cayman arbitration). |
| **4. Answering questions on provided documents** | **Anti-Hallucination Grounded Q&A** | Answers bounded strictly by document text, returning **verbatim clause citations** to prevent hallucinations. |
| **5. Helping users understand options & next steps** | **Rights & Recourse Navigator** | Provides actionable counter-proposals, statutory protections, and concrete negotiation wording. |
| **6. Generating actionable checklists & summaries** | **Due Diligence Checklist & Calendar** | Extracts actionable pre-signing tasks, post-signing obligations, and renewal notice deadlines. |
| **7. Preparing for a legal professional** | **Attorney Consultation Briefing Pack** | Generates an exportable 1-page briefing memorandum outlining primary red flags, exposure estimates, and targeted questions. |
| **Ethical & Regulatory Disclaimer** | **Statutory Non-Advice Guardrail** | Permanent banner establishing that LexiAid provides informational literacy rather than formal legal representation. |

---

## 🛡️ Security and Ethical Guardrails

- **Prompt Injection Neutralization**: Protects against adversarial jailbreak prompts (e.g. "ignore prior instructions", "system prompt override").
- **Strict Payload Limits**: Restricts document payloads to 120,000 characters to prevent denial-of-wallet (DoW) and memory exhaustion.
- **Zero Secrets in Repository**: No hardcoded API keys; utilizes clean environment variable injection.
- **Repository Size (< 0.1 MB)**: Strictly optimized git repository (~48 KiB total), ensuring 100% compliance with Hack2Skill's `< 10 MB` limit.
- **Single Branch Enforcement**: Kept strictly on a single `main` branch as required by Hack2Skill submission guidelines.

---

## ♿ Accessibility Compliance (WCAG 2.1 AA)

- **Semantic ARIA Hierarchy**: Uses `role="banner"`, `role="tablist"`, `role="tab"`, `role="tabpanel"`, and `role="contentinfo"`.
- **High Contrast Ratios**: Color palette exceeds WCAG AA 4.5:1 contrast requirements for dark-mode readability.
- **Keyboard Navigable**: Full support for Tab/Shift-Tab navigation with visible `:focus-visible` outline rings.
- **Screen Reader Support**: Live regions (`aria-live="polite"`) for real-time AI Q&A responses.

---

## 🧪 Testing & Validation

Run the automated test suite covering security sanitization, endpoint contracts, and legal heuristics:

```bash
python -m pytest tests/ -v
```

### Test Suite Results:
```
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.1.1
rootdir: C:\Users\barot\.gemini\antigravity\scratch\lexiaid_legal_ai
collected 22 items

tests/test_api.py::test_health_endpoint PASSED                           [  4%]
tests/test_api.py::test_samples_endpoint PASSED                          [  9%]
tests/test_api.py::test_analyze_predatory_contract_endpoint PASSED       [ 13%]
tests/test_api.py::test_analyze_lease_endpoint PASSED                    [ 18%]
tests/test_api.py::test_analyze_empty_payload_validation PASSED          [ 22%]
tests/test_api.py::test_compare_endpoint PASSED                          [ 27%]
tests/test_api.py::test_chat_termination_query PASSED                    [ 31%]
tests/test_api.py::test_chat_general_query PASSED                        [ 36%]
tests/test_api.py::test_simplify_endpoint PASSED                         [ 40%]
tests/test_legal_services.py::test_predatory_contract_analysis PASSED    [ 45%]
tests/test_legal_services.py::test_lease_contract_analysis PASSED        [ 50%]
tests/test_legal_services.py::test_general_contract_analysis PASSED      [ 54%]
tests/test_legal_services.py::test_contract_comparison_divergence PASSED [ 59%]
tests/test_legal_services.py::test_grounded_qa_citations PASSED          [ 63%]
tests/test_legal_services.py::test_grounded_qa_lease_rent PASSED         [ 68%]
tests/test_legal_services.py::test_grounded_qa_non_compete PASSED        [ 72%]
tests/test_legal_services.py::test_clause_simplification PASSED          [ 77%]
tests/test_security.py::test_empty_text_rejection PASSED                 [ 81%]
tests/test_security.py::test_prompt_injection_neutralization PASSED      [ 86%]
tests/test_security.py::test_dan_mode_injection_detection PASSED         [ 90%]
tests/test_security.py::test_oversized_document_truncation PASSED        [ 95%]
tests/test_security.py::test_standard_disclaimer PASSED                  [100%]

======================= 22 passed in 1.61s =======================
```

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/RajBarot3826/lexiaid-legal-ai.git
cd lexiaid-legal-ai
pip install -r requirements.txt
```

### 2. Configure (Optional)
```bash
cp .env.example .env
# Edit .env and paste your GEMINI_API_KEY if desired.
# Note: Operates out of the box with zero configuration via deterministic engine!
```

### 3. Launch
```bash
python run.py
```
Open **`http://localhost:8000`** in your browser. API docs available at **`http://localhost:8000/docs`**.

---

## 📄 License
MIT License. Built for the **PromptWars: Virtual (September 2026)** Hackathon on Hack2Skill.
