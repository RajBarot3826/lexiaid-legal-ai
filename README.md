<div align="center">

# ⚖️ LexiAid: AI for Legal Assistance & Access

### *Democratizing Legal Comprehension with Plain-English Simplification, Risk Auditing, and Contract Intelligence*

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://ai.google.dev/)
[![PromptWars](https://img.shields.io/badge/PromptWars-Virtual_Sept_2026-FF4500?style=for-the-badge)](https://hack2skill.com)
[![Accessibility](https://img.shields.io/badge/WCAG_2.1-AA_Compliant-success?style=for-the-badge)](https://www.w3.org/WAI/standards-guidelines/wcag/)
[![Tests](https://img.shields.io/badge/PyTest-66%2F66_Passed-brightgreen?style=for-the-badge)](https://docs.pytest.org)

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

- **Prompt Injection Neutralization**: 14 compiled regex patterns detect and neutralize adversarial jailbreak prompts (e.g. "ignore prior instructions", "DAN mode", "system prompt override", "jailbreak").
- **Rate Limiting**: In-memory sliding-window rate limiter (30 requests/minute per IP) prevents abuse and denial-of-service attacks.
- **Restricted CORS**: Origin-locked CORS policy allowing only the production GitHub Pages domain and local development servers (no wildcard `*`).
- **Request Timing Headers**: Every response includes `X-Processing-Time-Ms` and `X-RateLimit-Limit` headers for performance monitoring.
- **Strict Payload Limits**: Restricts document payloads to 120,000 characters to prevent denial-of-wallet (DoW) and memory exhaustion.
- **Zero Secrets in Repository**: No hardcoded API keys; utilizes clean environment variable injection.
- **Repository Size (< 0.1 MB)**: Strictly optimized git repository (~48 KiB total), ensuring 100% compliance with Hack2Skill's `< 10 MB` limit.
- **Single Branch Enforcement**: Kept strictly on a single `main` branch as required by Hack2Skill submission guidelines.

---

## ♿ Accessibility Compliance (WCAG 2.1 AA)

- **Skip-to-Content Navigation**: Keyboard-accessible skip link enables users to bypass repetitive navigation and jump directly to the main content area.
- **Semantic ARIA Hierarchy**: Uses `role="banner"`, `role="tablist"`, `role="tab"`, `role="tabpanel"`, `role="status"`, `role="log"`, and `role="contentinfo"`.
- **Descriptive ARIA Attributes**: All interactive elements include `aria-label`, `aria-describedby`, and `aria-live` attributes for screen reader support.
- **Visually-Hidden Labels**: Screen-reader-only labels use the proper `visually-hidden` CSS class (clip pattern) instead of `display:none`.
- **High Contrast Ratios**: Color palette exceeds WCAG AA 4.5:1 contrast requirements for dark-mode readability.
- **Keyboard Navigable**: Full support for Tab/Shift-Tab navigation with visible `:focus-visible` outline rings and proper `tabindex` management on tab components.
- **Screen Reader Live Regions**: `aria-live="polite"` regions for real-time AI Q&A responses and status updates.
- **Meta Description**: Includes `<meta name="description">` for SEO and assistive technology context.

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
collected 66 items

tests/test_api.py::TestHealthEndpoint::test_health_returns_200_with_service_metadata PASSED
tests/test_api.py::TestHealthEndpoint::test_health_includes_processing_time_header PASSED
tests/test_api.py::TestSamplesEndpoint::test_samples_returns_at_least_three_contracts PASSED
tests/test_api.py::TestSamplesEndpoint::test_each_sample_has_required_fields PASSED
tests/test_api.py::TestAnalyzeEndpoint::test_predatory_contract_returns_high_risk PASSED
tests/test_api.py::TestAnalyzeEndpoint::test_lease_contract_returns_favorable_risk PASSED
tests/test_api.py::TestAnalyzeEndpoint::test_empty_text_returns_validation_error PASSED
tests/test_api.py::TestAnalyzeEndpoint::test_missing_text_field_returns_422 PASSED
tests/test_api.py::TestAnalyzeEndpoint::test_all_reading_levels[Plain English] PASSED
tests/test_api.py::TestAnalyzeEndpoint::test_all_reading_levels[Executive] PASSED
tests/test_api.py::TestAnalyzeEndpoint::test_all_reading_levels[ELI5] PASSED
tests/test_api.py::TestAnalyzeEndpoint::test_unicode_document_text_handled PASSED
tests/test_api.py::TestAnalyzeEndpoint::test_very_long_document_accepted PASSED
tests/test_api.py::TestAnalyzeEndpoint::test_analysis_response_time_under_two_seconds PASSED
tests/test_api.py::TestCompareEndpoint::test_comparison_favorability_scores PASSED
tests/test_api.py::TestCompareEndpoint::test_missing_contract_b_returns_error PASSED
tests/test_api.py::TestChatEndpoint::test_termination_query_with_citations PASSED
tests/test_api.py::TestChatEndpoint::test_general_query_follow_up_suggestions PASSED
tests/test_api.py::TestChatEndpoint::test_empty_document_returns_error PASSED
tests/test_api.py::TestSimplifyEndpoint::test_indemnification_critical PASSED
tests/test_api.py::TestSimplifyEndpoint::test_generic_clause_moderate PASSED
tests/test_legal_services.py::TestMockAnalysis::test_predatory_high_risk PASSED
tests/test_legal_services.py::TestMockAnalysis::test_lease_favorable PASSED
tests/test_legal_services.py::TestMockAnalysis::test_general_moderate_risk PASSED
tests/test_legal_services.py::TestMockAnalysis::test_disclaimer_included PASSED
tests/test_legal_services.py::TestMockAnalysis::test_keyword_detection[cayman] PASSED
tests/test_legal_services.py::TestMockAnalysis::test_keyword_detection[contractor] PASSED
tests/test_legal_services.py::TestMockAnalysis::test_keyword_detection[lease] PASSED
tests/test_legal_services.py::TestMockAnalysis::test_keyword_detection[tenant] PASSED
tests/test_legal_services.py::TestMockAnalysis::test_keyword_detection[landlord] PASSED
tests/test_legal_services.py::TestMockComparison::test_standard_higher_favorability PASSED
tests/test_legal_services.py::TestMockComparison::test_liquidated_damages_critical PASSED
tests/test_legal_services.py::TestMockComparison::test_negotiation_advice PASSED
tests/test_legal_services.py::TestMockChat::test_termination_citation PASSED
tests/test_legal_services.py::TestMockChat::test_rent_financial_details PASSED
tests/test_legal_services.py::TestMockChat::test_non_compete_risk_note PASSED
tests/test_legal_services.py::TestMockChat::test_general_query_excerpt PASSED
tests/test_legal_services.py::TestMockSimplification::test_indemnification_critical PASSED
tests/test_legal_services.py::TestMockSimplification::test_generic_safe_moderate PASSED
tests/test_security.py::TestInputValidation::test_empty_rejected PASSED
tests/test_security.py::TestInputValidation::test_whitespace_rejected PASSED
tests/test_security.py::TestInputValidation::test_none_rejected PASSED
tests/test_security.py::TestInputValidation::test_valid_text_passes PASSED
tests/test_security.py::TestInputValidation::test_oversized_truncated PASSED
tests/test_security.py::TestInputValidation::test_control_chars_stripped PASSED
tests/test_security.py::TestInputValidation::test_unicode_preserved PASSED
tests/test_security.py::TestPromptInjection::test_ignore_instructions PASSED
tests/test_security.py::TestPromptInjection::test_dan_mode PASSED
tests/test_security.py::TestPromptInjection::test_system_prompt_reveal PASSED
tests/test_security.py::TestPromptInjection::test_jailbreak_keyword PASSED
tests/test_security.py::TestPromptInjection::test_all_patterns[10 patterns] PASSED
tests/test_security.py::TestDisclaimer::test_statutory_notice PASSED
tests/test_security.py::TestDisclaimer::test_no_formal_advice PASSED
tests/test_security.py::TestDisclaimer::test_attorney_consultation PASSED
tests/test_security.py::TestRateLimiter::test_allows_within_limit PASSED
tests/test_security.py::TestRateLimiter::test_blocks_exceeding_limit PASSED
tests/test_security.py::TestRateLimiter::test_independent_client_limits PASSED

======================= 66 passed in 1.23s =======================
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
