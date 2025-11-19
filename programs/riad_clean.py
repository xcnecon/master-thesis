import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

df = df[df['average_interest_bearing_deposit'] > 0]

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

df = df.dropna(subset=['d_interest_rate_on_deposit',
                       'd_interest_rate_on_interest_bearing_deposit',
                       'd_average_deposit',
                       'd_average_interest_bearing_deposit'])

df = df[['rssd9001', 'rssd9999', 'rssd9050',
         'interest_rate_on_deposit', 'interest_rate_on_interest_bearing_deposit',
         'average_deposit', 'average_interest_bearing_deposit',
         'd_interest_rate_on_deposit', 'd_interest_rate_on_interest_bearing_deposit',
         'd_average_deposit', 'd_average_interest_bearing_deposit']]
df.to_csv("data/processed/deposit_interest_rate.csv", index=False)

# Plot: aggregate rates (sum interest / sum deposits) to reduce outliers
# Reconstruct total interest from rates and averages to avoid carrying raw interest column
df['_implied_interest'] = (df['interest_rate_on_deposit'] * df['average_deposit']) / 4
ts_weighted = df.groupby('rssd9999', as_index=False).agg(
    total_interest=('_implied_interest', 'sum'),
    total_avg_deposit=('average_deposit', 'sum'),
    total_avg_interest_bearing=('average_interest_bearing_deposit', 'sum'),
)
ts_weighted['weighted_interest_rate_on_deposit'] = (ts_weighted['total_interest'] / ts_weighted['total_avg_deposit']) * 4
ts_weighted['weighted_interest_rate_on_interest_bearing_deposit'] = (ts_weighted['total_interest'] / ts_weighted['total_avg_interest_bearing']) * 4
ts_weighted.sort_values('rssd9999', inplace=True)

# Also create a combined figure with weighted vs simple-average side-by-side
ts_rates_input = df[['rssd9001', 'rssd9999', 'interest_rate_on_deposit', 'interest_rate_on_interest_bearing_deposit']].copy()
per_bank_rates = ts_rates_input.groupby(['rssd9001', 'rssd9999'], as_index=False).mean(numeric_only=True)
ts_simple = per_bank_rates.groupby('rssd9999', as_index=False).mean(numeric_only=True)
ts_simple.sort_values('rssd9999', inplace=True)

# Winsorize per-date simple averages (0.5% / 99.5%) before plotting
winsor_cols = ['interest_rate_on_deposit', 'interest_rate_on_interest_bearing_deposit']
per_bank_w = per_bank_rates.copy()
for col in winsor_cols:
    lower = per_bank_w.groupby('rssd9999')[col].transform(lambda s: s.quantile(0.005))
    upper = per_bank_w.groupby('rssd9999')[col].transform(lambda s: s.quantile(0.995))
    per_bank_w[col] = per_bank_w[col].clip(lower=lower, upper=upper)
ts_simple_w = per_bank_w.groupby('rssd9999', as_index=False).mean(numeric_only=True)
ts_simple_w.sort_values('rssd9999', inplace=True)

fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharex=True, sharey=True)

# Left: weighted aggregate
axes[0].plot(ts_weighted['rssd9999'], ts_weighted['weighted_interest_rate_on_deposit'], label='Weighted: all deposits')
axes[0].plot(ts_weighted['rssd9999'], ts_weighted['weighted_interest_rate_on_interest_bearing_deposit'], label='Weighted: interest-bearing')
axes[0].set_title('Aggregate (sum interest / sum deposits)')
axes[0].set_xlabel('Date')
axes[0].set_ylabel('Annualized rate')
axes[0].grid(True, alpha=0.3)
axes[0].legend()

# Right: winsorized simple average across banks
axes[1].plot(ts_simple_w['rssd9999'], ts_simple_w['interest_rate_on_deposit'], label='Winsorized simple avg: all deposits')
axes[1].plot(ts_simple_w['rssd9999'], ts_simple_w['interest_rate_on_interest_bearing_deposit'], label='Winsorized simple avg: interest-bearing')
axes[1].set_title('Winsorized simple average across banks')
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Annualized rate')
axes[1].tick_params(axis='y', labelleft=True)
axes[1].grid(True, alpha=0.3)
axes[1].legend()

fig.suptitle('Deposit interest rates over time')
fig.tight_layout()
fig.savefig("data/processed/deposit_interest_rates_timeseries_combined.png", dpi=150)