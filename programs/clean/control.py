import pandas as pd
import numpy as np

rcon1 = pd.read_csv("data/raw/rcon_control_1.csv", parse_dates=["rssd9999"])
# De-dupe by keys, keeping the latest submission by date
rcon1['rssdsubmissiondate'] = pd.to_datetime(rcon1['rssdsubmissiondate'], errors='coerce')
rcon1.sort_values(['rssd9001', 'rssd9999', 'rssdsubmissiondate'], inplace=True)
rcon1 = rcon1.drop_duplicates(subset=['rssd9001', 'rssd9999'], keep='last')
rcon1.drop(columns=['rssdsubmissiondate'], inplace=True)

rcon2 = pd.read_csv("data/raw/rcon_control_2.csv", parse_dates=["rssd9999"])
rcon2['rssdsubmissiondate'] = pd.to_datetime(rcon2['rssdsubmissiondate'], errors='coerce')
rcon2.sort_values(['rssd9001', 'rssd9999', 'rssdsubmissiondate'], inplace=True)
rcon2 = rcon2.drop_duplicates(subset=['rssd9001', 'rssd9999'], keep='last')
rcon2.drop(columns=['rssdsubmissiondate'], inplace=True)

riad = pd.read_csv("data/raw/riad_control.csv", parse_dates=["rssd9999"])
riad['rssdsubmissiondate'] = pd.to_datetime(riad['rssdsubmissiondate'], errors='coerce')
riad.sort_values(['rssd9001', 'rssd9999', 'rssdsubmissiondate'], inplace=True)
riad = riad.drop_duplicates(subset=['rssd9001', 'rssd9999'], keep='last')
riad.drop(columns=['rssdsubmissiondate'], inplace=True)

df = rcon1.merge(rcon2, on=["rssd9001", "rssd9999"], how="left")
df = df.merge(riad, on=["rssd9001", "rssd9999"], how="left")

df['ROA'] = df['riad4340'] / df['rcon2170']
df['core_deposit_share'] = (df['rcon2210'] + df['rcon0352'] + df['rcon6810'] + df['rconj473'] + df['rcon6648']) / df['rcon2170']
df['wholesale_share'] = (df['rcon3353'] + df['rcon3200'] + df['rconj474'] + df['rcon3190']) / df['rcon2170']
df['asset_to_equity'] = df['rcon2170'] / df['rcon3210']
df['log_asset'] = np.log(df['rcon2170'])

df = df[['rssd9001', 'rssd9999', 'ROA', 'core_deposit_share', 'wholesale_share', 'asset_to_equity', 'log_asset']]


# Calculate bank deposit-weighted county-level household income and urban dummy
acs = pd.read_csv("data/raw/ACS.csv")
sod = pd.read_csv("data/raw/SOD.csv")

# Keep only necessary SOD columns and construct branch weights
sod_w = sod[['YEAR', 'RSSDID', 'DEPDOM', 'DEPSUMBR', 'STCNTYBR', 'METROBR']].copy()
sod_w['fips'] = sod_w['STCNTYBR'].astype(str).str.zfill(5)
# Avoid divide-by-zero; weights where DEPDOM <= 0 will propagate as NaN and be dropped in sums
sod_w['weight'] = sod_w['DEPSUMBR'] / sod_w['DEPDOM']

# Ensure ACS FIPS standardized
acs_w = acs[['fips', 'median_hh_income']].copy()
acs_w['fips'] = acs_w['fips'].astype(str).str.zfill(5)

# Deposit-weighted METROBR per (YEAR, RSSDID)
metro = sod_w.dropna(subset=['weight', 'METROBR']).copy()
metro['w_var'] = metro['weight'] * metro['METROBR']
metro_agg = (
    metro.groupby(['YEAR', 'RSSDID'], as_index=False)
    .agg(sum_w=('weight', 'sum'), sum_wy=('w_var', 'sum'))
)
metro_agg['deposit_weighted_metrobr'] = (metro_agg['sum_wy'] / metro_agg['sum_w']).where(metro_agg['sum_w'] > 0)
metro_agg = metro_agg[['YEAR', 'RSSDID', 'deposit_weighted_metrobr']]

# Deposit-weighted county median household income per (YEAR, RSSDID)
sod_acs = sod_w.merge(acs_w, on='fips', how='left')
income = sod_acs.dropna(subset=['weight', 'median_hh_income']).copy()
income['w_var'] = income['weight'] * income['median_hh_income']
income_agg = (
    income.groupby(['YEAR', 'RSSDID'], as_index=False)
    .agg(sum_w=('weight', 'sum'), sum_wy=('w_var', 'sum'))
)
income_agg['deposit_weighted_median_hh_income'] = (income_agg['sum_wy'] / income_agg['sum_w']).where(income_agg['sum_w'] > 0)
income_agg = income_agg[['YEAR', 'RSSDID', 'deposit_weighted_median_hh_income']]

# Combine and keep the most recent SOD YEAR per bank
exposures = metro_agg.merge(income_agg, on=['YEAR', 'RSSDID'], how='outer')
exposures.sort_values(['RSSDID', 'YEAR'], inplace=True)
latest_exposures = exposures.groupby('RSSDID', as_index=False).tail(1)
latest_exposures.rename(columns={'RSSDID': 'rssd9001'}, inplace=True)

# Merge deposit-weighted exposures onto bank-quarter controls (repeat across quarters)
df = df.merge(
    latest_exposures[['rssd9001', 'deposit_weighted_metrobr', 'deposit_weighted_median_hh_income']],
    on='rssd9001',
    how='left'
)

df['log_median_hh_income'] = np.log(df['deposit_weighted_median_hh_income'])
df['log_median_hh_income_z'] = (df['log_median_hh_income'] - df['log_median_hh_income'].mean()) / df['log_median_hh_income'].std()
df.drop(columns=['deposit_weighted_median_hh_income'], inplace=True)

df.rename(columns={'deposit_weighted_metrobr': 'metro_dummy'}, inplace=True)

df.to_csv("data/processed/controls.csv", index=False)