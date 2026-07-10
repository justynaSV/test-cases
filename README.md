# SVCloud Test Case Generator

This repository stores context, style rules, prompt templates, and generated CSV test scenarios for SVCloud. Its main purpose is to make creating Azure DevOps test cases faster while keeping them consistent with Justyna Biernacka's established QA writing style.

The current approach is RAG-style prompting: use the project context, style guide, examples, and output schema as input for Copilot Chat or another LLM, then review and export the generated scenarios as semicolon-delimited CSV files.

## Current Contents

- `PROJECT_CONTEXT.md` - main project reference with goals, domain notes, conventions, open items, and usage guidance.
- `prompts/system_prompt.md` - reusable prompt template for generating scenarios.
- `prompts/style_guide.md` - concise rules for titles, steps, expected results, metadata, and coverage order.
- `prompts/output_schema.json` - JSON schema expected from the generator before CSV export.
- `generation/export_to_csv.py` - helper for converting generated scenario dictionaries to Azure DevOps-style CSV rows.
- `ingestion/parse_xlsx.py` - initial XLSX parsing helper for turning exported examples into structured data.
- `TC_*.csv` - generated or curated test case CSV files.
- `SVC_obiegowki.xlsx` - source XLSX example currently present in the workspace.
- `validation/` - placeholder for future validation scripts.

## CSV Format

Generated test cases use a semicolon-delimited CSV format with this header:

```csv
Title;Step;Expected result;Area Path;Iteration Path;QA Priority;Assigned To;Preconditions
```

Scenario row rules:

- The first row contains `Title` and metadata. `Step` and `Expected result` are empty.
- Following rows contain only `Step` and `Expected result`.
- Every scenario ends with the exact step `End of test.`.
- Default `Area Path` is `QA\SVCloud`.
- Default `QA Priority` is `Medium` unless a feature requires another priority.

## Recommended Workflow

1. Add or update feature requirements, user stories, or notes in the repository.
2. Read `PROJECT_CONTEXT.md` and `prompts/style_guide.md` before generating scenarios.
3. Generate JSON that matches `prompts/output_schema.json`.
4. Convert generated JSON to CSV with `generation/export_to_csv.py`.
5. Review the CSV manually for business accuracy, wording, missing negative cases, and Azure DevOps import compatibility.
6. Store final files as `TC_<feature_or_module>.csv`.

Example Copilot Chat prompt:

```text
Read PROJECT_CONTEXT.md, prompts/style_guide.md, and the relevant TC_*.csv examples.
Generate test scenarios for <feature> in the same style.
Return strict JSON matching prompts/output_schema.json and flag any assumptions.
```

## Suggested Additions

The project is usable as a prompt/context workspace today, but these additions would make it more complete and repeatable:

- Create `data/raw/`, `data/gold_examples/`, and `data/knowledge/` folders for original exports, curated examples, and product knowledge.
- Add `generation/generate_scenarios.py` when generation moves from manual Copilot prompting to a scripted flow.
- Add `validation/validate_output.py` to check CSV headers, required metadata, row structure, missing `End of test.`, and schema compliance.
- Add a small sample JSON file showing the expected input for `export_to_csv.py`.
- Add dependency tracking, for example `requirements.txt` or `pyproject.toml`, for packages such as `pandas` and `openpyxl`.
- Add a `review/scoring_sheet.csv` or checklist for manual review before importing to Azure DevOps.
- Keep source user stories or feature specs in a dedicated folder so generated CSV files can be traced back to requirements.
- Decide whether `PROJECT_CONTEXT.md` or `prompts/style_guide.md` is the source of truth for style rules, then keep the other file synchronized.

## Notes From Verification

- The CSV files currently present follow the expected semicolon-delimited Azure DevOps-style structure.
- Some files mentioned in `PROJECT_CONTEXT.md` are planned but not currently present, including `data/`, `review/`, `generation/generate_scenarios.py`, and `validation/validate_output.py`.
- `ingestion/parse_xlsx.py` currently points to `data/raw/SVC_obiegowki.xlsx`, while the XLSX file is currently located at the repository root. Either move the file into `data/raw/` or update the script path before running it.
