#!/usr/bin/env python3
"""
map_to_rmf.py
-------------
Maps each NovaPay AI system to the four functions of the
NIST AI Risk Management Framework 1.0 (NIST AI RMF).

Functions:
  GOVERN  — Policies, culture, accountability, and risk tolerance
  MAP     — Categorisation, context, and stakeholder impact analysis
  MEASURE — Testing, evaluation, monitoring, and bias metrics
  MANAGE  — Risk response, incident handling, and system review

Output:
  - Console table showing RMF function coverage per system
  - Updates configs/ai_inventory.json with RMF mapping data

Usage:
  python scripts/map_to_rmf.py
"""

import json
from pathlib import Path


# ---------------------------------------------------------------------------
# RMF control definitions per function
# These represent the subset of NIST AI RMF subcategories most relevant
# to financial services AI systems.
# ---------------------------------------------------------------------------

RMF_CONTROLS = {
    "GOVERN": {
        "description": "Establish organisational policies, roles, accountability structures, and risk tolerance for AI.",
        "subcategories": {
            "GOV-1.1": "Policies and processes exist to map the organisation's AI risk appetite and risk tolerance.",
            "GOV-1.2": "Accountability mechanisms for AI risks are established within the organisation.",
            "GOV-2.1": "Roles and responsibilities for AI risk management are defined and communicated.",
            "GOV-4.1": "Organisational teams are committed to AI risk management across the AI lifecycle.",
            "GOV-6.1": "Policies and procedures are in place for AI incidents, including escalation paths.",
        },
    },
    "MAP": {
        "description": "Understand the context, stakeholder impact, and risk categorisation of each AI system.",
        "subcategories": {
            "MAP-1.1": "The purpose, scope, and intended use of the AI system are documented.",
            "MAP-1.5": "Organisational risk tolerance for AI is applied in context when categorising systems.",
            "MAP-2.1": "Scientific findings, user feedback, and real-world data are used to understand the system's context.",
            "MAP-3.1": "Potential benefits and costs of the AI system are identified and documented.",
            "MAP-5.1": "Likelihood and magnitude of each identified risk is estimated and documented.",
        },
    },
    "MEASURE": {
        "description": "Evaluate AI system risks using quantitative and qualitative methods, testing, and metrics.",
        "subcategories": {
            "MS-1.1": "Evaluation approaches are defined before and during deployment.",
            "MS-2.1": "Test sets and evaluation datasets are established and maintained.",
            "MS-2.5": "Bias and fairness metrics are measured and tracked throughout the system lifecycle.",
            "MS-2.6": "System explainability and interpretability are tested and documented.",
            "MS-4.1": "AI system performance is monitored against established baselines in production.",
        },
    },
    "MANAGE": {
        "description": "Respond to, recover from, and continuously improve AI risk posture.",
        "subcategories": {
            "MG-1.1": "Risks identified in Map and Measure functions are prioritised and treated.",
            "MG-2.1": "Procedures exist for responding to AI incidents and near-misses.",
            "MG-2.4": "AI system updates, rollbacks, and decommissioning procedures are documented.",
            "MG-3.1": "Processes are in place to monitor and evaluate AI systems on an ongoing basis.",
            "MG-4.1": "Risk management activities are continually reviewed and updated based on new information.",
        },
    },
}


def map_system_to_rmf(system: dict) -> dict:
    """
    Map a single AI system to applicable NIST AI RMF subcategories.
    Returns a dict of function → list of applicable subcategory IDs.
    """
    automated = system.get("automated_decision", False)
    affects_individuals = system.get("affects_individuals", False)
    sector = system.get("sector", "")
    classification = system.get("eu_ai_act_classification", {})
    risk_tier = classification.get("risk_tier", "MINIMAL RISK")

    mapping = {}

    # GOVERN — applies to all systems
    govern_controls = ["GOV-1.1", "GOV-1.2", "GOV-2.1", "GOV-4.1"]
    if risk_tier == "HIGH RISK":
        govern_controls.append("GOV-6.1")  # Incident escalation mandatory for high-risk
    mapping["GOVERN"] = govern_controls

    # MAP — applies to all systems; depth increases with risk tier
    map_controls = ["MAP-1.1", "MAP-1.5", "MAP-3.1"]
    if affects_individuals:
        map_controls.append("MAP-2.1")
    if risk_tier == "HIGH RISK":
        map_controls.append("MAP-5.1")
    mapping["MAP"] = sorted(set(map_controls))

    # MEASURE — depth increases with automated decisions and high risk
    measure_controls = ["MS-1.1", "MS-4.1"]
    if automated:
        measure_controls += ["MS-2.1", "MS-2.5", "MS-2.6"]
    if risk_tier == "HIGH RISK":
        if "MS-2.1" not in measure_controls:
            measure_controls.append("MS-2.1")
        if "MS-2.5" not in measure_controls:
            measure_controls.append("MS-2.5")
    mapping["MEASURE"] = sorted(set(measure_controls))

    # MANAGE — all systems need basic management; high-risk needs full suite
    manage_controls = ["MG-1.1", "MG-3.1", "MG-4.1"]
    if risk_tier == "HIGH RISK" or automated:
        manage_controls += ["MG-2.1", "MG-2.4"]
    mapping["MANAGE"] = sorted(set(manage_controls))

    return mapping


def print_rmf_table(systems: list) -> None:
    """Print a formatted RMF mapping summary to stdout."""
    function_icons = {
        "GOVERN": "🔵",
        "MAP": "🟣",
        "MEASURE": "🟠",
        "MANAGE": "🟤",
    }

    print("\n" + "=" * 70)
    print("  NIST AI RMF Function Mapping — NovaPay")
    print("=" * 70)

    for system in systems:
        rmf = system.get("nist_rmf_mapping", {})
        print(f"\n  [{system['system_id']}] {system['system_name']}")
        print(f"  Risk Tier: {system.get('eu_ai_act_classification', {}).get('risk_tier', 'N/A')}\n")

        for function, controls in rmf.items():
            icon = function_icons.get(function, "⚪")
            desc = RMF_CONTROLS[function]["description"]
            print(f"  {icon} {function}")
            print(f"     {desc}")
            for control_id in controls:
                control_text = RMF_CONTROLS[function]["subcategories"].get(control_id, "")
                print(f"     • {control_id}: {control_text}")
            print()

    print("=" * 70)


def main():
    repo_root = Path(__file__).parent.parent
    inventory_path = repo_root / "configs" / "ai_inventory.json"

    if not inventory_path.exists():
        print(f"[ERROR] Inventory file not found: {inventory_path}")
        raise SystemExit(1)

    with open(inventory_path, "r", encoding="utf-8") as f:
        inventory = json.load(f)

    # Check classifications have been run
    first_system = inventory["systems"][0]
    if not first_system.get("eu_ai_act_classification"):
        print("[WARNING] EU AI Act classifications not found in inventory.")
        print("          Run classify_systems.py first for best results.")
        print("          Continuing with basic mapping...\n")

    # Map each system
    for system in inventory["systems"]:
        system["nist_rmf_mapping"] = map_system_to_rmf(system)

    # Print results
    print_rmf_table(inventory["systems"])

    # Save updated inventory
    with open(inventory_path, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)

    print(f"  [✓] RMF mapping complete. Inventory updated at: configs/ai_inventory.json")
    print(f"  [✓] See docs/nist_rmf_mapping.md for full written analysis.\n")


if __name__ == "__main__":
    main()
