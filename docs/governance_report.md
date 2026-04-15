# AI Governance Report - NorthPoint Financial Services
**Classification:** Internal - Restricted  
**Prepared by:** AI Governance Office  
**Review Cycle:** Quarterly  
**Report Date:** Q1 2026  
**Status:** ✅ Validated - Ready for Board Review

---

## Executive Summary

NorthPoint Financial Services operates four AI systems across its credit, fraud, customer support and marketing functions. This report presents the findings of a structured governance assessment covering EU AI Act risk classification, NIST AI Risk Management Framework control mapping and identification of priority compliance actions.

**Key findings:**
- **2 of 4 systems (50%)** carry HIGH RISK classification under EU AI Act Annex III and are subject to mandatory obligations under Articles 9–15
- **2 of 4 systems** carry Limited or Minimal Risk classification with proportionate, lighter-touch obligations
- **26 governance controls** are active across the portfolio; HIGH RISK systems each carry a full 20-control suite
- **1 priority action** is required before the next regulatory cycle: formal conformity assessment for NP-001 (Credit Scoring Engine)
- All inventory records passed the 12-point automated validation check

---

## 1. AI System Inventory Summary

| ID | System | Risk Tier | Automated Decisions | Owner |
|---|---|---|---|---|
| NP-001 | Credit Scoring Engine | 🔴 HIGH RISK | Yes | Head of Credit Risk |
| NP-002 | Fraud Detection System | 🔴 HIGH RISK | Yes | Head of Financial Crime |
| NP-003 | Customer Support Chatbot | 🟡 LIMITED RISK | No | Head of Customer Operations |
| NP-004 | Marketing Personalisation AI | 🟢 MINIMAL RISK | No | Head of Marketing |

**Total systems inventoried:** 4  
**Automated decision-making systems:** 2 (NP-001, NP-002)  
**Systems subject to mandatory EU AI Act obligations:** 3 (NP-001, NP-002, NP-003)

---

## 2. EU AI Act Compliance Status

### 2.1 HIGH RISK Systems (Articles 9–15)

Both NP-001 and NP-002 are classified HIGH RISK under EU AI Act Annex III, Category 5(b) - AI systems used in financial services that determine access to credit or financial resources.

**Mandatory obligations for both systems:**

| Article | Obligation | NP-001 Status | NP-002 Status |
|---|---|---|---|
| Article 9 | Risk management system - ongoing identification, analysis and mitigation of risks | ✅ In place | ✅ In place |
| Article 10 | Data governance - training data quality, bias monitoring, data lineage | ⚠️ Partial - bias monitoring not formalised | ✅ In place |
| Article 11 | Technical documentation - system purpose, design, performance data | ✅ In place | ✅ In place |
| Article 12 | Record-keeping - automated logging of operations | ✅ In place | ✅ In place |
| Article 13 | Transparency - instructions for use provided to deployers | ⚠️ Partial - instructions require update | ✅ In place |
| Article 14 | Human oversight - measures enabling human intervention | ✅ In place | ✅ In place |
| Article 15 | Accuracy, robustness and cybersecurity - performance benchmarks defined | ✅ In place | ⚠️ Robustness testing schedule not formalised |

**NP-001 gaps requiring action:**  
- Formalise bias monitoring process for credit scoring model (Article 10)  
- Update instructions for use documentation (Article 13)

**NP-002 gaps requiring action:**  
- Establish and document formal robustness testing schedule (Article 15)

### 2.2 LIMITED RISK Systems (Article 50)

NP-003 (Customer Support Chatbot) is classified LIMITED RISK under Article 50(1). The sole mandatory obligation is disclosure: users must be informed they are interacting with an AI system at the start of every session.

**NP-003 status:** ✅ Disclosure implemented - chatbot identifies itself as AI at session start.

### 2.3 MINIMAL RISK Systems

NP-004 (Marketing Personalisation AI) carries no mandatory obligations under the EU AI Act. Voluntary adherence to AI codes of conduct is encouraged.

---

## 3. NIST AI RMF Control Coverage

Controls are applied proportionate to each system's risk level across the four NIST AI RMF functions.

| System | GOVERN | MAP | MEASURE | MANAGE | Total | Coverage |
|---|---|---|---|---|---|---|
| NP-001 Credit Scoring Engine | 5/5 | 5/5 | 5/5 | 5/5 | **20/20** | 100% |
| NP-002 Fraud Detection System | 5/5 | 5/5 | 5/5 | 5/5 | **20/20** | 100% |
| NP-003 Customer Support Chatbot | 4/5 | 4/5 | 2/5 | 3/5 | **13/20** | 65% |
| NP-004 Marketing Personalisation AI | 4/5 | 4/5 | 2/5 | 3/5 | **13/20** | 65% |

**Total active controls across portfolio:** 66  
**Assessment:** Control coverage is proportionate. The HIGH RISK systems carry full governance suites. The lower coverage for LIMITED and MINIMAL RISK systems reflects deliberate proportionality - over-governing low-risk systems would create compliance burden without reducing actual risk.

---

## 4. Priority Recommended Actions

| Priority | System | Action | Article / Framework | Owner | Target Date |
|---|---|---|---|---|---|
| 🔴 High | NP-001 | Complete formal conformity assessment before next regulatory cycle | EU AI Act Article 43 | Head of Credit Risk | Q2 2026 |
| 🔴 High | NP-001 | Formalise bias monitoring and document outcomes | EU AI Act Article 10 | Head of Credit Risk | Q2 2026 |
| 🟡 Medium | NP-002 | Establish documented robustness testing schedule | EU AI Act Article 15 | Head of Financial Crime | Q3 2026 |
| 🟡 Medium | NP-001 | Update instructions for use documentation | EU AI Act Article 13 | Head of Credit Risk | Q3 2026 |
| 🟢 Low | NP-004 | Review voluntary AI code of conduct adoption | EU AI Act Recital 97 | Head of Marketing | Q4 2026 |

---

## 5. Review Schedule

| System | Review Frequency | Next Review Due | Responsible Owner |
|---|---|---|---|
| NP-001 Credit Scoring Engine | Every 6 months | Q3 2026 | Head of Credit Risk |
| NP-002 Fraud Detection System | Every 3 months | Q2 2026 | Head of Financial Crime |
| NP-003 Customer Support Chatbot | Annually | Q1 2026 | Head of Customer Operations |
| NP-004 Marketing Personalisation AI | Annually | Q1 2026 | Head of Marketing |

---

## 6. Next Steps - Phase 2

This report concludes Phase 1 of NorthPoint's AI governance programme: inventory, classification and control mapping.

**Phase 2 - AI Risk Assessment** will apply deep risk assessment methodology to the two HIGH RISK systems identified here:
- Likelihood and impact analysis across identified risk scenarios
- Bias and fairness assessment for the Credit Scoring Engine
- Detailed EU AI Act Article 9 compliance review
- Board-level governance memo with executive recommendations

→ [Phase 2: AI Risk Assessment - NorthPoint Financial Services](https://github.com/franciscovfonseca/AI-Risk-Assessment)

---

*Report generated from validated AI inventory data. All 12 governance validation checks passed.*  
*Prepared by the AI Governance Office, NorthPoint Financial Services.*
