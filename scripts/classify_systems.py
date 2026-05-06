#!/usr/bin/env python3
"""
classify_systems.py
-------------------
Applies EU AI Act (Regulation 2024/1689) risk classification logic
to each AI system in the NovaPay inventory.

Classification tiers:
  - UNACCEPTABLE RISK : Prohibited under Article 5
  - HIGH RISK         : Listed in Annex III; subject to Articles 9-15
  - LIMITED RISK      : Subject to transparency obligations under Article 50
  - MINIMAL RISK      : No mandatory obligations

Output:
  - Console table of classified systems
  - Updates configs/ai_inventory.json with classification results

Usage:
  python scripts/classify_systems.py
"""

import json
import os
from pathlib import Path


# ---------------------------------------------------------------------------
# Classification rules
# ---------------------------------------------------------------------------

# Annex III sector keywords that trigger HIGH RISK classification when
# the system also affects individuals AND makes automated decisions.
ANNEX_III_SECTORS = {
    "Financial Services": "Annex III §5(b) - AI systems used in credit scoring, insurance or access to financial services",
    "Employment": "Annex III §4 - AI systems used in recruitment, performance evaluation or employment decisions",
    "Education": "Annex III §3 - AI systems used in access to education or evaluation of students",
    "Law Enforcement": "Annex III §6 - AI systems used in law enforcement or border control",
    "Healthcare": "Annex III §5(a) - AI systems used in medical devices or healthcare",
    "Critical Infrastructure": "Annex III §2 - AI in safety components of critical infrastructure",
    "Justice": "Annex III §8 - AI used in administration of justice",
}

# Systems interacting with humans via generated content are LIMITED RISK
# under Article 50 transparency obligations.
LIMITED_RISK_KEYWORDS = ["chatbot", "assistant", "conversational", "llm", "chat"]


def classify_system(system: dict) -> dict:
    """
    Classify a single AI system under the EU AI Act.

    Returns a dict with:
      - risk_tier      : str  ('HIGH RISK', 'LIMITED RISK', 'MINIMAL RISK')
      - annex_ref      : str  (regulatory reference)
      - obligations    : list (what the organisation must do)
      - reasoning      : str  (plain-language explanation)
    """
    name_lower = system["system_name"].lower()
    sector = system.get("sector", "")
    affects_individuals = system.get("affects_individuals", False)
    automated_decision = system.get("automated_decision", False)
    vendor = system.get("vendor_or_inhouse", "").lower()

    # --- Check HIGH RISK ---
    if sector in ANNEX_III_SECTORS and affects_individuals:
        annex_ref = ANNEX_III_SECTORS[sector]
        obligations = [
            "Article 9  - Establish a risk management system for the lifecycle of the AI system",
            "Article 10 - Implement data governance practices (quality, relevance, bias checks)",
            "Article 11 - Maintain technical documentation before placing on market",
            "Article 12 - Enable logging and traceability of system operations",
            "Article 13 - Ensure transparency to users about the system's nature and limitations",
            "Article 14 - Implement meaningful human oversight mechanisms",
            "Article 15 - Ensure accuracy, robustness and cybersecurity throughout lifecycle",
        ]
        if automated_decision:
            reasoning = (
                f"'{system['system_name']}' operates in the {sector} sector (covered by {annex_ref.split('-')[0].strip()}), "
                f"directly affects individuals and makes automated decisions without requiring prior human review. "
                f"This combination places it firmly within the HIGH RISK tier under Annex III. "
                f"The organisation must satisfy Articles 9–15 obligations before deployment and on an ongoing basis."
            )
        else:
            reasoning = (
                f"'{system['system_name']}' operates in the {sector} sector (covered by {annex_ref.split('-')[0].strip()}) "
                f"and affects individuals, but does not make fully automated decisions. "
                f"However, its sector classification alone is sufficient to trigger HIGH RISK status under Annex III. "
                f"Articles 9–15 obligations apply."
            )
        return {
            "risk_tier": "HIGH RISK",
            "annex_ref": annex_ref,
            "obligations": obligations,
            "reasoning": reasoning,
        }

    # --- Check LIMITED RISK ---
    if any(keyword in name_lower for keyword in LIMITED_RISK_KEYWORDS) or "vendor" in vendor:
        # Chatbots and AI systems using third-party LLMs that interact with
        # humans must disclose their AI nature under Article 50.
        if any(keyword in name_lower for keyword in LIMITED_RISK_KEYWORDS):
            obligations = [
                "Article 50(1) - Inform users they are interacting with an AI system (not a human)",
                "Article 50(2) - Disclose when AI-generated content (text, images) is produced",
            ]
            reasoning = (
                f"'{system['system_name']}' interacts directly with customers via a conversational interface "
                f"and is powered by a third-party LLM vendor. Under Article 50 of the EU AI Act, "
                f"the organisation must clearly disclose to users that they are interacting with an AI system "
                f"and not a human. No Annex III classification applies. Obligations are limited to transparency disclosures."
            )
            return {
                "risk_tier": "LIMITED RISK",
                "annex_ref": "Article 50 - Transparency obligations for certain AI systems",
                "obligations": obligations,
                "reasoning": reasoning,
            }

    # --- Default: MINIMAL RISK ---
    return {
        "risk_tier": "MINIMAL RISK",
        "annex_ref": "No mandatory provisions - Recital 48 and voluntary codes of practice apply",
        "obligations": [
            "No mandatory obligations under the EU AI Act",
            "Voluntary: Consider adopting codes of conduct under Article 95",
            "Voluntary: Maintain internal documentation as good governance practice",
        ],
        "reasoning": (
            f"'{system['system_name']}' does not appear in Annex III prohibited or high-risk categories, "
            f"does not interact with individuals via a conversational interface and does not make decisions "
            f"that significantly affect individuals' rights or access to services. "
            f"It falls into the MINIMAL RISK tier. No mandatory EU AI Act obligations apply, "
            f"though voluntary codes of practice are encouraged."
        ),
    }


def print_classification_table(systems: list) -> None:
    """Print a formatted summary table to stdout."""
    tier_colours = {
        "HIGH RISK": "🔴",
        "LIMITED RISK": "🟡",
        "MINIMAL RISK": "🟢",
    }

    print("\n" + "=" * 70)
    print("  EU AI Act Risk Classification - NovaPay")
    print("=" * 70)
    print(f"  {'System ID':<10} {'System Name':<35} {'Risk Tier'}")
    print("-" * 70)

    for system in systems:
        classification = system.get("eu_ai_act_classification", {})
        tier = classification.get("risk_tier", "UNCLASSIFIED")
        icon = tier_colours.get(tier, "⚪")
        print(f"  {system['system_id']:<10} {system['system_name']:<35} {icon} {tier}")

    print("=" * 70)
    print("\n  Detailed classification reasoning:\n")

    for system in systems:
        classification = system.get("eu_ai_act_classification", {})
        print(f"  [{system['system_id']}] {system['system_name']}")
        print(f"  Tier     : {classification.get('risk_tier', 'N/A')}")
        print(f"  Reference: {classification.get('annex_ref', 'N/A')}")
        print(f"  Reasoning: {classification.get('reasoning', 'N/A')}")
        print(f"  Obligations:")
        for obligation in classification.get("obligations", []):
            print(f"    • {obligation}")
        print()


def main():
    # Resolve paths relative to this script's location
    repo_root = Path(__file__).parent.parent
    inventory_path = repo_root / "configs" / "ai_inventory.json"

    if not inventory_path.exists():
        print(f"[ERROR] Inventory file not found: {inventory_path}")
        print("        Make sure you are running from the repo root directory.")
        raise SystemExit(1)

    # Load inventory
    with open(inventory_path, "r", encoding="utf-8") as f:
        inventory = json.load(f)

    # Classify each system
    for system in inventory["systems"]:
        system["eu_ai_act_classification"] = classify_system(system)

    # Print results
    print_classification_table(inventory["systems"])

    # Write updated inventory back to JSON (with classifications populated)
    with open(inventory_path, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)

    print(f"  [✓] Classification complete. Inventory updated at: configs/ai_inventory.json")
    print(f"  [✓] See docs/eu_ai_act_classification.md for full written analysis.\n")


if __name__ == "__main__":
    main()
