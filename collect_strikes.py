import pandas as pd
import os
import glob
import GUILD_THRESHOLDS

def load_reports(reports_dir="Reports"):
    data = {}
    
    # Load CSV files (Territory War/General stats)
    csv_files = glob.glob(os.path.join(reports_dir, "*.csv"))
    for file_path in csv_files:
        data[os.path.basename(file_path)] = pd.read_csv(file_path)
        
    # Load XLSX files (Raid history)
    xlsx_files = glob.glob(os.path.join(reports_dir, "*.xlsx"))
    for file_path in xlsx_files:
        data[os.path.basename(file_path)] = pd.read_excel(file_path)
        
    return data

def main():
    reports = load_reports()
    for name, df in reports.items():
        print(f"--- {name} ---")
        print(df.head())
        print()

if __name__ == "__main__":
    main()
