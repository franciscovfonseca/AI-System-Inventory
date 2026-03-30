# NIST AI RMF Control Mapping

**Framework:** NIST AI Risk Management Framework 1.0 (January 2023)  
**Client:** Financial Services  
**Analyst:** Francisco Fonseca  
**Date:** March 2026  

---

## About the NIST AI RMF

The NIST AI RMF organises AI risk management into four functions that form a continuous cycle. Unlike the EU AI Act, which defines *what* obligations apply, the RMF defines *how* to implement governance in practice. The two frameworks complement each other directly.

| Function | Purpose |
|---|---|
| 🔵 **GOVERN** | Establish the policies, culture, accountability structures, and risk tolerance that underpin all other functions |
| 🟣 **MAP** | Understand the system's context, categorise it, and identify stakeholder impacts and risk priorities |
| 🟠 **MEASURE** | Evaluate AI risks using quantitative and qualitative testing, metrics, and monitoring |
| 🟤 **MANAGE** | Respond to identified risks, manage incidents, and drive continuous improvement |

I applied controls proportionate to each system's EU AI Act risk tier. HIGH RISK systems received the full governance suite. Lower-risk systems received a baseline proportionate to their actual impact.

---

## NP-001 — Credit Scoring Engine · HIGH RISK · 20 Controls

### 🔵 GOVERN

| Control | Description | Implementation |
|---|---|---|
| GOV-1.1 | AI risk appetite and tolerance documented | Defined acceptable false positive/negative rates for credit decisions; escalation thresholds documented |
| GOV-1.2 | Accountability mechanisms established | Head of Credit Risk assigned as accountable owner; escalation path to AI Governance Committee defined |
| GOV-2.1 | Roles and responsibilities communicated | Ownership documented across model development, deployment, monitoring, and incident response |
| GOV-4.1 | Cross-team commitment to AI risk management | Credit risk, data science, compliance, and legal all participate in lifecycle governance |
| GOV-6.1 | AI incident escalation procedures in place | Incident triggers defined (bias spike, model drift, regulatory complaint); response path documented |

### 🟣 MAP

| Control | Description | Implementation |
|---|---|---|
| MAP-1.1 | Purpose, scope, and intended use documented | Credit scoring for personal loan applications; UK and EU applicants; decisions up to £50,000 |
| MAP-1.5 | Organisational risk tolerance applied in context | False negative rate threshold defined; breach triggers mandatory model review |
| MAP-2.1 | Scientific findings and real-world data used to understand context | Academic literature on credit scoring bias reviewed; enforcement actions against similar firms incorporated |
| MAP-3.1 | Benefits and costs identified and documented | Benefits: faster lending decisions, reduced underwriter load. Costs: discrimination risk, regulatory exposure |
| MAP-5.1 | Likelihood and magnitude of risks estimated | Probability of biased outcomes quantified; regulatory fine exposure modelled; reputational impact scenarios documented |

### 🟠 MEASURE

| Control | Description | Implementation |
|---|---|---|
| MS-1.1 | Evaluation approaches defined before and during deployment | Accuracy, AUC-ROC, and disparate impact metrics established pre-deployment; re-evaluated quarterly |
| MS-2.1 | Test sets established and maintained | Held-out validation set maintained; refreshed with recent data semi-annually |
| MS-2.5 | Bias and fairness metrics tracked | Approval rate disparities monitored by protected characteristic using demographic parity and equalised odds |
| MS-2.6 | Explainability tested and documented | SHAP explanations implemented; model generates human-readable rationale for every rejection |
| MS-4.1 | Performance monitored against baselines in production | Alerts triggered when performance drops below threshold; distribution shift in input features monitored |

### 🟤 MANAGE

| Control | Description | Implementation |
|---|---|---|
| MG-1.1 | Identified risks prioritised and treated | Bias risk: Priority 1. Accuracy degradation: Priority 2. Treatment approach documented for each |
| MG-2.1 | AI incident and near-miss response procedures in place | Incident response procedure documented; regulatory notification assessment included |
| MG-2.4 | Model update, rollback, and decommissioning procedures documented | Tested rollback procedure maintained; Head of Credit Risk sign-off required before any model update |
| MG-3.1 | Ongoing monitoring and evaluation in place | Monthly performance dashboard; quarterly bias audit; 6-month formal governance review |
| MG-4.1 | Risk management activities continually reviewed | Lessons learned incorporated after each quarterly review; controls updated when regulatory guidance changes |

---

## NP-002 — Fraud Detection System · HIGH RISK · 20 Controls

The Fraud Detection System received the same 20-control governance suite as NP-001, with the following system-specific emphases:

**GOVERN — GOV-6.1 (Incident Escalation)** is the most operationally critical control here. A false positive surge in fraud detection can affect thousands of customers simultaneously, making rapid escalation and response a real-time operational requirement, not just a compliance formality.

**MEASURE — MS-2.5 (Bias Metrics)** requires particular vigilance. A fraud model trained on historically biased data risks disproportionately flagging customers from particular demographics or geographies. Bias testing was built into the quarterly review cycle with demographic breakdowns of flag rates.

**MANAGE — MG-2.1 (Incident Response)** was scoped to cover financial crime compliance incidents, not just technical failures. A fraud model failure that results in discriminatory outcomes is simultaneously a regulatory incident requiring assessment against FCA reporting obligations.

Owner: Head of Financial Crime (replacing Head of Credit Risk for all GOV-1.2 references).

---

## NP-003 — Customer Support Chatbot · LIMITED RISK · 13 Controls

The chatbot makes no automated decisions affecting individuals' rights, so the MEASURE controls targeting bias in decision-making (MS-2.5, MS-2.6) were not applied. The primary risk is reputational and operational — incorrect information, poor escalation, or data privacy violations.

### 🔵 GOVERN (4 controls)
- **GOV-1.1** — Acceptable resolution rate defined; query types the chatbot must not handle documented (complaints, regulatory matters, account changes)
- **GOV-1.2** — Head of Customer Experience owns the system; vendor contract assigns clear responsibilities
- **GOV-2.1** — Roles documented across transcript review, vendor management, and complaint escalation
- **GOV-4.1** — Customer experience, legal, and security teams all have input into chatbot governance

### 🟣 MAP (4 controls)
- **MAP-1.1** — Scope defined: tier-1 support only; no account changes without human confirmation
- **MAP-1.5** — Risk tolerance defined: escalation rate above X% triggers content review
- **MAP-2.1** — Vendor LLM capabilities and limitations assessed; known failure modes documented
- **MAP-3.1** — Benefits (reduced ticket volume) and costs (reputational risk from misinformation) documented

### 🟠 MEASURE (2 controls)
- **MS-1.1** — Resolution rate, escalation rate, CSAT, and complaint rate tracked monthly
- **MS-4.1** — Production monitoring for unusual escalation spikes or satisfaction drops

### 🟤 MANAGE (3 controls)
- **MG-1.1** — High escalation rate triggers content review; misinformation complaints trigger immediate review
- **MG-3.1** — Monthly transcript sample review; quarterly vendor performance review
- **MG-4.1** — Customer feedback incorporated into vendor chatbot training data reviews

---

## NP-004 — Marketing Personalisation AI · MINIMAL RISK · 13 Controls

As a minimal-risk system, the full control suite was not mandated. I applied a proportionate governance baseline that provides meaningful oversight without creating compliance overhead disproportionate to the actual risk.

### 🔵 GOVERN (4 controls)
- **GOV-1.1** — Acceptable targeting parameters defined (no use of protected characteristics for product exclusions)
- **GOV-1.2** — Head of Marketing is accountable owner
- **GOV-2.1** — Marketing and data teams understand their responsibilities
- **GOV-4.1** — Marketing, legal, and data privacy teams aligned on data use within campaigns

### 🟣 MAP (4 controls)
- **MAP-1.1** — Purpose documented: marketing segmentation and campaign personalisation only
- **MAP-1.5** — Risk tolerance applied: no use of sensitive data categories for targeting
- **MAP-2.1** — GDPR obligations assessed alongside AI Act considerations
- **MAP-3.1** — Benefits (higher campaign ROI) and costs (GDPR exposure, reputational risk) documented

### 🟠 MEASURE (2 controls)
- **MS-1.1** — Campaign performance metrics and segmentation accuracy tracked
- **MS-4.1** — Annual review of targeting logic and segment composition

### 🟤 MANAGE (3 controls)
- **MG-1.1** — Risks prioritised; data misuse risk treated as Priority 1
- **MG-3.1** — Annual review of segmentation rules and targeting parameters
- **MG-4.1** — Controls updated if regulatory guidance on marketing AI changes

---

## Control Coverage Summary

| System | GOVERN | MAP | MEASURE | MANAGE | Total |
|---|---|---|---|---|---|
| 🔴 NP-001 Credit Scoring Engine | 5 | 5 | 5 | 5 | **20** |
| 🔴 NP-002 Fraud Detection System | 5 | 5 | 5 | 5 | **20** |
| 🟡 NP-003 Customer Support Chatbot | 4 | 4 | 2 | 3 | **13** |
| 🟢 NP-004 Marketing Personalisation AI | 4 | 4 | 2 | 3 | **13** |

The difference in control counts is intentional. Applying 20 controls to a minimal-risk marketing system would create governance noise without reducing actual risk — and would make it harder to focus serious attention on the systems that genuinely warrant it.

---

*← Back to [Main Project](../README.md)*
