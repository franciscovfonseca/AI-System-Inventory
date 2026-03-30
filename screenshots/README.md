# Screenshots

This folder contains annotated screenshots used in the project documentation.

## Expected Screenshots

| Filename | Description |
|---|---|
| `01-inventory-csv.png` | The `ai_inventory.csv` open in a spreadsheet showing all four NovaPay systems |
| `02-classify-output.png` | Terminal output of `python scripts/classify_systems.py` |
| `03-rmf-output.png` | Terminal output of `python scripts/map_to_rmf.py` |
| `04-validation-pass.png` | Terminal output of `python scripts/validate_inventory.py` showing all checks passed |
| `05-report-preview.png` | The generated `governance_report.md` rendered in GitHub |

## Adding Screenshots

When you run the project, capture terminal output and save screenshots to this folder.
Then update README.md to replace the placeholder image references with your actual screenshots:

```markdown
![Classification Output](screenshots/02-classify-output.png)
```

Screenshots should be:
- Taken at 1280px minimum width
- Cropped to relevant content only
- Saved as `.png` (preferred) or `.jpg`
- Named using the convention above for consistency with the README
