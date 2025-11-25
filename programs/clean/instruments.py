"""Builds a bank-level panel combining county sophistication and deposit concentration measures.

Inputs
- data/raw/SOD.csv: FDIC SOD extract with at least YEAR, RSSDID, NAMEFULL, ASSET, BKCLASS,
  DEPDOM (bank total domestic deposits), DEPSUMBR (branch deposits), STCNTYBR (county FIPS).
- data/processed/sophistication_index.csv: county-level sophistication index with 'fips'.

Output
- data/processed/instruments.csv: one row per (YEAR, RSSDID) including z-scored sophistication
  and HHI exposures.

Notes
- Branch weights use DEPSUMBR / DEPDOM and are renormalized when some counties lack an index.
- County HHI is on [0, 1] (not multiplied by 10,000).
- The retained 'fips' in the final dataframe corresponds to an arbitrary branch; drop if undesired.
"""
import pandas as pd
import numpy as np

# Build a bank-level dataset with:
# - County sophistication index merged by county FIPS (from precomputed file)
# - Bank-level weighted sophistication index (weights = branch deposits / bank total deposits)
# - County-level deposit HHI (Herfindahl-Hirschman Index) computed within each county-year
# - Bank-level exposure to county HHI (deposit-weighted average of county HHIs across a bank's footprint)
# - Bank-level branch density (number of branches per $1B of DEPDOM)

# State (USPS) -> Census Division name
STATE_TO_CENSUS_DIVISION = {
    # 1) New England
    "CT": "New England", "ME": "New England", "MA": "New England",
    "NH": "New England", "RI": "New England", "VT": "New England",
    # 2) Middle Atlantic
    "NJ": "Middle Atlantic", "NY": "Middle Atlantic", "PA": "Middle Atlantic",
    # 3) East North Central
    "IL": "East North Central", "IN": "East North Central", "MI": "East North Central",
    "OH": "East North Central", "WI": "East North Central",
    # 4) West North Central
    "IA": "West North Central", "KS": "West North Central", "MN": "West North Central",
    "MO": "West North Central", "NE": "West North Central", "ND": "West North Central",
    "SD": "West North Central",
    # 5) South Atlantic (includes DC)
    "DE": "South Atlantic", "DC": "South Atlantic", "FL": "South Atlantic",
    "GA": "South Atlantic", "MD": "South Atlantic", "NC": "South Atlantic",
    "SC": "South Atlantic", "VA": "South Atlantic", "WV": "South Atlantic",
    # 6) East South Central
    "AL": "East South Central", "KY": "East South Central",
    "MS": "East South Central", "TN": "East South Central",
    # 7) West South Central
    "AR": "West South Central", "LA": "West South Central",
    "OK": "West South Central", "TX": "West South Central",
    # 8) Mountain
    "AZ": "Mountain", "CO": "Mountain", "ID": "Mountain", "MT": "Mountain",
    "NV": "Mountain", "NM": "Mountain", "UT": "Mountain", "WY": "Mountain",
    # 9) Pacific
    "AK": "Pacific", "CA": "Pacific", "HI": "Pacific", "OR": "Pacific", "WA": "Pacific",
}
DIVISION_NAMES = [
    "New England",
    "Middle Atlantic",
    "East North Central",
    "West North Central",
    "South Atlantic",
    "East South Central",
    "West South Central",
    "Mountain",
    "Pacific",
]
# FIPS (2-digit string) -> USPS
STATE_FIPS_TO_USPS = {
    "01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA",
    "08": "CO", "09": "CT", "10": "DE", "11": "DC", "12": "FL",
    "13": "GA", "15": "HI", "16": "ID", "17": "IL", "18": "IN",
    "19": "IA", "20": "KS", "21": "KY", "22": "LA", "23": "ME",
    "24": "MD", "25": "MA", "26": "MI", "27": "MN", "28": "MS",
    "29": "MO", "30": "MT", "31": "NE", "32": "NV", "33": "NH",
    "34": "NJ", "35": "NM", "36": "NY", "37": "NC", "38": "ND",
    "39": "OH", "40": "OK", "41": "OR", "42": "PA", "44": "RI",
    "45": "SC", "46": "SD", "47": "TN", "48": "TX", "49": "UT",
    "50": "VT", "51": "VA", "53": "WA", "54": "WV", "55": "WI",
    "56": "WY",
    # Territories (not mapped to divisions; will become NaN and be ignored)
    "60": "AS", "66": "GU", "69": "MP", "72": "PR", "78": "VI",
}

sod = pd.read_csv("data/raw/SOD.csv")
sophistication_index = pd.read_csv("data/processed/sophistication_index.csv")

# Keep only the columns required for this build (helps memory and ensures consistent inputs).
sod_mask = ['YEAR', 'RSSDID', 'NAMEFULL', 'ASSET', 'BKCLASS', 'DEPDOM', 'DEPSUMBR', 'STCNTYBR']
sod = sod[sod_mask]

sod['STCNTYBR'] = sod['STCNTYBR'].astype(str).str.zfill(5)  # standardize county FIPS format
sod.rename(columns={'STCNTYBR': 'fips'}, inplace=True)      # use a consistent 'fips' column

# Map branches to census divisions via state inferred from FIPS.
sod['state_fips'] = sod['fips'].str[:2]
sod['state_usps'] = sod['state_fips'].map(STATE_FIPS_TO_USPS)
sod['census_division'] = sod['state_usps'].map(STATE_TO_CENSUS_DIVISION)

# Branch weight = branch deposits / bank total domestic deposits.
# Summing weights across all branches of a bank yields ~1. For banks with missing or zero DEPDOM,
# weights will be NaN/inf and naturally drop out of later averages via the renormalization step.
sod['weight'] = sod['DEPSUMBR'] / sod['DEPDOM']

# Ensure FIPS is standardized to 5 digits in both sources and merge the county sophistication index.
sophistication_index['fips'] = sophistication_index['fips'].astype(str).str.zfill(5)
sod = sod.merge(sophistication_index[['fips', 'sophistication_index']], on='fips', how='left')

# Bank-level branch density BEFORE HHI: branches per $1B of DEPDOM.
# Count branches per (YEAR, RSSDID) and divide by bank DEPDOM (in billions).
branch_count = (
    sod.groupby(['YEAR', 'RSSDID'])
    .size()
    .reset_index(name='branch_count')
)

# DEPDOM in SOD is bank-level total domestic deposits (same for all branches of a bank-year),
# so we can safely take .first().
bank_depdom = sod.groupby(['YEAR', 'RSSDID'], as_index=False)['DEPDOM'].first()

branch_density_df = branch_count.merge(bank_depdom, on=['YEAR', 'RSSDID'], how='left')

# Convert DEPDOM to billions of dollars
branch_density_df['DEPDOM_bil'] = branch_density_df['DEPDOM'] / 1_000_000_000

# Branches per $1B of DEPDOM
branch_density_df['branch_density'] = np.where(
    branch_density_df['DEPDOM'] > 0,
    branch_density_df['branch_count'] / branch_density_df['DEPDOM_bil'],
    np.nan,
)

branch_density_df['branch_density'] = np.log(branch_density_df['branch_density'] + 1)

# Division deposit shares per bank-year: % of bank deposits in each census division (0–1).
# We compute as sum(DEPSUMBR in division) / DEPDOM for the bank-year.
division_deposits = (
    sod.dropna(subset=['census_division'])
    .groupby(['YEAR', 'RSSDID', 'census_division'], as_index=False)['DEPSUMBR']
    .sum()
    .rename(columns={'DEPSUMBR': 'division_deposits'})
)
division_share = division_deposits.merge(bank_depdom, on=['YEAR', 'RSSDID'], how='left')
division_share['division_share'] = (
    (division_share['division_deposits'] / division_share['DEPDOM']).where(division_share['DEPDOM'] > 0)
)
division_pivot = (
    division_share.pivot(index=['YEAR', 'RSSDID'], columns='census_division', values='division_share')
    .fillna(0)
    .reset_index()
)
# Ensure all 9 divisions are present as columns; if absent, create with 0.
for div_name in DIVISION_NAMES:
    if div_name not in division_pivot.columns:
        division_pivot[div_name] = 0.0
# Rename columns to two-character codes per division
DIVISION_CODE_MAP = {
    "New England": "NE",
    "Middle Atlantic": "MA",
    "East North Central": "EC",
    "West North Central": "WC",
    "South Atlantic": "SA",
    "East South Central": "ES",
    "West South Central": "WS",
    "Mountain": "MT",
    "Pacific": "PC",
}
division_pivot = division_pivot.rename(columns=DIVISION_CODE_MAP)

# Compute bank-level weighted sophistication index (by YEAR, RSSDID).
# We weight county sophistication by the bank's deposit distribution. Because some counties can
# be missing an index, we divide by the sum of weights with non-missing sophistication to re-scale.
valid = sod.dropna(subset=['sophistication_index']).copy()
valid['weighted_sophistication_component'] = valid['sophistication_index'] * valid['weight']
bank_agg = (
    valid.groupby(['YEAR', 'RSSDID'], as_index=False)
    .agg(
        bank_weight_sum=('weight', 'sum'),
        bank_weighted_sum=('weighted_sophistication_component', 'sum'),
    )
)
bank_agg['bank_weighted_sophistication_index'] = (
    bank_agg['bank_weighted_sum'] / bank_agg['bank_weight_sum']
).where(bank_agg['bank_weight_sum'] > 0)

# County-level deposit HHI using branch deposits within each county-year.
# HHI_county = sum_banks ( (bank deposits in county / total county deposits)^2 ), on [0, 1].
# 1) Sum branch deposits to bank-by-county totals
county_bank = (
    sod.groupby(['YEAR', 'fips', 'RSSDID'], as_index=False)['DEPSUMBR']
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

# Bank-level exposure to county HHI: deposit-weighted average of county HHIs across a bank's footprint.
# The weight per county is the bank's total branch-deposit share in that county (summing branch weights).
bank_county_weight = (
    sod.groupby(['YEAR', 'RSSDID', 'fips'], as_index=False)['weight']
    .sum()
    .rename(columns={'weight': 'bank_county_weight'})
)
bank_hhi = bank_county_weight.merge(county_hhi, on=['YEAR', 'fips'], how='left')
bank_hhi['weighted_hhi_component'] = bank_hhi['bank_county_weight'] * bank_hhi['county_deposit_hhi']
bank_hhi = (
    bank_hhi.groupby(['YEAR', 'RSSDID'], as_index=False)
    .agg(sum_w=('bank_county_weight', 'sum'), sum_ws=('weighted_hhi_component', 'sum'))
)
bank_hhi['bank_weighted_county_deposit_hhi'] = (
    bank_hhi['sum_ws'] / bank_hhi['sum_w']
).where(bank_hhi['sum_w'] > 0)

# Build bank-level dataframe: one row per (YEAR, RSSDID), dropping branch-only columns.
# We keep the first occurrence for identifier columns (e.g., NAMEFULL, ASSET, BKCLASS, DEPDOM).
# Any 'fips' retained here corresponds to one arbitrary branch row and is not bank-level.
df_base = sod.drop(columns=['DEPSUMBR', 'weight'])
df = (
    df_base.sort_values(['YEAR', 'RSSDID'])
    .drop_duplicates(['YEAR', 'RSSDID'])
)
df = df.merge(
    bank_agg[['YEAR', 'RSSDID', 'bank_weighted_sophistication_index']],
    on=['YEAR', 'RSSDID'],
    how='left'
)
df = df.merge(
    bank_hhi[['YEAR', 'RSSDID', 'bank_weighted_county_deposit_hhi']],
    on=['YEAR', 'RSSDID'],
    how='left'
)
df = df.merge(
    branch_density_df[['YEAR', 'RSSDID', 'branch_density']],
    on=['YEAR', 'RSSDID'],
    how='left'
)
df = df.merge(
    division_pivot[['YEAR', 'RSSDID'] + list(DIVISION_CODE_MAP.values())],
    on=['YEAR', 'RSSDID'],
    how='left'
)

df.drop(columns=['sophistication_index'], inplace=True)

# Standardize SI and HHI across all bank-year observations (z-scores).
# Columns are renamed to *_z and then z-scored. If a series is constant (std=0), the result is NaN.
df.rename(columns={'bank_weighted_sophistication_index': 'sophistication_index_z', 'bank_weighted_county_deposit_hhi': 'hhi_z', 'branch_density': 'branch_density_z'}, inplace=True)
df['sophistication_index_z'] = (df['sophistication_index_z'] - df['sophistication_index_z'].mean()) / df['sophistication_index_z'].std()
df['hhi_z'] = (df['hhi_z'] - df['hhi_z'].mean()) / df['hhi_z'].std()
df['branch_density_z'] = (df['branch_density_z'] - df['branch_density_z'].mean()) / df['branch_density_z'].std()

# Write the final panel.
df.to_csv("data/processed/instruments.csv", index=False)