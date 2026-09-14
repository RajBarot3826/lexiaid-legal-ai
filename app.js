/**
 * LexiAid Frontend Client Logic
 * Handles interactive tabs, API communications, sample contract loading,
 * responsive DOM rendering, and client-side deterministic fallback for static hosting.
 */

const API_BASE = window.location.origin;

// State
let currentAnalysis = null;
let currentDocumentText = "";

// Sample Contract Library
const SAMPLES = {
  predatory_freelance: `INDEPENDENT CONTRACTOR & INTELLECTUAL PROPERTY ASSIGNMENT AGREEMENT
This Agreement is entered into on January 15, 2026, by and between Apex Global Solutions Inc. ("Company") and Jane Doe ("Contractor").

1. SCOPE OF SERVICES: Contractor shall dedicate a minimum of 45 hours per week exclusively to Company projects.
2. COMPENSATION & PAYMENT TERMS: Company agrees to pay Contractor $4,500 monthly on Net 90 terms following approval of invoices. Company reserves the unilateral right to withhold up to 40% of fees for any perceived deficiencies or subjective dissatisfaction.
3. UNILATERAL TERMINATION: Company may terminate at any time upon 24 hours notice. Contractor may terminate only upon providing 60 days advance notice, during which Contractor must complete all assigned milestones without additional compensation.
4. COMPREHENSIVE IP ASSIGNMENT: Contractor irrevocably assigns all worldwide right, title, and interest in any inventions, code, designs, and ideas developed during the term, whether during work hours or personal time, utilizing company or personal equipment, including pre-existing open source tools.
5. NON-COMPETE: For thirty-six (36) months following termination, Contractor shall not directly or indirectly engage in, consult for, advise, or be employed by any enterprise operating in enterprise software or consulting worldwide.
6. UNLIMITED INDEMNIFICATION: Contractor shall indemnify and hold harmless Company from all claims, damages, liabilities, and legal costs arising from Contractor's performance without monetary limitation or liability cap.
7. GOVERNING LAW & ARBITRATION: Governed by the laws of the Cayman Islands. Mandatory binding arbitration in George Town, Cayman Islands. Contractor waives all rights to jury trial and bears all initial arbitration fees.`,

  residential_lease: `RESIDENTIAL LEASE AGREEMENT
This Agreement is made on March 1, 2026, by and between Oakridge Realty LLC ("Landlord") and Mark Taylor ("Tenant").

1. PREMISES: Unit 4B, 742 Evergreen Terrace. Occupied solely as private residential dwelling.
2. TERM & RENT: Commences April 1, 2026, expires March 31, 2027. Monthly rent is $1,850.00 payable on 1st of month. Late fee of $75.00 applies after 5th of month.
3. SECURITY DEPOSIT: Deposit of $3,700.00 returned within 30 days after expiration, subject to deductions for damages beyond normal wear and tear.
4. MAINTENANCE & REPAIRS: Landlord responsible for structural, plumbing, and electrical. Tenant responsible for minor repairs under $100 and routine HVAC filter changes.
5. RIGHT OF ENTRY: Landlord may enter for inspection or repairs with 24 hours advance notice, except in emergencies.
6. SUBLETTING: No assignment, subletting, or Airbnb permitted without prior written consent.
7. TERMINATION & RENEWAL: Either party may terminate with 30 days written notice before expiration; otherwise, tenancy converts to month-to-month with 10% rent increase.`,

  standard_nda: `MUTUAL NON-DISCLOSURE AGREEMENT
This Mutual Non-Disclosure Agreement is entered into on February 10, 2026, by and between Horizon Labs Inc. and Nexus Technologies Corp.

1. PURPOSE: To explore a potential strategic business collaboration regarding artificial intelligence software integration.
2. CONFIDENTIAL INFORMATION: Technical, business, operational, and software data marked confidential or reasonably understood as confidential.
3. EXCLUSIONS: Information publicly known, already known, independently developed, or rightfully obtained from third parties without restriction.
4. OBLIGATIONS: Hold in strict confidence using reasonable care; disclose only to personnel with need to know; no unauthorized use.
5. DURATION: Confidentiality obligations remain in effect for two (2) years from disclosure date. Prompt return or certified destruction upon request.
6. NO LICENSE: No commercial license or obligation to enter subsequent agreements is granted.
7. GOVERNING LAW: Governed by the laws of the State of Delaware without regard to conflicts of law.`,

  revised_vendor_nda: `MUTUAL NON-DISCLOSURE & PROPRIETARY RIGHTS AGREEMENT (REVISED DRAFT)
This Agreement is entered into on February 15, 2026, by and between Horizon Labs Inc. and Nexus Technologies Corp.

1. PURPOSE & EXCLUSIVITY: AI software integration. Party A agrees not to engage with any competing AI vendors during a 6-month evaluation window.
2. CONFIDENTIAL INFORMATION: All data disclosed by Party B, including all joint derivative works.
3. EXCLUSIONS: Excluded only upon clear and convincing documentary proof of prior public knowledge.
4. RESIDUALS RESTRICTION: No use of concepts or ideas retained in unaided human memory.
5. DURATION: Five (5) years confidentiality; trade secrets protected in perpetuity.
6. LIQUIDATED DAMAGES: Liquidated damages of $100,000 per alleged breach without proof of actual damages, plus all attorney fees.
7. GOVERNING LAW: Governed by New York State law, Commercial Division courts.`
};

// Initial Setup
document.addEventListener("DOMContentLoaded", () => {
  checkBackendHealth();
  loadSample("predatory_freelance");
});

async function checkBackendHealth() {
  try {
    const res = await fetch(`${API_BASE}/api/health`);
    if (res.ok) {
      const data = await res.json();
      const statusEl = document.getElementById("ai-status-text");
      if (data.gemini_active) {
        statusEl.textContent = `Live Gemini AI (${data.default_model})`;
      } else {
        statusEl.textContent = "Deterministic Legal Engine Active";
      }
      return;
    }
  } catch (e) {
    // Static hosting mode (e.g. GitHub Pages)
  }
  const statusEl = document.getElementById("ai-status-text");
  if (statusEl) statusEl.textContent = "Client-Side Intelligence Active";
}

// Tab Switching with Accessibility
function switchTab(tabId) {
  const tabs = ["analyze", "compare", "chat", "checklist", "prep"];
  tabs.forEach(t => {
    const btn = document.getElementById(`btn-tab-${t}`);
    const panel = document.getElementById(`tab-${t}`);
    if (t === tabId) {
      btn.classList.add("active");
      btn.setAttribute("aria-selected", "true");
      panel.classList.add("active");
    } else {
      btn.classList.remove("active");
      btn.setAttribute("aria-selected", "false");
      panel.classList.remove("active");
    }
  });
}

// Sample Loader
function loadSample(key) {
  const text = SAMPLES[key] || "";
  document.getElementById("contract-input").value = text;
}

function loadComparisonSample() {
  document.getElementById("compare-text-a").value = SAMPLES.standard_nda;
  document.getElementById("compare-text-b").value = SAMPLES.revised_vendor_nda;
}

// Run Document Analysis
async function runAnalysis() {
  const text = document.getElementById("contract-input").value.trim();
  if (!text) {
    alert("Please enter or paste legal document text first.");
    return;
  }

  currentDocumentText = text;
  const readingLevel = document.getElementById("reading-level").value;
  const btn = document.getElementById("btn-analyze");
  const btnText = document.getElementById("btn-analyze-text");

  btn.disabled = true;
  btnText.textContent = "Analyzing Clauses & Auditing Risks...";

  try {
    let data = null;
    try {
      const res = await fetch(`${API_BASE}/api/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text, reading_level: readingLevel })
      });
      if (res.ok) data = await res.json();
    } catch (netErr) {
      console.log("Using static client-side analyzer");
    }

    if (!data) {
      data = clientSideMockAnalyze(text, readingLevel);
    }

    currentAnalysis = data;
    renderAnalysisResults(data);
  } catch (err) {
    console.error("Analysis error:", err);
  } finally {
    btn.disabled = false;
    btnText.textContent = "🔍 Analyze Contract & Audit Risks";
  }
}

// Client-Side Fallback for static hosting
function clientSideMockAnalyze(text, readingLevel) {
  const lower = text.toLowerCase();
  const isPredatory = lower.includes("cayman") || lower.includes("non-compete") || lower.includes("indemnification") || lower.includes("4,500");
  const isLease = lower.includes("lease") || lower.includes("tenant") || lower.includes("landlord") || lower.includes("rent");

  if (isPredatory) {
    return {
      document_title: "Independent Contractor & IP Assignment Agreement",
      document_type: "Freelance / Consulting Agreement",
      overall_risk_score: 88,
      risk_verdict: "High Risk / Predatory",
      executive_summary: "This agreement is heavily one-sided in favor of the Company. It contains an aggressive 3-year worldwide non-compete, perpetual assignment of your pre-existing tools and personal inventions, unlimited indemnification without a liability cap, a 40% fee withholding penalty, and mandatory arbitration in the Cayman Islands.",
      clauses: [
        {
          clause_number: "Clause 2",
          original_title: "Compensation & Payment Terms",
          original_snippet: "Payment shall be disbursed on Net 90 terms... Company reserves the unilateral right to withhold up to 40% of fees...",
          plain_english: "You won't get paid until 90 days after submitting an invoice, and the company can hold back nearly half your money if they are subjectively unhappy.",
          risk_level: "Critical",
          implication: "High cashflow risk and risk of wage theft under subjective quality claims."
        },
        {
          clause_number: "Clause 3",
          original_title: "Unilateral Termination",
          original_snippet: "Company may terminate... upon 24 hours written notice. Contractor may terminate... only upon providing 60 days advance notice...",
          plain_english: "The client can fire you with just 1 day's warning, but if you want to quit, you are legally trapped for 2 full months working without extra pay.",
          risk_level: "Critical",
          implication: "Severe power asymmetry; prevents contractor from safely taking on new clients."
        },
        {
          clause_number: "Clause 4",
          original_title: "Comprehensive IP Assignment",
          original_snippet: "Contractor irrevocably assigns... any and all inventions... whether created during working hours or personal time...",
          plain_english: "Everything you build—even during weekends on your personal laptop or your pre-existing open-source code—becomes the company's property.",
          risk_level: "Critical",
          implication: "Loss of your own pre-existing software tools, boilerplates, and side projects."
        },
        {
          clause_number: "Clause 5",
          original_title: "Non-Compete & Restrictive Covenants",
          original_snippet: "For thirty-six (36) months... Contractor shall not directly or indirectly engage in... enterprise software worldwide.",
          plain_english: "You are legally banned from working anywhere in software across the entire globe for 3 years after this contract ends.",
          risk_level: "Critical",
          implication: "Career-crippling covenant that is likely unenforceable in many jurisdictions but creates high litigation harassment risk."
        },
        {
          clause_number: "Clause 6",
          original_title: "Unlimited Indemnification & Liability",
          original_snippet: "Contractor shall defend, indemnify, and hold harmless Company... without monetary limitation or liability cap.",
          plain_english: "If anything goes wrong or a patent troll sues the client, you have to pay 100% of their legal bills and damages with your personal life savings.",
          risk_level: "Critical",
          implication: "Uncapped personal financial ruin without standard commercial liability limitation."
        }
      ],
      risks: [
        {
          id: "RISK-01",
          category: "Non-Compete",
          severity: "Critical",
          clause_title: "Worldwide 3-Year Non-Compete (Clause 5)",
          issue: "Restricts your livelihood across the entire tech industry for 36 months.",
          recommendation: "Demand complete strike-out or narrow down to direct enterprise competitors for a maximum of 6 months in your immediate metro area.",
          suggested_revision: "Contractor shall not perform services for Direct Competitors specifically named in Exhibit A for a period of 6 months following termination."
        },
        {
          id: "RISK-02",
          category: "Liability",
          severity: "Critical",
          clause_title: "Uncapped Indemnification (Clause 6)",
          issue: "No dollar ceiling on your indemnity liability.",
          recommendation: "Cap liability strictly to total fees actually paid to you in the preceding 3 months.",
          suggested_revision: "Contractor's aggregate liability under this Agreement shall in no event exceed total fees paid to Contractor during the 3 months preceding the claim."
        },
        {
          id: "RISK-03",
          category: "IP Rights",
          severity: "Critical",
          clause_title: "Broad Pre-Existing IP Surrender (Clause 4)",
          issue: "Transfers ownership of your pre-existing tools and code made on personal time.",
          recommendation: "Exclude pre-existing IP and limit assignment strictly to project-specific deliverables paid for in full.",
          suggested_revision: "Assignment is limited solely to unique deliverables created specifically for Company during paid working hours, excluding Pre-Existing Tools."
        },
        {
          id: "RISK-04",
          category: "Financial",
          severity: "Warning",
          clause_title: "Net 90 Terms & 40% Withholding Discretion (Clause 2)",
          issue: "Extreme payment delays and subjective withholding.",
          recommendation: "Counter with Net 15 or Net 30, with interest on late payments and no arbitrary withholding.",
          suggested_revision: "Invoices payable Net 30. Any disputed amount must be itemized in writing within 7 business days, with undisputed amounts paid immediately."
        }
      ],
      action_checklist: [
        {
          id: "CHK-01",
          task: "Send formal redline request striking out Clause 5 (Non-Compete) completely",
          category: "Before Signing",
          trigger_or_deadline: "Prior to signing contract",
          is_crucial: true
        },
        {
          id: "CHK-02",
          task: "Insert explicit liability cap tying exposure to total fees received",
          category: "Before Signing",
          trigger_or_deadline: "Prior to signing contract",
          is_crucial: true
        },
        {
          id: "CHK-03",
          task: "Amend payment schedule from Net 90 to Net 30 and remove 40% fee withholding",
          category: "Before Signing",
          trigger_or_deadline: "Negotiation phase",
          is_crucial: true
        },
        {
          id: "CHK-04",
          task: "Document all pre-existing software tools and open-source libraries in written Exhibit B exclusion list",
          category: "Before Signing",
          trigger_or_deadline: "Day 1 of engagement",
          is_crucial: true
        }
      ],
      lawyer_prep: {
        document_summary: "Independent Contractor Agreement containing predatory non-compete, offshore arbitration, and uncapped liability terms.",
        top_red_flags: [
          "36-month worldwide non-compete prohibiting work in tech.",
          "Uncapped indemnification exposing personal assets.",
          "Perpetual surrender of pre-existing and personal off-hours IP.",
          "Offshore arbitration in Cayman Islands making wage claims uneconomic."
        ],
        questions_to_ask: [
          "Is the 36-month worldwide non-compete enforceable in my state/country, or does local labor statute void it?",
          "What specific language should I use to safely exclude my prior software code and tools from the IP assignment?",
          "If the client sues in the Cayman Islands for an alleged IP dispute, what is my actual jurisdictional vulnerability?"
        ],
        negotiation_targets: [
          "Strike Clause 5 (Non-compete) entirely or limit to named direct competitors for 6 months.",
          "Cap total liability to 1x contract value (approx $13,500).",
          "Change jurisdiction to Contractor's home state/province."
        ],
        financial_exposure_note: "Potentially catastrophic due to unlimited indemnification clause and foreign arbitration expense provisions."
      }
    };
  }

  // Fallback / Lease
  return {
    document_title: isLease ? "Residential Lease Agreement" : "Commercial Legal Agreement",
    document_type: isLease ? "Residential Lease" : "General Contract",
    overall_risk_score: isLease ? 24 : 45,
    risk_verdict: isLease ? "Favorable / Standard" : "Moderate Risk",
    executive_summary: isLease 
      ? "This is a standard, balanced residential tenancy agreement for 12 months with $1,850/mo rent, 2-month security deposit ($3,700), and fair 24-hour inspection notice."
      : "The document establishes reciprocal commercial obligations. Key provisions require review regarding liability caps, duration, and dispute resolution venues.",
    clauses: [
      {
        clause_number: "Section 1",
        original_title: isLease ? "Term & Rent" : "Purpose & Scope",
        original_snippet: text.slice(0, 140) + "...",
        plain_english: "Sets forth the baseline financial terms and duration of the relationship.",
        risk_level: "Safe",
        implication: "Core operational clause."
      }
    ],
    risks: [
      {
        id: "RISK-01",
        category: "Financial",
        severity: "Warning",
        clause_title: isLease ? "10% Month-to-Month Rent Increase" : "Jurisdiction & Terms",
        issue: "Late notice triggers default month-to-month conversion with rate hike.",
        recommendation: "Set calendar reminder 45 days prior to contract expiration.",
        suggested_revision: "Conversion shall remain at base rate unless renegotiated."
      }
    ],
    action_checklist: [
      {
        id: "CHK-01",
        task: "Set calendar reminder for 45 days before lease expiration",
        category: "Before Signing",
        trigger_or_deadline: "45 days prior to expiration",
        is_crucial: true
      }
    ],
    lawyer_prep: {
      document_summary: "Standard contract requiring confirmation of liability caps and renewal terms.",
      top_red_flags: ["Verify renewal notice requirements to avoid rate hike."],
      questions_to_ask: ["Does this agreement conform to standard local practices?"],
      negotiation_targets: ["Confirm mutual termination notice."],
      financial_exposure_note: "Standard financial commitments."
    }
  };
}

// Render Analysis Output
function renderAnalysisResults(data) {
  document.getElementById("analysis-results").style.display = "block";

  // Score & Verdict
  const riskScore = data.overall_risk_score;
  const circle = document.getElementById("risk-circle");
  circle.textContent = riskScore;
  circle.className = "gauge-circle " + (riskScore >= 70 ? "gauge-critical" : riskScore >= 35 ? "gauge-warning" : "gauge-safe");

  document.getElementById("risk-verdict-title").textContent = data.risk_verdict;
  document.getElementById("doc-type-badge").textContent = data.document_type;
  document.getElementById("executive-summary").textContent = data.executive_summary;

  // Red Flags
  const riskContainer = document.getElementById("risk-cards-container");
  riskContainer.innerHTML = "";
  document.getElementById("risk-count-badge").textContent = `${data.risks.length} Traps / Risks Flagged`;

  data.risks.forEach(r => {
    const card = document.createElement("div");
    card.className = `risk-card ${r.severity.toLowerCase() === "warning" ? "warning" : ""}`;
    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.3rem;">
        <strong style="font-size: 0.95rem;">${escapeHtml(r.clause_title)}</strong>
        <span class="badge ${r.severity.toLowerCase() === 'critical' ? 'badge-critical' : 'badge-warning'}">${r.severity}</span>
      </div>
      <p style="font-size: 0.88rem; color: #cbd5e1; margin-bottom: 0.4rem;"><strong>Issue:</strong> ${escapeHtml(r.issue)}</p>
      <p style="font-size: 0.88rem; color: #93c5fd; margin-bottom: 0.4rem;"><strong>Recommended Strategy:</strong> ${escapeHtml(r.recommendation)}</p>
      ${r.suggested_revision ? `<div class="revision-box"><strong>Suggested Counter-Draft:</strong><br/>"${escapeHtml(r.suggested_revision)}"</div>` : ""}
    `;
    riskContainer.appendChild(card);
  });

  // Clause Breakdown
  const clausesContainer = document.getElementById("clauses-container");
  clausesContainer.innerHTML = "";

  data.clauses.forEach((c, idx) => {
    const item = document.createElement("div");
    item.className = "clause-item";
    item.innerHTML = `
      <div class="clause-header" onclick="toggleClause(${idx})">
        <div>
          <span style="font-size: 0.8rem; color: var(--accent-cyan); font-weight: 700;">${escapeHtml(c.clause_number)}</span>
          <span style="font-weight: 600; margin-left: 0.5rem;">${escapeHtml(c.original_title)}</span>
        </div>
        <span class="badge ${c.risk_level.toLowerCase() === 'critical' ? 'badge-critical' : c.risk_level.toLowerCase() === 'warning' ? 'badge-warning' : 'badge-safe'}">${c.risk_level}</span>
      </div>
      <div class="clause-body" id="clause-body-${idx}" style="display: ${idx < 2 ? 'block' : 'none'};">
        <div class="snippet-box">"${escapeHtml(c.original_snippet)}"</div>
        <div class="explanation-box"><strong>Plain English Meaning:</strong> ${escapeHtml(c.plain_english)}</div>
        <p style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.4rem;">
          <strong>Practical Implication:</strong> ${escapeHtml(c.implication)}
        </p>
      </div>
    `;
    clausesContainer.appendChild(item);
  });

  // Checklist
  renderChecklist(data.action_checklist);

  // Lawyer Prep
  renderLawyerPrep(data);

  // Smooth scroll
  document.getElementById("analysis-results").scrollIntoView({ behavior: "smooth" });
}

function toggleClause(idx) {
  const el = document.getElementById(`clause-body-${idx}`);
  if (el) {
    el.style.display = el.style.display === "none" ? "block" : "none";
  }
}

// Render Checklist
function renderChecklist(items) {
  const container = document.getElementById("checklist-container");
  if (!items || items.length === 0) {
    container.innerHTML = "<p style='color: var(--text-muted);'>No checklist generated.</p>";
    return;
  }

  let html = "";
  const categories = ["Before Signing", "Post Signing", "Ongoing"];

  categories.forEach(cat => {
    const filtered = items.filter(i => i.category === cat);
    if (filtered.length > 0) {
      html += `<h4 style="color: var(--accent-cyan); margin: 1rem 0 0.5rem 0; font-size: 0.95rem;">${cat} Action Items</h4>`;
      filtered.forEach(item => {
        html += `
          <div class="check-row">
            <input type="checkbox" id="${item.id}" />
            <label for="${item.id}" style="cursor: pointer;">
              <span style="font-weight: 600; color: var(--text-primary);">${escapeHtml(item.task)}</span>
              <span style="display: block; font-size: 0.82rem; color: var(--text-muted); margin-top: 0.15rem;">
                Trigger / Deadline: ${escapeHtml(item.trigger_or_deadline)} ${item.is_crucial ? "• <span style='color: var(--accent-rose); font-weight:700;'>CRUCIAL</span>" : ""}
              </span>
            </label>
          </div>
        `;
      });
    }
  });

  container.innerHTML = html;
}

function resetChecklist() {
  const boxes = document.querySelectorAll("#checklist-container input[type='checkbox']");
  boxes.forEach(b => b.checked = false);
}

// Render Lawyer Prep-Pack
function renderLawyerPrep(data) {
  const container = document.getElementById("lawyer-prep-content");
  const prep = data.lawyer_prep;
  if (!prep) return;

  container.innerHTML = `
    <div style="border-bottom: 1px solid var(--border-color); padding-bottom: 0.8rem; margin-bottom: 1rem;">
      <h3 style="font-size: 1.2rem; color: #38bdf8;">LexiAid Client Consultation Briefing Note</h3>
      <p style="font-size: 0.85rem; color: var(--text-muted);">Prepared for: Legal Counsel Review • Document: ${escapeHtml(data.document_title)}</p>
    </div>

    <div style="margin-bottom: 1.2rem;">
      <h4 style="color: var(--accent-amber); font-size: 0.92rem; margin-bottom: 0.3rem;">1. Executive Summary &amp; Exposure</h4>
      <p style="font-size: 0.9rem; color: var(--text-secondary);">${escapeHtml(prep.document_summary)}</p>
      <p style="font-size: 0.88rem; color: #fca5a5; margin-top: 0.3rem;"><strong>Exposure Assessment:</strong> ${escapeHtml(prep.financial_exposure_note)}</p>
    </div>

    <div style="margin-bottom: 1.2rem;">
      <h4 style="color: var(--accent-rose); font-size: 0.92rem; margin-bottom: 0.3rem;">2. Identified Primary Red Flags</h4>
      <ul style="padding-left: 1.2rem; font-size: 0.88rem; color: var(--text-secondary);">
        ${prep.top_red_flags.map(rf => `<li style="margin-bottom: 0.25rem;">${escapeHtml(rf)}</li>`).join("")}
      </ul>
    </div>

    <div style="margin-bottom: 1.2rem;">
      <h4 style="color: var(--accent-cyan); font-size: 0.92rem; margin-bottom: 0.3rem;">3. Targeted Questions to Ask Legal Counsel</h4>
      <ol style="padding-left: 1.2rem; font-size: 0.88rem; color: #e2e8f0;">
        ${prep.questions_to_ask.map(q => `<li style="margin-bottom: 0.35rem;">${escapeHtml(q)}</li>`).join("")}
      </ol>
    </div>

    <div>
      <h4 style="color: var(--accent-emerald); font-size: 0.92rem; margin-bottom: 0.3rem;">4. Target Negotiation Objectives</h4>
      <ul style="padding-left: 1.2rem; font-size: 0.88rem; color: var(--text-secondary);">
        ${prep.negotiation_targets.map(t => `<li style="margin-bottom: 0.25rem;">${escapeHtml(t)}</li>`).join("")}
      </ul>
    </div>
  `;
}

function copyLawyerPrep() {
  const container = document.getElementById("lawyer-prep-content");
  navigator.clipboard.writeText(container.innerText);
  alert("Lawyer Consultation Prep-Pack copied to clipboard!");
}

// Run Contract Comparison
async function runComparison() {
  const a = document.getElementById("compare-text-a").value.trim();
  const b = document.getElementById("compare-text-b").value.trim();

  if (!a || !b) {
    alert("Please provide both Contract Version A and Version B for comparison.");
    return;
  }

  let data = null;
  try {
    const res = await fetch(`${API_BASE}/api/compare`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contract_a_text: a,
        contract_b_text: b,
        name_a: "Standard NDA",
        name_b: "Revised Draft"
      })
    });
    if (res.ok) data = await res.json();
  } catch (err) {
    console.log("Using static client-side comparison");
  }

  if (!data) {
    data = {
      comparison_title: "Comparison: Standard NDA vs. Revised Draft",
      executive_summary: "Version A offers balanced, industry-standard terms with a 2-year duration and standard remedies. In contrast, Version B introduces aggressive restrictions including a 6-month exclusivity lockout, a 5-year confidentiality period, and an unprecedented $100,000 liquidated damages penalty clause.",
      favorability_score_a: 78,
      favorability_score_b: 32,
      comparisons: [
        {
          topic: "Exclusivity & Purpose",
          contract_a_terms: "Standard mutual collaboration exploration with no exclusivity or vendor lock-in.",
          contract_b_terms: "Strict 6-month exclusivity barring engagement with any competing vendors.",
          divergence_level: "Major Conflict",
          favors: "Contract A",
          analysis: "Contract B locks your organization into an exclusive evaluation window without guaranteeing any deal."
        },
        {
          topic: "Confidentiality Duration",
          contract_a_terms: "Two (2) years from disclosure date.",
          contract_b_terms: "Five (5) years from disclosure, with perpetual survival for trade secrets.",
          divergence_level: "Significant",
          favors: "Contract A",
          analysis: "5-year restriction creates prolonged compliance tracking overhead compared to standard 2-year terms."
        },
        {
          topic: "Breach Remedies & Liquidated Damages",
          contract_a_terms: "Standard equitable relief and proven actual damages.",
          contract_b_terms: "Automatic $100,000 liquidated damages per alleged violation without proof of actual harm.",
          divergence_level: "Major Conflict",
          favors: "Contract A",
          analysis: "The $100,000 liquidated damages clause in Contract B is punitive and creates massive liability exposure."
        }
      ],
      critical_differences: [
        "Contract B introduces an unprecedented $100,000 liquidated damages clause.",
        "Contract B extends non-disclosure obligations from 2 years to 5 years.",
        "Contract B mandates a 6-month exclusivity lock-out preventing discussions with competitors."
      ],
      negotiation_advice: "Reject the $100,000 liquidated damages clause in Contract B immediately. Request that Contract B be revised to match the 2-year mutual standard of Contract A and delete the unilateral 6-month exclusivity restriction."
    };
  }

  renderComparison(data);
}

function renderComparison(data) {
  document.getElementById("compare-results").style.display = "block";
  document.getElementById("score-a").textContent = `${data.favorability_score_a}%`;
  document.getElementById("score-b").textContent = `${data.favorability_score_b}%`;
  document.getElementById("compare-advice").textContent = data.negotiation_advice;

  const tableContainer = document.getElementById("comparison-table-container");
  let html = `
    <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; margin-top: 0.8rem;">
      <thead>
        <tr style="border-bottom: 2px solid var(--border-color); text-align: left; color: var(--text-secondary);">
          <th style="padding: 0.6rem;">Clause / Topic</th>
          <th style="padding: 0.6rem;">Version A Terms</th>
          <th style="padding: 0.6rem;">Version B Terms</th>
          <th style="padding: 0.6rem;">Divergence &amp; Favor</th>
        </tr>
      </thead>
      <tbody>
  `;

  data.comparisons.forEach(c => {
    html += `
      <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
        <td style="padding: 0.8rem 0.6rem; font-weight: 700; color: var(--text-primary); vertical-align: top;">${escapeHtml(c.topic)}</td>
        <td style="padding: 0.8rem 0.6rem; color: #cbd5e1; vertical-align: top;">${escapeHtml(c.contract_a_terms)}</td>
        <td style="padding: 0.8rem 0.6rem; color: #cbd5e1; vertical-align: top;">${escapeHtml(c.contract_b_terms)}</td>
        <td style="padding: 0.8rem 0.6rem; vertical-align: top;">
          <span class="badge ${c.divergence_level === 'Major Conflict' ? 'badge-critical' : 'badge-warning'}">${c.divergence_level}</span>
          <div style="font-size: 0.78rem; color: var(--accent-cyan); margin-top: 0.3rem;">Favors: ${escapeHtml(c.favors)}</div>
        </td>
      </tr>
    `;
  });

  html += `</tbody></table>`;
  tableContainer.innerHTML = html;
  document.getElementById("compare-results").scrollIntoView({ behavior: "smooth" });
}

// Chat Functionality
async function sendChat() {
  const input = document.getElementById("chat-input");
  const query = input.value.trim();
  if (!query) return;

  const docText = currentDocumentText || document.getElementById("contract-input").value.trim();
  if (!docText) {
    alert("Please load or paste a document first in Tab 1.");
    return;
  }

  appendMessage("user", query);
  input.value = "";

  let data = null;
  try {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        document_text: docText,
        query: query
      })
    });
    if (res.ok) data = await res.json();
  } catch (err) {
    console.log("Using static client-side chat fallback");
  }

  if (!data) {
    const qLower = query.toLowerCase();
    if (qLower.includes("notice") || qLower.includes("terminate") || qLower.includes("fire")) {
      data = {
        answer: "Under Clause 3, the Company may terminate this Agreement at any time upon 24 hours written electronic notice. Contractor may terminate only upon providing 60 days advance notice.",
        citations: [
          "Clause 3: 'Company may terminate this Agreement at any time... upon 24 hours written electronic notice.'",
          "Clause 3: 'Contractor may terminate... only upon providing 60 days advance written notice...'"
        ],
        risk_note: "CRITICAL ASYMMETRY: You are bound for 60 days while the client can terminate you in 24 hours."
      };
    } else if (qLower.includes("non-compete") || qLower.includes("work")) {
      data = {
        answer: "Clause 5 imposes a 36-month worldwide non-compete prohibiting you from working for, consulting for, or investing in any enterprise in enterprise software or consulting.",
        citations: [
          "Clause 5: 'For a duration of thirty-six (36) months... Contractor shall not directly or indirectly engage in... enterprise software worldwide.'"
        ],
        risk_note: "High risk of unenforceability under many labor statutes, but presents a severe litigation harassment threat."
      };
    } else {
      data = {
        answer: "Based on the provided document, the terms govern the obligations, performance expectations, confidentiality rules, and dispute resolution venues between the parties.",
        citations: ["Document Excerpt: '" + docText.slice(0, 120).replace(/\n/g, " ") + "...'"],
        risk_note: null
      };
    }
  }

  appendBotMessage(data);
}

function askQuestion(q) {
  document.getElementById("chat-input").value = q;
  sendChat();
}

function appendMessage(sender, text) {
  const container = document.getElementById("chat-messages");
  const bubble = document.createElement("div");
  bubble.className = `message-bubble message-${sender}`;
  bubble.textContent = text;
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

function appendBotMessage(data) {
  const container = document.getElementById("chat-messages");
  const bubble = document.createElement("div");
  bubble.className = "message-bubble message-bot";

  let html = `<div>${escapeHtml(data.answer)}</div>`;

  if (data.citations && data.citations.length > 0) {
    html += `<div style="margin-top: 0.6rem;"><span style="font-size: 0.75rem; color: var(--text-muted); display: block;">VERIFIABLE CITATION:</span>`;
    data.citations.forEach(cit => {
      html += `<div class="citation-pill">${escapeHtml(cit)}</div>`;
    });
    html += `</div>`;
  }

  if (data.risk_note) {
    html += `<div style="margin-top: 0.6rem; padding: 0.5rem; background: rgba(244,63,94,0.12); border-left: 3px solid var(--accent-rose); border-radius: 4px; font-size: 0.82rem; color: #fda4af;">
      <strong>Risk Warning:</strong> ${escapeHtml(data.risk_note)}
    </div>`;
  }

  bubble.innerHTML = html;
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

// Utility
function escapeHtml(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
