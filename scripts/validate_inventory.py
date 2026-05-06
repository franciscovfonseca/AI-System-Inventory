#!/usr/bin/env python3
"""
validate_inventory.py
---------------------
Validates the NovaPay AI system inventory for completeness and
governance compliance before report generation.

Checks performed:
  1. All mandatory fields are populated
  2. HIGH RISK systems have a named system_owner
  3. HIGH RISK systems have a review_cycle of 6 months or less
  4. Automated decision systems have documented human_oversight_notes
  5. No duplicate system_id values exist
  6. All system_ids follow the expected format (NP-XXX)

Usage:
  python scripts/validate_inventory.py

Exit codes:
  0 - All checks passed
  1 - One or more checks failed (details printed to stdout)
"""

import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MANDATORY_FIELDS = [
    "system_id",
    "system_name",
    "purpose",
    "data_sources",
    "business_impact",
    "system_owner",
    "review_cycle",
    "affects_individuals",
    "automated_decision",
    "sector",
    "deployment_date",
    "vendor_or_inhouse",
]

# Maximum allowed review cycle (in months) for HIGH RISK systems
HIGH_RISK_MAX_REVIEW_MONTHS = 6

# Regex pattern for system_id format
SYSTEM_ID_PATTERN = re.compile(r"^NP-\d{3}$")

# Map review cycle strings to month counts for comparison
REVIEW_CYCLE_MAP = {
    "1 month": 1,
    "2 months": 2,
    "3 months": 3,
    "6 months": 6,
    "12 months": 12,
    "annually": 12,
    "quarterly": 3,
    "monthly": 1,
    "biannual": 6,
    "semi-annual": 6,
}


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def parse_review_months(review_cycle_str: str) -> int | None:
    """Parse a review cycle string to a number of months. Returns None if unparseable."""
    normalised = review_cycle_str.strip().lower()
    return REVIEW_CYCLE_MAP.get(normalised)


def validate_inventory(inventory: dict) -> tuple[list, list]:
    """
    Validate the inventory dict.

    Returns:
      (passed_checks, failed_checks) - lists of strings describing each result.
    """
    passed = []
    failed = []
    systems = inventory.get("systems", [])

    # --- Check 1: No duplicate system_ids ---
    ids = [s.get("system_id", "") for s in systems]
    duplicates = [sid for sid in set(ids) if ids.count(sid) > 1]
    if duplicates:
        failed.append(f"Duplicate system_id values found: {duplicates}")
    else:
        passed.append("No duplicate system IDs detected")

    # --- Check 2: system_id format ---
    bad_format = [s["system_id"] for s in systems if not SYSTEM_ID_PATTERN.match(s.get("system_id", ""))]
    if bad_format:
        failed.append(f"system_id format invalid (expected NP-XXX): {bad_format}")
    else:
        passed.append("All system IDs match expected format (NP-XXX)")

    for system in systems:
        sid = system.get("system_id", "?")
        name = system.get("system_name", "?")

        # --- Check 3: Mandatory fields populated ---
        missing = []
        for field in MANDATORY_FIELDS:
            value = system.get(field)
            if value is None or value == "" or value == []:
                missing.append(field)
        if missing:
            failed.append(f"[{sid}] {name} - Missing mandatory fields: {missing}")
        else:
            passed.append(f"[{sid}] All mandatory fields populated")

        # --- Check 4: HIGH RISK systems have a named owner ---
        classification = system.get("eu_ai_act_classification", {})
        risk_tier = classification.get("risk_tier", "UNCLASSIFIED")

        if risk_tier == "HIGH RISK":
            owner = system.get("system_owner", "").strip()
            if not owner or owner.lower() in ("tbc", "unknown", "n/a", ""):
                failed.append(f"[{sid}] {name} - HIGH RISK system has no named system_owner")
            else:
                passed.append(f"[{sid}] HIGH RISK system has a named owner: '{owner}'")

            # --- Check 5: HIGH RISK systems have review_cycle ≤ 6 months ---
            review_cycle = system.get("review_cycle", "")
            months = parse_review_months(review_cycle)
            if months is None:
                failed.append(
                    f"[{sid}] {name} - Could not parse review_cycle '{review_cycle}'. "
                    f"Use a standard value (e.g. '3 months', '6 months')."
                )
            elif months > HIGH_RISK_MAX_REVIEW_MONTHS:
                failed.append(
                    f"[{sid}] {name} - HIGH RISK system has review_cycle '{review_cycle}' "
                    f"({months} months), which exceeds the {HIGH_RISK_MAX_REVIEW_MONTHS}-month maximum."
                )
            else:
                passed.append(f"[{sid}] HIGH RISK system review cycle is within limit ({review_cycle})")

        # --- Check 6: Automated decision systems have oversight notes ---
        if system.get("automated_decision"):
            notes = system.get("human_oversight_notes", "").strip()
            if not notes or len(notes) < 20:
                failed.append(
                    f"[{sid}] {name} - Automated decision system is missing human_oversight_notes "
                    f"(field is blank or too short). Document the human oversight mechanism."
                )
            else:
                passed.append(f"[{sid}] Human oversight documented for automated decision system")

    return passed, failed


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    repo_root = Path(__file__).parent.parent
    inventory_path = repo_root / "configs" / "ai_inventory.json"

    if not inventory_path.exists():
        print(f"[ERROR] Inventory file not found: {inventory_path}")
        sys.exit(1)

    with open(inventory_path, "r", encoding="utf-8") as f:
        inventory = json.load(f)

    # Warn if classifications haven't been run
    first_system = inventory["systems"][0]
    if not first_system.get("eu_ai_act_classification"):
        print("[WARNING] EU AI Act classifications not found.")
        print("          Run classify_systems.py first for full HIGH RISK validation.\n")

    passed, failed = validate_inventory(inventory)

    # Print results
    print("\n" + "=" * 60)
    print("  AI Inventory Validation - NovaPay")
    print("=" * 60 + "\n")

    for check in passed:
        print(f"  [✓] {check}")

    if failed:
        print()
        for check in failed:
            print(f"  [✗] {check}")
        print(f"\n  Validation FAILED - {len(failed)} issue(s) found. Resolve before generating report.\n")
        sys.exit(1)
    else:
        print(f"\n  Validation PASSED - All {len(passed)} checks completed successfully.")
        print("  Ready to generate governance report.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
