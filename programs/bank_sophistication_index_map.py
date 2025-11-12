import pandas as pd

# Build a bank-level dataset with:
# - County sophistication index merged by county FIPS (from precomputed file)
# - Bank-level weighted sophistication index (weights = branch deposits / bank total deposits)
# - County-level deposit HHI (Herfindahl-Hirschman Index) computed within each county-year
# - Bank-level exposure to county HHI (deposit-weighted average of county HHIs across a bank's footprint)

sod = pd.read_csv("data/raw/SOD.csv")
sophistication_index = pd.read_csv("data/processed/sophistication_index.csv")

sod_mask = ['YEAR', 'CERT', 'NAMEFULL', 'ASSET', 'BKCLASS', 'DEPDOM', 'DEPSUMBR', 'STCNTYBR']
sod = sod[sod_mask]

sod['STCNTYBR'] = sod['STCNTYBR'].astype(str).str.zfill(5)  # standardize county FIPS format
sod.rename(columns={'STCNTYBR': 'fips'}, inplace=True)      # use a consistent 'fips' column

# Branch weight = branch deposits / bank total domestic deposits.
# Summing weights across all branches of a bank yields ~1 (subject to data consistency).
sod['weight'] = sod['DEPSUMBR'] / sod['DEPDOM']

# Ensure fips is standardized and merge sophistication index
sophistication_index['fips'] = sophistication_index['fips'].astype(str).str.zfill(5)
sod = sod.merge(sophistication_index[['fips', 'sophistication_index']], on='fips', how='left')

# Compute bank-level weighted sophistication index (by YEAR, CERT).
# We weight county sophistication by the bank's deposit distribution (sum of branch weights within each bank).
valid = sod.dropna(subset=['sophistication_index']).copy()
valid['weighted_sophistication_component'] = valid['sophistication_index'] * valid['weight']
bank_agg = (
    valid.groupby(['YEAR', 'CERT'], as_index=False)
    .agg(
        bank_weight_sum=('weight', 'sum'),
        bank_weighted_sum=('weighted_sophistication_component', 'sum'),
    )
)
bank_agg['bank_weighted_sophistication_index'] = (
    bank_agg['bank_weighted_sum'] / bank_agg['bank_weight_sum']
).where(bank_agg['bank_weight_sum'] > 0)

# County-level deposit HHI using branch deposits within each county:
# HHI_county = sum_banks ( (bank deposits in county / total county deposits)^2 )
# 1) Sum branch deposits to bank-by-county totals
county_bank = (
    sod.groupby(['YEAR', 'fips', 'CERT'], as_index=False)['DEPSUMBR']
    .sum()
    .rename(columns={'DEPSUMBR': 'bank_county_deposits'})
)
# 2) County total deposits (sum of all branches in county)
county_total = (
    sod.groupby(['YEAR', 'fips'], as_index=False)['DEPSUMBR']
    .sum()
    .rename(columns={'DEPSUMBR': 'county_total_deposits'})
)
# 3) Market shares and HHI per county
shares = county_bank.merge(county_total, on=['YEAR', 'fips'], how='left')
shares['county_share'] = shares['bank_county_deposits'] / shares['county_total_deposits']
shares['sq_share'] = shares['county_share'] ** 2
county_hhi = (
    shares.groupby(['YEAR', 'fips'], as_index=False)['sq_share']
    .sum()
    .rename(columns={'sq_share': 'county_deposit_hhi'})
)

# Bank-level exposure to county HHI: deposit-weighted average of county HHIs across a bank's counties.
bank_county_weight = (
    sod.groupby(['YEAR', 'CERT', 'fips'], as_index=False)['weight']
    .sum()
    .rename(columns={'weight': 'bank_county_weight'})
)
bank_hhi = bank_county_weight.merge(county_hhi, on=['YEAR', 'fips'], how='left')
bank_hhi['weighted_hhi_component'] = bank_hhi['bank_county_weight'] * bank_hhi['county_deposit_hhi']
bank_hhi = (
    bank_hhi.groupby(['YEAR', 'CERT'], as_index=False)
    .agg(sum_w=('bank_county_weight', 'sum'), sum_ws=('weighted_hhi_component', 'sum'))
)
bank_hhi['bank_weighted_county_deposit_hhi'] = (
    bank_hhi['sum_ws'] / bank_hhi['sum_w']
).where(bank_hhi['sum_w'] > 0)

# Build bank-level dataframe: one row per (YEAR, CERT), keeping previous columns except DEPSUMBR, weight.
# We keep the first occurrence for identifier-like columns (e.g., NAMEFULL, ASSET, BKCLASS, DEPDOM).
df_base = sod.drop(columns=['DEPSUMBR', 'weight'])
df = (
    df_base.sort_values(['YEAR', 'CERT'])
    .drop_duplicates(['YEAR', 'CERT'])
)
df = df.merge(
    bank_agg[['YEAR', 'CERT', 'bank_weighted_sophistication_index']],
    on=['YEAR', 'CERT'],
    how='left'
)
df = df.merge(
    bank_hhi[['YEAR', 'CERT', 'bank_weighted_county_deposit_hhi']],
    on=['YEAR', 'CERT'],
    how='left'
)

print(df.head())