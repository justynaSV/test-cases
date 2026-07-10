import pandas as pd

def parse_scenarios(filepath: str, sheet_name=0) -> pd.DataFrame:
    """
    Reads test scenarios from an XLSX file into a normalized DataFrame.
    Expected columns (adjust to match your actual headers):
    ID, Title, Preconditions, Steps, TestData, ExpectedResult, Priority, Type, Requirement
    """
    df = pd.read_excel(filepath, sheet_name=sheet_name)
    df = df.dropna(how="all")
    df.columns = [c.strip() for c in df.columns]
    return df

if __name__ == "__main__":
    df = parse_scenarios("data/raw/SVC_obiegowki.xlsx")
    df.to_csv("test_cases/examples/scenarios.csv", index=False)
    print(f"Parsed {len(df)} scenarios.")