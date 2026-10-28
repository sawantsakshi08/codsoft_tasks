"""
CodSoft Data Analytics Internship — Task 1
Project: Customer Data Cleaning and Preprocessing

Run from the project folder:
    python clean_data.py
Required packages:
    pandas
"""
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
INPUT_FILE = PROJECT_DIR / "data" / "customers_raw.csv"
OUTPUT_DIR = PROJECT_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "customers_cleaned.csv"

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = pd.read_csv(INPUT_FILE)

    print("1. ORIGINAL DATASET")
    print("Shape:", df.shape)
    print(df.head())
    print("\nData types:\n", df.dtypes)
    print("\nMissing values:\n", df.isnull().sum())
    print("\nDuplicate rows:", df.duplicated().sum())

    # Remove fully duplicated rows
    df = df.drop_duplicates().copy()

    # Standardize text fields
    for col in ["Name", "City", "Gender"]:
        df[col] = df[col].astype("string").str.strip()

    df["Name"] = df["Name"].str.title()
    df["City"] = df["City"].str.title()
    df["Gender"] = df["Gender"].str.lower().replace({
        "f": "female", "m": "male"
    }).str.title()
    df["Gender"] = df["Gender"].replace({"Unknown": pd.NA, "": pd.NA})

    # Convert columns to appropriate data types
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["PurchaseAmount"] = pd.to_numeric(df["PurchaseAmount"], errors="coerce")
    df["Satisfaction"] = pd.to_numeric(df["Satisfaction"], errors="coerce")
    df["JoinDate"] = pd.to_datetime(df["JoinDate"], errors="coerce", dayfirst=True)

    # Mark impossible/out-of-range values as missing
    df.loc[~df["Age"].between(0, 100), "Age"] = pd.NA
    df.loc[df["PurchaseAmount"] < 0, "PurchaseAmount"] = pd.NA
    df.loc[~df["Satisfaction"].between(1, 5), "Satisfaction"] = pd.NA

    # Fill numeric missing values with the column median (robust to extreme values)
    for col in ["Age", "PurchaseAmount", "Satisfaction"]:
        df[col] = df[col].fillna(df[col].median())

    # Fill missing category values with the most common category
    for col in ["Gender", "City"]:
        mode_value = df[col].mode(dropna=True)
        if not mode_value.empty:
            df[col] = df[col].fillna(mode_value.iloc[0])

    # Dates that cannot be interpreted remain missing; do not invent dates.
    # Keep date as datetime for analysis, then format for CSV.
    df["Age"] = df["Age"].round().astype("Int64")
    df["Satisfaction"] = df["Satisfaction"].round().astype("Int64")
    df["PurchaseAmount"] = df["PurchaseAmount"].round(2)

    df.to_csv(OUTPUT_FILE, index=False, date_format="%Y-%m-%d")

    print("\n2. CLEANING SUMMARY")
    print("Cleaned shape:", df.shape)
    print("Duplicate rows remaining:", df.duplicated().sum())
    print("\nMissing values after cleaning:\n", df.isnull().sum())
    print("\nCleaned data preview:\n", df.head())
    print(f"\nSaved cleaned dataset to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
