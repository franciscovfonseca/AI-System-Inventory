#!/usr/bin/env python3
"""
generate_report.py
------------------
Generates a complete AI governance report in Markdown format
from the validated NovaPay AI system inventory.

The report includes:
  - Executive summary
  - Full inventory table
  - EU AI Act classification summary
  - NIST AI RMF mapping summary
  - Prioritised recommended actions
  - 12-month review schedule

Output: docs/governance_report.md

Usage:
  python scripts/generate_report.py

Note: Run classify_systems.py, map_to_rmf.py and validate_inventory.py
      before running this script.
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


# ---------------------------------------------------------------------------
# Report sections
# ---------------------------------------------------------------------------

def build_header(inventory: dict) -> str:
    org = inventory.get("organisation", "Unknown Organisation")
    version = inventory.get("inventory_version", "1.0")
    date = datetime.now().strftime("%d %B %Y")

    return f"""# AI Governance Report - {org}

**Report Version:** {version}  
**Generated:** {date}  
**Classification:** Internal - Restricted  
**Owner:** AI Governance Team  

---

> This report summarises the AI system inventory for {org}, including EU AI Act risk classification and NIST AI RMF control mapping. It is intended for review by the AI Governance Committee and senior leadership.

"""


def build_executive_summary(systems: list) -> str:
    high_risk = [s for s in systems if s.get("eu_ai_act_classification", {}).get("risk_tier") == "HIGH RISK"]
    limited_risk = [s for s in systems if s.get("eu_ai_act_classification", {}).get("risk_tier") == "LIMITED RISK"]
    minimal_risk = [s for s in systems if s.get("eu_ai_act_classification", {}).get("risk_tier") == "MINIMAL RISK"]
    automated = [s for s in systems if s.get("automated_decision")]

    summary = f"""## Executive Summary

{len(systems)} AI systems have been inventoried and classified across NovaPay's operations.

| Metric | Count |
|---|---|
| Total AI systems inventoried | {len(systems)} |
| HIGH RISK (EU AI Act Annex III) | {len(high_risk)} |
| LIMITED RISK (Article 50) | {len(limited_risk)} |
| MINIMAL RISK | {len(minimal_risk)} |
| Systems making automated decisions | {len(automated)} |

**Key findings:**

"""
    if high_risk:
        summary += f"- **{len(high_risk)} system(s) are classified HIGH RISK** under the EU AI Act and require immediate compliance action under Articles 9–15. These systems operate in the Financial Services sector and directly affect individuals' access to credit and financial services.\n"

    if limited_risk:
        summary += f"- **{len(limited_risk)} system(s) are classified LIMITED RISK** and must comply with Article 50 transparency obligations - specifically, users must be informed they are interacting with an AI system.\n"

    if automated:
        summary += f"- **{len(automated)} system(s) make automated decisions** affecting individuals. Human oversight mechanisms are documented for all of these systems.\n"

    summary += "\nImmediate priorities are outlined in the Recommended Actions section.\n\n---\n\n"
    return summary


def build_inventory_table(systems: list) -> str:
    section = "## AI System Inventory\n\n"
    section += "| ID | System Name | Purpose | Sector | Owner | Review Cycle | Automated Decision |\n"
    section += "|---|---|---|---|---|---|---|\n"

    for s in systems:
        auto = "✅ Yes" if s.get("automated_decision") else "❌ No"
        section += (
            f"| {s['system_id']} | {s['system_name']} | "
            f"{s['purpose'][:60]}{'...' if len(s['purpose']) > 60 else ''} | "
            f"{s['sector']} | {s['system_owner']} | {s['review_cycle']} | {auto} |\n"
        )

    section += "\n---\n\n"
    return section


def build_classification_section(systems: list) -> str:
    tier_emoji = {"HIGH RISK": "🔴", "LIMITED RISK": "🟡", "MINIMAL RISK": "🟢"}

    section = "## EU AI Act Risk Classification\n\n"
    section += "Classification applied under Regulation (EU) 2024/1689 (EU AI Act).\n\n"

    # Summary table
    section += "| System | Risk Tier | Regulatory Reference |\n"
    section += "|---|---|---|\n"
    for s in systems:
        c = s.get("eu_ai_act_classification", {})
        tier = c.get("risk_tier", "UNCLASSIFIED")
        icon = tier_emoji.get(tier, "⚪")
        ref = c.get("annex_ref", "N/A")
        section += f"| {s['system_id']} - {s['system_name']} | {icon} **{tier}** | {ref} |\n"

    section += "\n"

    # Per-system detail
    for s in systems:
        c = s.get("eu_ai_act_classification", {})
        tier = c.get("risk_tier", "UNCLASSIFIED")
        icon = tier_emoji.get(tier, "⚪")

        section += f"### {icon} {s['system_id']} - {s['system_name']}\n\n"
        section += f"**Tier:** {tier}  \n"
        section += f"**Reference:** {c.get('annex_ref', 'N/A')}  \n\n"
        section += f"**Reasoning:** {c.get('reasoning', 'N/A')}\n\n"
        section += "**Obligations:**\n\n"
        for obligation in c.get("obligations", []):
            section += f"- {obligation}\n"
        section += "\n"

    section += "---\n\n"
    return section


def build_rmf_section(systems: list) -> str:
    function_icons = {"GOVERN": "🔵", "MAP": "🟣", "MEASURE": "🟠", "MANAGE": "🟤"}

    section = "## NIST AI RMF Control Mapping\n\n"
    section += "Mapped against NIST AI Risk Management Framework 1.0 (January 2023).\n\n"

    # Summary table - show which functions apply per system
    section += "| System | GOVERN | MAP | MEASURE | MANAGE |\n"
    section += "|---|---|---|---|---|\n"
    for s in systems:
        rmf = s.get("nist_rmf_mapping", {})
        gov = f"{len(rmf.get('GOVERN', []))} controls"
        mp = f"{len(rmf.get('MAP', []))} controls"
        ms = f"{len(rmf.get('MEASURE', []))} controls"
        mg = f"{len(rmf.get('MANAGE', []))} controls"
        section += f"| {s['system_id']} - {s['system_name']} | {gov} | {mp} | {ms} | {mg} |\n"

    section += "\n"

    # Per-system RMF detail
    for s in systems:
        rmf = s.get("nist_rmf_mapping", {})
        section += f"### {s['system_id']} - {s['system_name']}\n\n"

        for function, controls in rmf.items():
            icon = function_icons.get(function, "⚪")
            section += f"**{icon} {function}** ({len(controls)} subcategories)\n\n"
            for control in controls:
                section += f"- `{control}`\n"
            section += "\n"

    section += "---\n\n"
    return section


def build_recommended_actions(systems: list) -> str:
    section = "## Recommended Actions\n\n"
    section += "Prioritised by risk tier. HIGH RISK items require immediate action.\n\n"

    high_risk = [s for s in systems if s.get("eu_ai_act_classification", {}).get("risk_tier") == "HIGH RISK"]
    limited_risk = [s for s in systems if s.get("eu_ai_act_classification", {}).get("risk_tier") == "LIMITED RISK"]

    if high_risk:
        section += "### 🔴 HIGH PRIORITY - HIGH RISK Systems\n\n"
        for s in high_risk:
            section += f"**{s['system_id']} - {s['system_name']}**\n\n"
            section += "- [ ] Conduct and document a formal risk management assessment (Article 9)\n"
            section += "- [ ] Review and document data governance practices including bias checks (Article 10)\n"
            section += "- [ ] Produce and maintain technical documentation (Article 11)\n"
            section += "- [ ] Verify logging and traceability mechanisms are active (Article 12)\n"
            section += "- [ ] Audit the human oversight mechanism - confirm it is meaningful, not nominal (Article 14)\n"
            section += f"- [ ] Schedule next review: within {s.get('review_cycle', '6 months')}\n\n"

    if limited_risk:
        section += "### 🟡 MEDIUM PRIORITY - LIMITED RISK Systems\n\n"
        for s in limited_risk:
            section += f"**{s['system_id']} - {s['system_name']}**\n\n"
            section += "- [ ] Confirm the chatbot interface displays an AI disclosure to all users (Article 50)\n"
            section += "- [ ] Review vendor contract to confirm Article 50 compliance obligations are covered\n"
            section += "- [ ] Add AI disclosure to in-app and web chat interface if not already present\n\n"

    section += "### 🟢 STANDARD - ALL Systems\n\n"
    section += "- [ ] Formally assign this inventory to the AI Governance Committee for ongoing ownership\n"
    section += "- [ ] Schedule quarterly governance reviews for HIGH and LIMITED RISK systems\n"
    section += "- [ ] Conduct annual review of MINIMAL RISK systems\n"
    section += "- [ ] Integrate this inventory into the organisation's broader risk register\n\n"

    section += "---\n\n"
    return section


def build_review_schedule(systems: list) -> str:
    section = "## 12-Month Review Schedule\n\n"

    today = datetime.now()
    section += "| System | Risk Tier | Review Cycle | Next Review Date |\n"
    section += "|---|---|---|---|\n"

    cycle_to_delta = {
        "3 months": timedelta(days=90),
        "6 months": timedelta(days=182),
        "12 months": timedelta(days=365),
    }

    for s in systems:
        tier = s.get("eu_ai_act_classification", {}).get("risk_tier", "N/A")
        cycle = s.get("review_cycle", "12 months")
        delta = cycle_to_delta.get(cycle, timedelta(days=365))
        next_review = (today + delta).strftime("%B %Y")
        section += f"| {s['system_id']} - {s['system_name']} | {tier} | {cycle} | {next_review} |\n"

    section += "\n---\n\n"
    return section


def build_footer() -> str:
    date = datetime.now().strftime("%d %B %Y")
    return f"""## References

| Resource | Link |
|---|---|
| EU AI Act (Official Text) | [EUR-Lex 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689) |
| NIST AI Risk Management Framework 1.0 | [airmf.nist.gov](https://airmf.nist.gov/) |
| EU AI Act Annex III | [High-Risk System List](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689#anx_III) |
| NIST AI RMF Playbook | [airc.nist.gov](https://airc.nist.gov/Docs/2) |

---

*Generated automatically by `generate_report.py` on {date}.*  
*Repository: [github.com/franciscovfonseca/AI-System-Inventory](https://github.com/franciscovfonseca/AI-System-Inventory)*
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    repo_root = Path(__file__).parent.parent
    inventory_path = repo_root / "configs" / "ai_inventory.json"
    output_path = repo_root / "docs" / "governance_report.md"

    if not inventory_path.exists():
        print(f"[ERROR] Inventory file not found: {inventory_path}")
        sys.exit(1)

    # Check validation passes first
    print("[→] Running pre-generation validation...")
    result = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "validate_inventory.py")],
        capture_output=True,
        text=True,
    )
    print(result.stdout.strip())

    if result.returncode != 0:
        print("[ERROR] Inventory validation failed. Resolve issues before generating report.")
        sys.exit(1)

    with open(inventory_path, "r", encoding="utf-8") as f:
        inventory = json.load(f)

    systems = inventory["systems"]

    print("[→] Generating governance report...")

    report = (
        build_header(inventory)
        + build_executive_summary(systems)
        + build_inventory_table(systems)
        + build_classification_section(systems)
        + build_rmf_section(systems)
        + build_recommended_actions(systems)
        + build_review_schedule(systems)
        + build_footer()
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"[✓] Governance report generated: docs/governance_report.md")
    print(f"[✓] Report length: {len(report.splitlines())} lines")
    print(f"[✓] Open docs/governance_report.md to review.\n")


if __name__ == "__main__":
    main()
