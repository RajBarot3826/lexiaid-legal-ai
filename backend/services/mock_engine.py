"""Deterministic mock analysis engine for offline legal document processing.

Provides high-fidelity legal analysis responses without requiring an API key,
using keyword-based document classification and curated response templates
for predatory freelance agreements, residential leases, and general contracts.
"""

import re
from typing import Dict, Any, List
from ..models.schemas import (
    AnalyzeResponse, ClauseExplanation, RiskItem, ChecklistItem, LawyerPrep,
    CompareResponse, ClauseComparison, ChatResponse, SimplifyResponse
)
from ..utils.security import get_standard_disclaimer

def get_mock_analysis(text: str, reading_level: str = "Plain English") -> AnalyzeResponse:
    lower = text.lower()
    disclaimer = get_standard_disclaimer()

    # Detect Predatory Freelance
    if "cayman islands" in lower or "independent contractor" in lower or "non-compete" in lower and "36" in lower:
        return AnalyzeResponse(
            document_title="Independent Contractor & IP Assignment Agreement",
            document_type="Freelance / Consulting Agreement",
            overall_risk_score=88,
            risk_verdict="High Risk / Predatory",
            executive_summary=(
                "This agreement is heavily one-sided in favor of the Company. It contains an aggressive 3-year worldwide "
                "non-compete, perpetual assignment of your pre-existing tools and personal inventions, unlimited indemnification "
                "without a liability cap, a 40% fee withholding penalty, and mandatory arbitration in the Cayman Islands."
            ),
            clauses=[
                ClauseExplanation(
                    clause_number="Clause 2",
                    original_title="Compensation & Payment Terms",
                    original_snippet="Payment shall be disbursed on Net 90 terms... Company reserves the unilateral right to withhold up to 40% of fees...",
                    plain_english="You won't get paid until 90 days after submitting an invoice, and the company can hold back nearly half your money if they are subjectively unhappy.",
                    risk_level="Critical",
                    implication="High cashflow risk and risk of wage theft under subjective quality claims."
                ),
                ClauseExplanation(
                    clause_number="Clause 3",
                    original_title="Unilateral Termination",
                    original_snippet="Company may terminate... upon 24 hours written notice. Contractor may terminate... only upon providing 60 days advance written notice...",
                    plain_english="The client can fire you with just 1 day's warning, but if you want to quit, you are legally trapped for 2 full months working without extra pay.",
                    risk_level="Critical",
                    implication="Severe power asymmetry; prevents contractor from safely taking on new clients."
                ),
                ClauseExplanation(
                    clause_number="Clause 4",
                    original_title="Comprehensive IP Assignment",
                    original_snippet="Contractor irrevocably assigns... any and all inventions... whether created during working hours or personal time...",
                    plain_english="Everything you build—even during weekends on your personal laptop or your pre-existing open-source code—becomes the company's property.",
                    risk_level="Critical",
                    implication="Loss of your own pre-existing software tools, boilerplates, and side projects."
                ),
                ClauseExplanation(
                    clause_number="Clause 5",
                    original_title="Non-Compete & Restrictive Covenants",
                    original_snippet="For a duration of thirty-six (36) months... Contractor shall not directly or indirectly engage in... enterprise software worldwide.",
                    plain_english="You are legally banned from working anywhere in software across the entire globe for 3 years after this contract ends.",
                    risk_level="Critical",
                    implication="Career-crippling covenant that is likely unenforceable in many jurisdictions but creates high litigation harassment risk."
                ),
                ClauseExplanation(
                    clause_number="Clause 6",
                    original_title="Unlimited Indemnification & Liability",
                    original_snippet="Contractor shall defend, indemnify, and hold harmless Company... without monetary limitation or liability cap.",
                    plain_english="If anything goes wrong or a patent troll sues the client, you have to pay 100% of their legal bills and damages with your personal life savings.",
                    risk_level="Critical",
                    implication="Uncapped personal financial ruin without standard commercial liability limitation."
                ),
                ClauseExplanation(
                    clause_number="Clause 7",
                    original_title="Governing Law & Mandatory Arbitration",
                    original_snippet="...governed by the laws of the Cayman Islands. Any dispute... resolved through binding arbitration in George Town...",
                    plain_english="If the client refuses to pay you, you can only sue them by flying to the Cayman Islands and paying thousands of dollars in offshore arbitration fees.",
                    risk_level="Warning",
                    implication="Deliberate jurisdictional hurdle designed to make enforcing unpaid wages impossible."
                ),
            ],
            risks=[
                RiskItem(
                    id="RISK-01",
                    category="Non-Compete",
                    severity="Critical",
                    clause_title="Worldwide 3-Year Non-Compete (Clause 5)",
                    issue="Restricts your livelihood across the entire tech industry for 36 months.",
                    recommendation="Demand complete strike-out or narrow down to direct enterprise competitors for a maximum of 6 months in your immediate metro area.",
                    suggested_revision="Contractor shall not perform services for Direct Competitors specifically named in Exhibit A for a period of 6 months following termination."
                ),
                RiskItem(
                    id="RISK-02",
                    category="Liability",
                    severity="Critical",
                    clause_title="Uncapped Indemnification (Clause 6)",
                    issue="No dollar ceiling on your indemnity liability.",
                    recommendation="Cap liability strictly to total fees actually paid to you in the preceding 3 months.",
                    suggested_revision="Contractor's aggregate liability under this Agreement shall in no event exceed total fees paid to Contractor during the 3 months preceding the claim."
                ),
                RiskItem(
                    id="RISK-03",
                    category="IP Rights",
                    severity="Critical",
                    clause_title="Broad Pre-Existing IP Surrender (Clause 4)",
                    issue="Transfers ownership of your pre-existing tools and code made on personal time.",
                    recommendation="Exclude pre-existing IP and limit assignment strictly to project-specific deliverables paid for in full.",
                    suggested_revision="Assignment is limited solely to unique deliverables created specifically for Company during paid working hours, excluding Pre-Existing Tools."
                ),
                RiskItem(
                    id="RISK-04",
                    category="Financial",
                    severity="Warning",
                    clause_title="Net 90 Terms & 40% Withholding Discretion (Clause 2)",
                    issue="Extreme payment delays and subjective withholding.",
                    recommendation="Counter with Net 15 or Net 30, with interest on late payments and no arbitrary withholding.",
                    suggested_revision="Invoices payable Net 30. Any disputed amount must be itemized in writing within 7 business days, with undisputed amounts paid immediately."
                )
            ],
            action_checklist=[
                ChecklistItem(
                    id="CHK-01",
                    task="Send formal redline request striking out Clause 5 (Non-Compete) completely",
                    category="Before Signing",
                    trigger_or_deadline="Prior to signing contract",
                    is_crucial=True
                ),
                ChecklistItem(
                    id="CHK-02",
                    task="Insert explicit liability cap tying exposure to total fees received",
                    category="Before Signing",
                    trigger_or_deadline="Prior to signing contract",
                    is_crucial=True
                ),
                ChecklistItem(
                    id="CHK-03",
                    task="Amend payment schedule from Net 90 to Net 30 and remove 40% fee withholding",
                    category="Before Signing",
                    trigger_or_deadline="Negotiation phase",
                    is_crucial=True
                ),
                ChecklistItem(
                    id="CHK-04",
                    task="Document all pre-existing software tools and open-source libraries in a written Exhibit B exclusion list",
                    category="Before Signing",
                    trigger_or_deadline="Day 1 of engagement",
                    is_crucial=True
                ),
                ChecklistItem(
                    id="CHK-05",
                    task="Maintain digital copies of all approved milestone delivery receipts and weekly timesheets",
                    category="Ongoing",
                    trigger_or_deadline="Weekly",
                    is_crucial=False
                )
            ],
            lawyer_prep=LawyerPrep(
                document_summary="Independent Contractor Agreement containing predatory non-compete, offshore arbitration, and uncapped liability terms.",
                top_red_flags=[
                    "36-month worldwide non-compete prohibiting work in tech.",
                    "Uncapped indemnification exposing personal assets.",
                    "Perpetual surrender of pre-existing and personal off-hours IP.",
                    "Offshore arbitration in Cayman Islands making wage claims uneconomic."
                ],
                questions_to_ask=[
                    "Is the 36-month worldwide non-compete enforceable in my state/country, or does local labor statute void it?",
                    "What specific language should I use to safely exclude my prior software code and tools from the IP assignment?",
                    "If the client sues in the Cayman Islands for an alleged IP dispute, what is my actual jurisdictional vulnerability?"
                ],
                negotiation_targets=[
                    "Strike Clause 5 (Non-compete) entirely or limit to named direct competitors for 6 months.",
                    "Cap total liability to 1x contract value (approx $13,500).",
                    "Change jurisdiction to Contractor's home state/province."
                ],
                financial_exposure_note="Potentially catastrophic due to unlimited indemnification clause and foreign arbitration expense provisions."
            ),
            disclaimer=disclaimer
        )

    # Detect Residential Lease
    elif "lease" in lower or "tenant" in lower or "landlord" in lower or "rent" in lower:
        return AnalyzeResponse(
            document_title="Residential Lease Agreement",
            document_type="Tenancy & Real Estate Lease",
            overall_risk_score=24,
            risk_verdict="Favorable / Standard",
            executive_summary=(
                "This is a relatively standard, balanced residential tenancy agreement for 12 months. It outlines clear "
                "rent amounts ($1,850/mo), a 2-month security deposit ($3,700), standard maintenance responsibilities, "
                "a reasonable 24-hour inspection notice window, and standard 30-day non-renewal notification."
            ),
            clauses=[
                ClauseExplanation(
                    clause_number="Clause 2",
                    original_title="Term & Rent",
                    original_snippet="Monthly rent is $1,850.00... A late fee of $75.00 shall automatically apply after the fifth calendar day...",
                    plain_english="Rent is due on the 1st of every month. You have a 5-day grace period, after which a $75 fee applies.",
                    risk_level="Safe",
                    implication="Clear, predictable monthly financial commitment with standard grace period."
                ),
                ClauseExplanation(
                    clause_number="Clause 3",
                    original_title="Security Deposit",
                    original_snippet="Tenant shall deposit... $3,700.00... returned within 30 days following lease expiration, subject to ordinary wear and tear.",
                    plain_english="You pay $3,700 upfront as a security deposit. The landlord must return it within 30 days of move-out, minus legitimate repair bills.",
                    risk_level="Safe",
                    implication="Standard deposit protection; document pre-existing defects during move-in."
                ),
                ClauseExplanation(
                    clause_number="Clause 4",
                    original_title="Maintenance & Repairs",
                    original_snippet="Landlord responsible for structural, plumbing, electrical... Tenant responsible for minor repairs under $100...",
                    plain_english="The landlord fixes major structural, electrical, and pipe issues. You pay for minor fixes under $100 and AC air filter changes.",
                    risk_level="Safe",
                    implication="Fair division of repair responsibilities."
                ),
                ClauseExplanation(
                    clause_number="Clause 5",
                    original_title="Inspection & Right of Entry",
                    original_snippet="Landlord... right to enter... upon providing a minimum of 24 hours advance notice, except in emergencies.",
                    plain_english="The landlord cannot show up unannounced. They must give you at least 24 hours warning before visiting, unless there's a flood or fire.",
                    risk_level="Safe",
                    implication="Complies with statutory privacy rights."
                ),
                ClauseExplanation(
                    clause_number="Clause 7",
                    original_title="Termination & Renewal Notice",
                    original_snippet="Either party may terminate... upon 30 days advance written notice... tenancy converts to month-to-month at 10% rate increase.",
                    plain_english="You must give written notice 30 days before the lease ends if you plan to move out; otherwise, rent increases by 10% on a monthly basis.",
                    risk_level="Warning",
                    implication="Automatic 10% price escalation if renewal or vacancy notice deadline is missed."
                ),
            ],
            risks=[
                RiskItem(
                    id="RISK-01",
                    category="Financial",
                    severity="Warning",
                    clause_title="Automatic 10% Month-to-Month Rent Increase (Clause 7)",
                    issue="Missing the 30-day notice trigger increases rent from $1,850 to $2,035/month.",
                    recommendation="Set a calendar reminder for 45 days before the lease expiration date (February 14, 2027).",
                    suggested_revision="Tenancy shall convert to month-to-month at the same base rent unless renegotiated."
                ),
                RiskItem(
                    id="RISK-02",
                    category="Liability",
                    severity="Low",
                    clause_title="Tenant Minor Repairs Under $100 (Clause 4)",
                    issue="Cumulative minor maintenance expenses could accumulate.",
                    recommendation="Ensure landlord repairs existing fixture defects prior to move-in date.",
                    suggested_revision="Clarify that minor repairs under $100 apply only to tenant-caused maintenance, not pre-existing wear."
                )
            ],
            action_checklist=[
                ChecklistItem(
                    id="CHK-01",
                    task="Conduct joint walk-through move-in inspection and photograph all walls, floors, and appliances",
                    category="Before Signing",
                    trigger_or_deadline="Before April 1, 2026",
                    is_crucial=True
                ),
                ChecklistItem(
                    id="CHK-02",
                    task="Pay initial rent ($1,850) and security deposit ($3,700) via traceable bank transfer",
                    category="Before Signing",
                    trigger_or_deadline="By March 31, 2026",
                    is_crucial=True
                ),
                ChecklistItem(
                    id="CHK-03",
                    task="Set calendar alert for Lease Non-Renewal Notice deadline",
                    category="Post Signing",
                    trigger_or_deadline="February 15, 2027 (45 days prior to expiry)",
                    is_crucial=True
                ),
                ChecklistItem(
                    id="CHK-04",
                    task="Replace HVAC filters every 90 days to avoid minor repair disputes",
                    category="Ongoing",
                    trigger_or_deadline="Quarterly",
                    is_crucial=False
                )
            ],
            lawyer_prep=LawyerPrep(
                document_summary="12-month standard residential tenancy agreement for $1,850/mo with 2-month security deposit.",
                top_red_flags=[
                    "Automatic 10% rent hike upon default conversion to month-to-month.",
                    "Tenant responsibility for sub-$100 minor repairs."
                ],
                questions_to_ask=[
                    "Does local municipal tenant law cap security deposits at 1 month rather than 2 months?",
                    "What are the statutory requirements for security deposit escrow accounts and interest accrual?"
                ],
                negotiation_targets=[
                    "Negotiate security deposit down to 1 month ($1,850).",
                    "Limit month-to-month escalation to local CPI index rather than fixed 10%."
                ],
                financial_exposure_note="Total annual lease commitment is $22,200 plus refundable $3,700 deposit."
            ),
            disclaimer=disclaimer
        )

    # General / Fallback Legal Analysis
    return AnalyzeResponse(
        document_title="Legal Agreement Analysis",
        document_type="Commercial / General Contract",
        overall_risk_score=45,
        risk_verdict="Moderate Risk",
        executive_summary=(
            "The document establishes reciprocal obligations between parties. Key provisions require careful "
            "review regarding liability limitations, confidentiality duration, and dispute resolution venues."
        ),
        clauses=[
            ClauseExplanation(
                clause_number="Section 1",
                original_title="Purpose & Scope",
                original_snippet=text[:180] + "...",
                plain_english="Defines the core operational relationship and permissible activities between parties.",
                risk_level="Safe",
                implication="Foundational operational clause."
            ),
            ClauseExplanation(
                clause_number="Section 2",
                original_title="Obligations & Compliance",
                original_snippet="Parties agree to perform covenants with reasonable care and confidentiality...",
                plain_english="Both sides must protect sensitive business information and carry out stated duties diligently.",
                risk_level="Warning",
                implication="Requires operational adherence to prevent breach claims."
            ),
        ],
        risks=[
            RiskItem(
                id="RISK-GEN-01",
                category="Liability",
                severity="Warning",
                clause_title="Dispute Jurisdiction & Legal Fees",
                issue="Venue and legal expense allocation should be localized.",
                recommendation="Ensure governing law is set to mutual home jurisdiction.",
                suggested_revision="Governing law shall be the courts of mutual convenience."
            )
        ],
        action_checklist=[
            ChecklistItem(
                id="CHK-GEN-01",
                task="Confirm execution authority of signatories",
                category="Before Signing",
                trigger_or_deadline="Prior to signing",
                is_crucial=True
            ),
            ChecklistItem(
                id="CHK-GEN-02",
                task="Store executed copy with date stamped verification",
                category="Post Signing",
                trigger_or_deadline="Effective date",
                is_crucial=True
            )
        ],
        lawyer_prep=LawyerPrep(
            document_summary="Standard commercial agreement requiring validation of termination triggers and dispute terms.",
            top_red_flags=["Potential lack of liability limitation cap."],
            questions_to_ask=["Does this agreement align with standard commercial practices in our sector?"],
            negotiation_targets=["Insert mutual liability caps and clear termination rights."],
            financial_exposure_note="Exposure bounded by transaction value once liability caps are affirmed."
        ),
        disclaimer=disclaimer
    )

def get_mock_comparison(contract_a: str, contract_b: str, name_a: str = "Contract A", name_b: str = "Contract B") -> CompareResponse:
    disclaimer = get_standard_disclaimer()
    return CompareResponse(
        comparison_title=f"Comparison: {name_a} vs. {name_b}",
        executive_summary=(
            f"{name_a} offers balanced, industry-standard terms with a 2-year duration and standard remedies. "
            f"In contrast, {name_b} introduces aggressive one-sided restrictions, including a 6-month non-solicitation/exclusivity "
            f"period, a 5-year confidentiality obligation, and a severe $100,000 liquidated damages penalty clause."
        ),
        favorability_score_a=78,
        favorability_score_b=32,
        comparisons=[
            ClauseComparison(
                topic="Exclusivity & Purpose",
                contract_a_terms="Standard mutual collaboration exploration with no exclusivity or vendor lock-in.",
                contract_b_terms="Strict 6-month exclusivity barring engagement with any competing vendors.",
                divergence_level="Major Conflict",
                favors="Contract A",
                analysis="Contract B locks your organization into an exclusive evaluation window without guaranteeing any deal."
            ),
            ClauseComparison(
                topic="Confidentiality Duration",
                contract_a_terms="Two (2) years from the date of disclosure.",
                contract_b_terms="Five (5) years from disclosure, with perpetual survival for trade secrets.",
                divergence_level="Significant",
                favors="Contract A",
                analysis="A 5-year restriction creates prolonged compliance tracking overhead compared to standard 2-year terms."
            ),
            ClauseComparison(
                topic="Breach Remedies & Liquidated Damages",
                contract_a_terms="Standard equitable relief and proven actual damages.",
                contract_b_terms="Automatic $100,000 liquidated damages per alleged violation without proof of actual harm.",
                divergence_level="Major Conflict",
                favors="Contract A",
                analysis="The $100,000 liquidated damages clause in Contract B is punitive and creates massive liability exposure."
            ),
            ClauseComparison(
                topic="Governing Law & Venue",
                contract_a_terms="Delaware State law (neutral corporate standard).",
                contract_b_terms="New York Commercial Division courts.",
                divergence_level="Minor",
                favors="Neutral",
                analysis="Both venues are standard, but Delaware is generally more predictable for business contracts."
            )
        ],
        critical_differences=[
            "Contract B introduces an unprecedented $100,000 liquidated damages clause.",
            "Contract B extends non-disclosure obligations from 2 years to 5 years.",
            "Contract B mandates a 6-month exclusivity lock-out preventing discussions with competitors."
        ],
        negotiation_advice=(
            "Reject the $100,000 liquidated damages clause in Contract B immediately. Request that Contract B be revised "
            "to match the 2-year mutual standard of Contract A and delete the unilateral 6-month exclusivity restriction."
        ),
        disclaimer=disclaimer
    )

def get_mock_chat_response(query: str, doc_text: str) -> ChatResponse:
    q_lower = query.lower()
    disclaimer = get_standard_disclaimer()

    if "evict" in q_lower or "notice" in q_lower or "terminate" in q_lower:
        if "24 hours" in doc_text:
            return ChatResponse(
                answer=(
                    "Under Clause 3 of the agreement, the Company may terminate immediately upon 24 hours electronic notice, "
                    "with or without cause. However, you as the contractor are obligated to give 60 days advance written notice "
                    "and continue working without extra compensation."
                ),
                citations=[
                    "Clause 3: 'Company may terminate this Agreement at any time... upon 24 hours written electronic notice.'",
                    "Clause 3: 'Contractor may terminate... only upon providing 60 days advance written notice...'"
                ],
                risk_note="CRITICAL ASYMMETRY: You are bound for 60 days while the client can terminate you in 24 hours.",
                follow_up_suggestions=[
                    "What happens if I terminate before the 60 days are over?",
                    "Can we negotiate mutual 14-day or 30-day notice periods?",
                    "Does local labor law protect me against 24-hour termination?"
                ],
                disclaimer=disclaimer
            )
        elif "30 days" in doc_text:
            return ChatResponse(
                answer=(
                    "According to Clause 7, either party may terminate or request non-renewal upon giving at least 30 days advance "
                    "written notice prior to the expiration date. If notice is not provided, the agreement automatically converts "
                    "to a month-to-month term with a 10% rent increase."
                ),
                citations=[
                    "Clause 7: 'Either party may terminate or request non-renewal... upon serving at least 30 days advance written notice...'",
                    "Clause 7: 'In the absence of written notice, tenancy shall convert to month-to-month terms at a 10% rate increase.'"
                ],
                risk_note="Ensure written notice is sent at least 35 days in advance via certified mail or tracked email.",
                follow_up_suggestions=[
                    "What is the exact deadline date to give notice?",
                    "How much is the 10% rate increase on current rent?",
                    "How can I request the full return of my security deposit?"
                ],
                disclaimer=disclaimer
            )

    if "non-compete" in q_lower or "work" in q_lower or "compet" in q_lower:
        return ChatResponse(
            answer=(
                "Clause 5 imposes a 36-month (3-year) worldwide non-compete. It prohibits you from working for, consulting for, "
                "or investing in any enterprise operating in enterprise software or consulting worldwide."
            ),
            citations=[
                "Clause 5: 'For a duration of thirty-six (36) months... Contractor shall not directly or indirectly engage in... enterprise software, technology, or consulting domains worldwide.'"
            ],
            risk_note="High risk of unenforceability under many state laws (e.g., California, FTC ruling), but creates litigation threat.",
            follow_up_suggestions=[
                "Is a 3-year worldwide non-compete legal for an independent contractor?",
                "How can I ask the client to strike out the non-compete clause?",
                "What is a reasonable alternative non-compete clause?"
            ],
            disclaimer=disclaimer
        )

    if "money" in q_lower or "pay" in q_lower or "fee" in q_lower or "rent" in q_lower:
        if "4,500" in doc_text:
            return ChatResponse(
                answer=(
                    "Under Clause 2, compensation is $4,500 monthly, payable on Net 90 terms (up to 3 months delay). "
                    "Importantly, the Company reserves the unilateral right to withhold up to 40% of fees for any perceived deficiencies."
                ),
                citations=[
                    "Clause 2: 'Company agrees to pay Contractor a fixed sum of $4,500 monthly.'",
                    "Clause 2: 'Payment shall be disbursed on Net 90 terms...'",
                    "Clause 2: 'Company reserves the unilateral right to withhold up to 40% of fees for any perceived deficiencies...'"
                ],
                risk_note="Net 90 with 40% discretionary withholding creates severe financial risk.",
                follow_up_suggestions=[
                    "How can I counter-propose Net 15 or Net 30 terms?",
                    "What constitutes a 'perceived deficiency' under contract law?",
                    "What happens if invoices remain unpaid after 90 days?"
                ],
                disclaimer=disclaimer
            )
        elif "1,850" in doc_text:
            return ChatResponse(
                answer=(
                    "Under Clause 2, rent is $1,850.00 per month, due on the 1st of each month. A late fee of $75.00 is assessed "
                    "if payment is received after the 5th day of the month. The security deposit is $3,700.00."
                ),
                citations=[
                    "Clause 2: 'Monthly rent is $1,850.00, payable on or before the first day of each calendar month.'",
                    "Clause 2: 'A late fee of $75.00 shall automatically apply if payment is received after the fifth calendar day...'",
                    "Clause 3: 'Tenant shall deposit with Landlord the sum of $3,700.00... as security...'"
                ],
                risk_note="Be sure to pay on or before the 5th to avoid the $75 fee.",
                follow_up_suggestions=[
                    "When does the landlord have to return the $3,700 deposit?",
                    "What repairs am I responsible for paying?",
                    "Can the landlord enter my apartment whenever they want?"
                ],
                disclaimer=disclaimer
            )

    # General Document Answer
    return ChatResponse(
        answer=(
            f"Based on the provided document, the text governs the commercial relationship and mutual duties of the parties. "
            f"Key terms address performance expectations, confidentiality, and dispute settlement procedures."
        ),
        citations=[
            "Document Excerpt: '" + doc_text[:140].replace("\n", " ") + "...'"
        ],
        risk_note="Ensure all contractual terms match your verbal understandings before executing the agreement.",
        follow_up_suggestions=[
            "What are my key obligations under this agreement?",
            "What are the consequences of terminating early?",
            "Are there any indemnity or liability clauses?"
        ],
        disclaimer=disclaimer
    )

def get_mock_simplification(clause_text: str, reading_level: str = "Plain English") -> SimplifyResponse:
    if "indemnif" in clause_text.lower():
        return SimplifyResponse(
            original=clause_text,
            simplified="You are promising to pay for all the other company's lawsuits, legal costs, and damages if a third party sues them because of your work, with no spending limit.",
            reading_level=reading_level,
            key_takeaway="Uncapped personal financial liability; should be capped to contract value.",
            risk_verdict="Critical Risk"
        )
    return SimplifyResponse(
        original=clause_text,
        simplified="This clause sets out the responsibilities and behavioral standards both parties must follow during the contract term.",
        reading_level=reading_level,
        key_takeaway="Standard contractual obligation.",
        risk_verdict="Moderate / Safe"
    )
