import pandas as pd
from pathlib import Path

excel_file = Path("data/IIoT_Smart_Parking_Management.xlsx")
csv_file = Path("data/parking_data.csv")

# Read Excel dataset
df = pd.read_excel(excel_file)

# Save as CSV
df.to_csv(csv_file, index=False)

print("=" * 50)
print("EXCEL TO CSV CONVERSION")
print("=" * 50)
print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")
print(f"Output  : {csv_file}")
print("=" * 50)