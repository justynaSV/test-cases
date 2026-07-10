md name=PROJECT_CONTEXT.md
# Project Context: Test Scenario Generator for SVCloud

This file summarizes all decisions, conventions, and context established for building
a tool that generates test scenarios in Justyna Biernacka's style for the SVCloud application.

Use this file as the reference/context when working with GitHub Copilot Chat (VS Code or elsewhere)
on this repository.

---

## 1. Goal

Build a tool/assistant that generates test scenarios matching an established personal style,
based on:
- existing test case examples (CSV exports from Azure DevOps),
- user stories / feature specs (Markdown files),
- generic cross-cutting rules (e.g. calendar icon epic rules).

Approach: RAG-style (retrieval-augmented generation), not fine-tuning.
Style guide + examples + schema + prompt template, with human review loop.

---

## 2. Repository contents so far

### Test case files (real examples, used as style reference)
- `test_cases/examples/TC_authorization.csv` — login/auth scenarios
- `test_cases/examples/TC_bodyshop.csv` — Blacharnia module
- `test_cases/examples/TC_carwash.csv` — Myjnia module
- `test_cases/examples/TC_fleet.csv` — Flota Dealera module

### Newly generated scenarios (following the established style)
- `test_cases/generated/TC_unconfirmed_parts_icon.csv` — Planer Serwisu, "Części niepotwierdzone" icon feature
- `test_cases/generated/TC_calendar_event_icons_general.csv` — shared/generic rules for ALL calendar event icons
  (tooltip layout, alignment, overflow +N indicator, view scoping, role independence, etc.)
- `test_cases/generated/TC_event_icons_configuration.csv` — Konfiguracja module, admin screen for configuring
  event icon visibility/priority (CRUD, parameter overloading, drag-and-drop priority order)
- `test_cases/generated/TC_event_icons_configuration_addendum.csv` — drag-and-drop priority ordering scenarios
  (confirmed mechanism: drag-and-drop list, analogous to "Plany pracy")

### Source stories/specs used as input
- `data/knowledge/unconfirmed_parts_icon.md` — user story for "Części niepotwierdzone" icon (Planer Serwisu)
- `data/knowledge/event_icons_guidelines.md` — EPIC "IKONY KALENDARZA" — generic rules for ALL calendar event icons
- `data/knowledge/event_configuration.md` — user story for admin configuration screen (Konfiguracja module)

---

## 3. File format (CSV, Azure DevOps Test Case export style)

Semicolon-delimited. Columns:
```
Title;Step;Expected result;Area Path;Iteration Path;QA Priority;Assigned To;Preconditions
```

### Row structure rules
- **Row 1** of each scenario: `Title` + metadata filled in (`Area Path`, `Iteration Path`,
  `QA Priority`, `Assigned To`, `Preconditions`). `Step`/`Expected result` are EMPTY on this row.
- **Following rows**: `Title` is EMPTY. Only `Step` + `Expected result` are filled in.
- **Last row** of each scenario: `Step = "End of test."`, `Expected result` empty.

---

## 4. Style guide (concrete, derived from real examples)

### Titles
- Pattern: `[Module] - [feature/page] ([qualifier if applicable])`
- Examples:
  - `Blacharnia - Lista szkód w toku (single filter - grid)`
  - `User login - blocking the account`
  - `Flota Dealera - vehicle: add mileage record`
- Layout-verification tests are explicitly suffixed `(page layout)`.
- Filter tests suffixed: `(single filter)`, `(single filter - grid)`, `(single filter - columns)`,
  `(multiple filters)`.
- Negative/edge tests named literally, e.g. `invalid e-mail format`, `empty credentials`.

### Steps
- Imperative mood: `Go to:`, `Click`, `Fill in field '...'`, `Verify...`, `Right-click...`
- Verification steps almost always start with **"Verify"**.
- Multi-item checks go in ONE cell as a quoted multi-line bullet list:
  ```
  "Verify columns in page layout:
  - Col1
  - Col2"
  ```
- Reuse of other scenarios via placeholder instead of repeating steps: `[LINK]` or `<link>`
  (e.g. "Create new washing reservation [LINK]").
- Every scenario ends with literal step: `End of test.`

### Expected results
- Short, declarative: `Field is filled in.`, `It displays correctly.`,
  `The list is filtered correctly.`
- Exact UI copy quoted verbatim, in original language (mostly Polish), in single quotes:
  `Error message appears: 'Błędny login lub hasło'`
- State/color/status checks as structured mini bullet-lists inside one cell:
  ```
  Verify the reservation:
  - colour: dark blue
  - title (after hovering over): Rezerwacja
  ```

### Preconditions
- Plain text, can be multi-line, e.g.:
  `User is logged in`
  `User has an account created in Omnetic (valid e-mail and password)`

### Metadata defaults
- `Area Path`: `QA\SVCloud`
- `Iteration Path`: `QA\SVCloud\<Module>` (e.g. Autoryzacja, Blacharnia, Myjnia, Flota,
  Planer Serwisu, Konfiguracja)
- `QA Priority`: mostly `Medium`
- `Assigned To`: `justyna.biernacka@softvig.pl` (constant)

### Coverage pattern per feature (order of scenario types)
1. **Page layout** scenario (verify all UI elements exist) — ALWAYS FIRST for a new page/feature.
2. **Happy path** (add/create).
3. **Edit** scenario.
4. **Delete** scenario.
5. **Single-filter/search/sort** scenario — repeated once per column
   ("Verify searching/sorting by X" as separate steps).
6. **Multiple-filter** scenario (combine 2-3 filters).
7. **Negative/validation** scenario (empty/invalid data → mandatory field errors).
8. **Cross-application/state-transition** scenarios where relevant (status colour logic,
   cross-module sync, real-time signaller behavior).

### Vocabulary
- "Verify if..." / "Verify that..." for UI state checks.
- "It displays correctly." as generic positive layout result.
- Polish UI labels always kept in original language, in single quotes.
- English used for step instructions/descriptions.

---

## 5. Modules identified so far

- Autoryzacja (Authorization/login)
- Blacharnia (Bodyshop)
- Myjnia (Carwash)
- Flota / Flota Dealera (Fleet)
- Planer Serwisu (Service Planner) — calendar, event icons
- Konfiguracja (Configuration) — admin settings
- Other modules mentioned but not yet covered: BMS, Hotel opon, Video service

---

## 6. Business domain notes (from stories covered so far)

### Calendar event icons (EPIC: IKONY KALENDARZA) — generic rules applying to ALL icons
- Displayed only on **BOK** and **Warsztat** calendars (NOT Myjnia, NOT Flota).
- Displayed only in **normal view** (not compact view).
- Displayed in views: **1-day, 7-day, 30-day**.
- Icons are **left-aligned**; if not all fit, show **+N** overflow indicator (white number,
  no border/background) at the end, right side of visible icons.
- In 1-day view: hours are always shown and **right-aligned**; icons remain left-aligned;
  overflow logic still applies.
- Icon **order/priority** is configurable in system settings (admin) — same order applies
  wherever the icon appears.
- Icons are **default white**, using **FontAwesome v5 Classic Regular** icon set.
- **Not clickable**, **no dedicated tooltip** on the icon itself — icons only appear inside
  the task's own tooltip in a dedicated bottom section, in **two columns** (icon + event name).
- Icon **name/translation** shown in tooltip according to configured event name + language.
- Visibility is **NOT dependent on user role or app permissions** — if user has calendar
  access, they see the icons (no extra logic).
- Real-time behavior: icons appear/disappear automatically via a "signaller" mechanism
  when the underlying condition changes (no manual refresh needed on the calendar itself
  for icon show/hide — this is DIFFERENT from the configuration screen behavior, see below).

### "Części niepotwierdzone" (Unconfirmed Parts) icon — specific instance
- Module: Planer Serwisu.
- Icon: FontAwesome `box-open` (Classic Regular).
- **Show condition**: repair's "Części" field = `Wymagane` AND no confirmation entry exists
  in `SpRepair.SpRepairPartsConfirmation`.
- **Hide condition**: repair's "Części" field = `Wymagane` AND confirmation entry EXISTS.
- Real-time reactive (signaller) — confirming/un-confirming parts immediately shows/hides
  icon without page refresh.
- Follows all generic calendar icon epic rules above (tooltip, alignment, view scoping, etc.)

### Event icons configuration screen — admin feature (Konfiguracja module)
- Menu path: `Konfiguracja systemowa → Planowanie Serwisu → Serwis → Ikony zdarzeń`
  (positioned directly under "Cechy napraw").
- **Access**: Local Administrator ONLY.
- **List columns**: Operacje, Zdarzenie, Widoczne? (Tak/Nie), Rodzaj zasobu, Symbol, Kolor
  (with graphical visualization), Firma, Lokalizacja, Instancja, Rodzaj profilu, Profil.
- **List actions**: Edytuj, Usuń (per row); header: Dodaj, Wyczyść filtry.
- **Add/Edit form fields**:
  - Zdarzenie (mandatory)
  - Widoczny Tak/Nie (mandatory)
  - Rodzaj zasobu (dropdown: Doradca serwisowy, Mechanik, Pracownik Door2Door, Stanowisko)
  - Symbol — NON-EDITABLE, auto-filled per event by vendor default
  - Kolor ikony (mandatory) — auto-filled default, editable via colour picker
    (basic/producer colours + custom colour definition)
  - Priority/order — **drag-and-drop list**, analogous to "Plany pracy" mechanism (CONFIRMED)
  - Parameter overloading section: Firma, Lokalizacja, Instancja, Rodzaj profilu, Profil
    (same mechanism as system parameters — more specific overload takes precedence)
- **Save behavior**:
  - Recalculates icon visibility for calendar tasks **from the current day forward only**
    (past tasks keep their previously calculated state).
  - Calendar is **NOT auto-refreshed** — user must manually refresh the calendar to see
    updated icon visibility. (This is DIFFERENT from the real-time signaller behavior for
    individual icon show/hide triggered by data changes — that IS real-time; only
    configuration-driven changes require manual refresh.)

---

## 7. Suggested project scaffolding (not yet created in repo)

```
test-cases/
├── data/
│   ├── raw/                  # original XLSX/CSV exports
│   └── knowledge/            # PRDs, user stories, API docs, glossary
├── test_cases/
│   ├── examples/             # curated best scenarios (style reference)
│   └── generated/            # ready CSV files for Azure DevOps import
├── ingestion/
│   ├── parse_xlsx.py
│   ├── chunk_docs.py
│   └── build_embeddings.py
├── prompts/
│   ├── system_prompt.md
│   ├── style_guide.md        # see section 4 above, formalize as standalone file
│   └── output_schema.json
├── generation/
│   ├── generate_scenarios.py
│   └── export_to_csv.py
├── validation/
│   └── validate_output.py
└── review/
    └── scoring_sheet.csv
```

### Output schema (JSON) matching the real CSV row structure
```json
{
  "type": "object",
  "required": ["title", "area_path", "iteration_path", "qa_priority", "assigned_to", "preconditions", "steps"],
  "properties": {
    "title": {"type": "string"},
    "area_path": {"type": "string", "const": "QA\\SVCloud"},
    "iteration_path": {"type": "string"},
    "qa_priority": {"enum": ["Low", "Medium", "High"]},
    "assigned_to": {"type": "string"},
    "preconditions": {"type": "string"},
    "steps": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "step": {"type": "string"},
          "expected_result": {"type": "string"}
        },
        "required": ["step"]
      }
    }
  }
}
```

---

## 8. Open items / things to confirm

- [ ] Confirm full list of modules (BMS, Hotel opon, Video service, Door to door — scope TBD).
- [ ] Formalize `prompts/style_guide.md` as a standalone file (currently only in this context doc).
- [ ] Decide whether to build the Python ingestion/generation scripts now or keep using
      Copilot Chat + this context file as the "poor man's RAG" approach.
- [ ] Set up GitHub Project board (manual creation needed — no API tool available for
      GitHub Projects v2 creation) and optionally create Issues per feature/story to track work.
- [ ] Confirm exact overflow icon-fit thresholds (pixel/character limits) if precise testing
      of the +N indicator is needed.
- [ ] Confirm priority/order UI behavior details for drag-and-drop (single global list vs.
      grouped/scoped per "Rodzaj zasobu") — flagged as open question in
  `test_cases/generated/TC_event_icons_configuration_addendum.csv`.

---

## 9. How to use this file with Copilot Chat in VS Code

1. Clone the repo: `git clone https://github.com/wrozka666/test-cases.git`
2. Open it in VS Code with the GitHub Copilot extension installed.
3. Open Copilot Chat and reference this file, e.g.:
  - *"Read PROJECT_CONTEXT.md and test_cases/examples/TC_bodyshop.csv, then generate a new test scenario for
     [feature] in module [X] following the same style."*
   - *"Based on the style guide in PROJECT_CONTEXT.md, review this draft scenario I wrote
     and tell me what to fix."*
4. Since Copilot Chat sessions don't carry over conversation history between github.com
   and VS Code, this file acts as the persistent shared memory/context between sessions.
