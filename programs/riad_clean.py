import pandas as pd
import numpy as np

riad = pd.read_csv("data/raw/riad.csv")

# Ensure consistent date format for merge key
riad['rssd9999'] = pd.to_datetime(riad['rssd9999'], errors='coerce').dt.normalize()

# De-dupe by keys, keeping the latest submission by date
riad['rssdsubmissiondate'] = pd.to_datetime(riad['rssdsubmissiondate'], errors='coerce')
riad.sort_values(['rssd9001', 'rssd9999', 'rssd9050', 'rssdsubmissiondate'], inplace=True)
riad = riad.drop_duplicates(subset=['rssd9001', 'rssd9999', 'rssd9050'], keep='last')

# Convert YTD interest items to quarterly amounts (per bank, per year)
riad.sort_values(['rssd9001', 'rssd9050', 'rssd9999'], inplace=True)
ytd_cols = ['riad4508', 'riad0093', 'riadhk04', 'riadhk03']
for col in ytd_cols:
    ytd_diff = riad.groupby(['rssd9001', 'rssd9050', riad['rssd9999'].dt.year])[col].diff()
    riad[col] = ytd_diff.where(~ytd_diff.isna(), riad[col])

# Now sum quarterly amounts
riad['interest_on_deposit'] = riad['riad4508'] + riad['riad0093'] + riad['riadhk04'] + riad['riadhk03']

rcon = pd.read_csv("data/raw/rcon_deposit.csv")

# Ensure consistent date format for merge key
rcon['rssd9999'] = pd.to_datetime(rcon['rssd9999'], errors='coerce').dt.normalize()

# De-dupe by keys, keeping the latest submission by date
rcon['rssdsubmissiondate'] = pd.to_datetime(rcon['rssdsubmissiondate'], errors='coerce')
rcon.sort_values(['rssd9001', 'rssd9999', 'rssd9050', 'rssdsubmissiondate'], inplace=True)
rcon = rcon.drop_duplicates(subset=['rssd9001', 'rssd9999', 'rssd9050'], keep='last')

df = riad.merge(rcon, on=['rssd9001', 'rssd9999', 'rssd9050'], how='left')

# Ensure chronological order within each bank for lag computation
df.sort_values(['rssd9001', 'rssd9999', 'rssd9050'], inplace=True)

# rcon2200 + rcon2200(-1) per bank
df['average_deposit'] = (df['rcon2200'] + df.groupby('rssd9001')['rcon2200'].shift(1)) / 2

# rcon6636 + rcon6636(-1) per bank
df['average_interest_bearing_deposit'] = (df['rcon6636'] + df.groupby('rssd9001')['rcon6636'].shift(1)) / 2

df['interest_rate_on_deposit'] = df['interest_on_deposit'] / df['average_deposit'] * 4
df['interest_rate_on_interest_bearing_deposit'] = df['interest_on_deposit'] / df['average_interest_bearing_deposit'] * 4

# Compute per-bank quarterly changes and drop NA
df['d_interest_rate_on_deposit'] = df.groupby('rssd9001')['interest_rate_on_deposit'].diff()
df['d_interest_rate_on_interest_bearing_deposit'] = df.groupby('rssd9001')['interest_rate_on_interest_bearing_deposit'].diff()
df['d_rcon2200'] = df.groupby('rssd9001')['rcon2200'].diff()
df['d_rcon6636'] = df.groupby('rssd9001')['rcon6636'].diff()

# Convert deposit diffs to relative changes by last quarter value (per bank)
prev_rcon2200 = df.groupby('rssd9001')['rcon2200'].shift(1)
prev_rcon6636 = df.groupby('rssd9001')['rcon6636'].shift(1)
df['d_rcon2200'] = np.where(prev_rcon2200 != 0, df['d_rcon2200'] / prev_rcon2200, np.nan)
df['d_rcon6636'] = np.where(prev_rcon6636 != 0, df['d_rcon6636'] / prev_rcon6636, np.nan)

# Rename to reflect average-deposit series
df.rename(columns={
    'd_rcon2200': 'd_average_deposit',
    'd_rcon6636': 'd_average_interest_bearing_deposit'
}, inplace=True)

df = df[['rssd9001', 'rssd9999', 'rssd9050',
         'interest_rate_on_deposit', 'interest_rate_on_interest_bearing_deposit',
         'average_deposit', 'average_interest_bearing_deposit',
         'd_interest_rate_on_deposit', 'd_interest_rate_on_interest_bearing_deposit',
         'd_average_deposit', 'd_average_interest_bearing_deposit']]
df.to_csv("data/processed/deposit_interest_rate.csv", index=False)