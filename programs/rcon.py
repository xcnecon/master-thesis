import pandas as pd
import numpy as np

rcon1 = pd.read_csv("data/raw/rcon_credit_1.csv", parse_dates=["rssd9999"])
# Ensure consistent date format for merge key
rcon1['rssd9999'] = pd.to_datetime(rcon1['rssd9999'], errors='coerce').dt.normalize()

# De-dupe by keys, keeping the latest submission by date
rcon1['rssdsubmissiondate'] = pd.to_datetime(rcon1['rssdsubmissiondate'], errors='coerce')
rcon1.sort_values(['rssd9001', 'rssd9999', 'rssd9050', 'rssdsubmissiondate'], inplace=True)
rcon1 = rcon1.drop_duplicates(subset=['rssd9001', 'rssd9999', 'rssd9050'], keep='last')
rcon1.drop(columns=['rssdsubmissiondate'], inplace=True)

rcon2 = pd.read_csv("data/raw/rcon_credit_2.csv", parse_dates=["rssd9999"])
rcon2['rssd9999'] = pd.to_datetime(rcon2['rssd9999'], errors='coerce').dt.normalize()
rcon2['rssdsubmissiondate'] = pd.to_datetime(rcon2['rssdsubmissiondate'], errors='coerce')
rcon2.sort_values(['rssd9001', 'rssd9999', 'rssd9050', 'rssdsubmissiondate'], inplace=True)
rcon2 = rcon2.drop_duplicates(subset=['rssd9001', 'rssd9999', 'rssd9050'], keep='last')
rcon2.drop(columns=['rssdsubmissiondate'], inplace=True)

# Merge on rssd9001 and rssd9999 after de-duplication (column exists in both)
df = rcon1.merge(rcon2, on=["rssd9001", "rssd9050", "rssd9999"], how="left")
df.drop(columns=['rcon5569', 'rcon5573', 'rcon5567', 'rcon5575', 'rcon5571', 'rcon5565'], inplace=True)

df.rename(columns={'rcon3465': 'single_family_loans', 'rcon1460': 'multifamily_loans', 'rcon2122': 'total_loans', 'rcon1766':'C&I', 'rconb528':'total_loans_not_for_sale', 'rcon6999':'small_buz_lending_flag'}, inplace=True)

# Ensure chronological order for QoQ computations
df.sort_values(['rssd9001', 'rssd9999', 'rssd9050'], inplace=True)

# Compute QoQ pct change for requested variables
qoq_cols = ['single_family_loans', 'multifamily_loans', 'total_loans', 'total_loans_not_for_sale', 'C&I']
for col in qoq_cols:
    prev = df.groupby('rssd9001')[col].shift(1)
    df[f'd_{col}'] = np.where(prev != 0, (df[col] - prev) / prev, np.nan)

df.drop(columns=['single_family_loans', 'multifamily_loans', 'total_loans', 'total_loans_not_for_sale', 'C&I'], inplace=True)

df.to_csv("data/processed/bank_credit.csv", index=False)