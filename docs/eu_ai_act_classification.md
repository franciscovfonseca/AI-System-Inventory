# EU AI Act Risk Classification

**Framework:** Regulation (EU) 2024/1689 - EU AI Act  
**Client:** Financial Services  
**Analyst:** Francisco Fonseca  
**Date:** March 2026  

---

## The EU AI Act Risk Framework

The EU AI Act structures AI oversight around four risk tiers. The tier determines what obligations apply - not whether a system is well-built.

| Tier | Criteria | Regulatory Response |
|---|---|---|
| 🚫 **Unacceptable Risk** | Systems that threaten fundamental rights outright | Prohibited under Article 5 |
| 🔴 **High Risk** | Systems in Annex III domains that affect individuals | Mandatory obligations under Articles 9–15 |
| 🟡 **Limited Risk** | Systems that interact with or generate content for humans | Transparency obligations under Article 50 |
| 🟢 **Minimal Risk** | All other systems | No mandatory obligations |

The guiding principle throughout is **proportionality** - the stricter the potential harm, the more rigorous the compliance requirement.

---

## Classification Results

### 🔴 NP-001 - Credit Scoring Engine · HIGH RISK

**Regulatory Reference:** Annex III §5(b) - AI in access to financial services and creditworthiness assessment

**Classification Reasoning:**

The Credit Scoring Engine determines individual applicants' eligibility for loan products. It operates in the financial services sector, directly affects natural persons and produces automated decisions - all applications below the £10,000 manual review threshold are processed without prior human review. This combination places it firmly within Annex III §5(b).

The existence of an appeals process does not reduce the classification. The automated decision is the primary output that affects the individual's access to credit and it must be compliant as a high-risk system regardless of downstream remediation mechanisms.

**Obligations under Articles 9–15:**

| Article | Requirement | Implementation |
|---|---|---|
| Art. 9 | Risk management system across the AI lifecycle | Documented risk identification, evaluation and mitigation processes for the credit model |
| Art. 10 | Data governance - quality, relevance, bias checks | Training data audited for historical bias; data lineage and pre-processing documented |
| Art. 11 | Technical documentation before and throughout deployment | Technical documentation produced and maintained per Annex IV |
| Art. 12 | Automatic logging of system operations | All decisions logged with sufficient detail to reconstruct reasoning |
| Art. 13 | Transparency to deployers about capabilities and limits | Credit team briefed on model limitations; user-facing disclosures in place |
| Art. 14 | Meaningful human oversight - not nominal | Human review capable of overriding the system; not rubber-stamping |
| Art. 15 | Accuracy, robustness and cybersecurity | Performance metrics maintained; drift monitoring active; adversarial testing conducted |

---

### 🔴 NP-002 - Fraud Detection System · HIGH RISK

**Regulatory Reference:** Annex III §5(b) - AI in access to financial services

**Classification Reasoning:**

The Fraud Detection System triggers automatic account holds on flagged transactions - effectively restricting individuals' access to their own funds. Its protective intent (preventing fraud losses) does not affect its classification. The outputs directly restrict financial access, which brings it within Annex III §5(b).

The hybrid architecture - vendor model combined with in-house rules - does not transfer compliance responsibility. As the deployer, the client retains full liability under Articles 9–15 regardless of which components are third-party. Appropriate due diligence on the vendor model was conducted and documented as part of this engagement.

**Key obligations with specific implementation notes:**

- **Article 10** - Bias vigilance is critical. A fraud model trained on historically biased data risks disproportionately flagging customers from particular demographics. Bias testing was built into the quarterly review cycle.
- **Article 14** - Human oversight must be operationally rapid. The 2-hour analyst review SLA for flagged accounts is the appropriate mechanism, but it must be enforceable and auditable, not aspirational.
- **Article 15** - Adversarial robustness testing (against fraud patterns designed to evade detection) is mandatory for this system type.

---

### 🟡 NP-003 - Customer Support Chatbot · LIMITED RISK

**Regulatory Reference:** Article 50(1) - Transparency obligations for AI systems interacting with natural persons

**Classification Reasoning:**

The chatbot interacts directly with customers via a conversational interface and is powered by a third-party LLM. It does not appear in Annex III - it makes no decisions affecting access to financial services, employment or other regulated domains. Human escalation is always available and no account-level changes are made without human confirmation.

However, Article 50(1) requires that any AI system intended to interact with natural persons must clearly inform those persons that they are interacting with an AI - unless this is obvious from context. A customer service chatbot is not obviously AI to all users, particularly older or less digitally literate customers. Disclosure is mandatory.

**Obligations and recommended implementation:**

| Obligation | Requirement | Implementation |
|---|---|---|
| Article 50(1) | Inform users they are speaking with an AI | Display a clear disclosure at the start of every chat session |
| Article 50(2) | Disclose AI-generated content if not obvious | Label chatbot responses as AI-generated in the interface |

**Recommended disclosure wording:**
> *"You are now chatting with our virtual assistant - an AI. You can request a human agent at any time."*

---

### 🟢 NP-004 - Marketing Personalisation AI · MINIMAL RISK

**Regulatory Reference:** Recital 48 - no Annex III classification applicable

**Classification Reasoning:**

The Marketing Personalisation AI segments customers and personalises product offers. It does not appear in Annex III, does not interact with individuals via a conversational interface and does not make decisions that significantly affect individuals' rights or access to services. The worst-case outcome of poor performance is suboptimal campaign ROI - not harm to fundamental rights.

The system does process personal data (browsing behaviour, transaction history), which carries separate GDPR obligations. Those were addressed in the client's data protection impact assessment, which is out of scope for this AI Act classification.

No EU AI Act mandatory obligations apply. Voluntary documentation and periodic fairness reviews of segmentation logic were recommended as good governance practice.

---

## Classification Summary

| System | Tier | Basis | Immediate Action |
|---|---|---|---|
| NP-001 Credit Scoring Engine | 🔴 HIGH RISK | Annex III §5(b) | Articles 9–15 full compliance suite |
| NP-002 Fraud Detection System | 🔴 HIGH RISK | Annex III §5(b) | Articles 9–15 full compliance suite |
| NP-003 Customer Support Chatbot | 🟡 LIMITED RISK | Article 50(1) | Add AI disclosure to chat interface |
| NP-004 Marketing Personalisation AI | 🟢 MINIMAL RISK | No Annex III classification | No mandatory action |

---

*← Back to [Main Project](../README.md)*
