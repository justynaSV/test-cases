import csv

def scenario_to_rows(scenario: dict) -> list[list[str]]:
    rows = []
    # Row 1: title + metadata
    rows.append([
        scenario["title"], "", "",
        scenario["area_path"], scenario["iteration_path"],
        scenario["qa_priority"], scenario["assigned_to"],
        scenario["preconditions"]
    ])
    # Step rows
    for s in scenario["steps"]:
        rows.append(["", s["step"], s.get("expected_result", ""), "", "", "", "", ""])
    # End of test row
    rows.append(["", "End of test.", "", "", "", "", "", ""])
    return rows

def write_csv(scenarios: list[dict], filepath: str):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Title","Step","Expected result","Area Path",
                          "Iteration Path","QA Priority","Assigned To","Preconditions"])
        for sc in scenarios:
            writer.writerows(scenario_to_rows(sc))