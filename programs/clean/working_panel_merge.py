"""
Builds the working panel by merging deposit rates, bank credit, instruments, and FFR.

Sources and citations:
- Effective Federal Funds Rate: Board of Governors H.15 Selected Interest Rates
  (via FRED series 'DFF').
- Bank-level variables and BKCLASS: FFIEC Call Report data. BKCLASS codes
  'N' (National), 'NM' (State nonmember), 'SM' (State member) denote commercial banks.
- Regional shares and instruments: constructed from FDIC Summary of Deposits (SOD).
"""
import pandas as pd
import numpy as np

# File paths
PROC_DIR = "data/processed"
WORK_DIR = "data/working"
DEPOSIT_INTEREST_RATE_CSV = f"{PROC_DIR}/deposit_interest_rate.csv"
BANK_CREDIT_CSV = f"{PROC_DIR}/bank_credit.csv"
INSTRUMENTS_CSV = f"{PROC_DIR}/instruments.csv"
FFR_CSV = f"{PROC_DIR}/ffr_quarterly.csv"
CONTROLS_CSV = f"{PROC_DIR}/controls.csv"
OUTPUT_CSV = f"{WORK_DIR}/working_panel.csv"

# Constants
ASSET_LARGE_THRESHOLD = 1_000_000
OUTLIER_Q_LOW = 0.01
OUTLIER_Q_HIGH = 0.99
Z_LIMIT = 10
COMMERCIAL_BKCLASS = {'N', 'NM', 'SM'}
DATE_START = "2022-01-01"
DATE_END = "2023-9-30"

def main() -> None:
    # Load inputs
    deposit_interest_rate = pd.read_csv(DEPOSIT_INTEREST_RATE_CSV)
    bank_credit = pd.read_csv(BANK_CREDIT_CSV)
    instruments = pd.read_csv(INSTRUMENTS_CSV)
    controls = pd.read_csv(
        CONTROLS_CSV,
        usecols=['rssd9001', 'rssd9999', 'metro_dummy', 'log_median_hh_income']
    )  # only needed fields

    # Merge core inputs
    df = deposit_interest_rate.merge(
        bank_credit, on=['rssd9001', 'rssd9999', 'rssd9050'], how='left'
    )
    instruments = instruments[
        ['RSSDID', 'sophistication_index_z', 'ASSET', 'BKCLASS',
         'hhi_z', 'branch_density_z', 'NE', 'MA', 'EC', 'WC', 'SA', 'ES', 'WS', 'MT', 'PC']
    ]
    instruments.rename(columns={'RSSDID': 'rssd9001'}, inplace=True)
    df = df.merge(instruments, on=['rssd9001'], how='left')
    df = df.merge(controls, on=['rssd9001', 'rssd9999'], how='left')
    # Harmonize identifiers
    df.rename(columns={'rssd9001': 'Bank ID', 'rssd9999': 'Date'}, inplace=True)
    df.drop(columns=['rssd9050', 'rssdfininstfilingtype'], inplace=True)

    # Build masks up-front (avoid sequential clipping)
    mask_rates_present = (
        ~df['interest_rate_on_deposit'].isna()
        & ~df['interest_rate_on_interest_bearing_deposit'].isna()
    )

    # Set missing deltas to zero (true zeros or missing changes)
    df['d_multifamily_loans'] = df['d_multifamily_loans'].fillna(0)
    df['d_single_family_loans'] = df['d_single_family_loans'].fillna(0)
    df['d_total_loans'] = df['d_total_loans'].fillna(0)
    df['d_total_loans_not_for_sale'] = df['d_total_loans_not_for_sale'].fillna(0)
    df['d_C&I'] = df['d_C&I'].fillna(0)

    # Small business lending flag (semi-annual) → carry forward last available within bank
    df.sort_values(['Bank ID', 'Date'], inplace=True)
    last_flag = df.groupby('Bank ID')['small_buz_lending_flag'].ffill()
    df['small_buz_lending_flag_asof'] = np.where(last_flag.fillna(0) == 1, 1, 0)
    df.drop(columns=['small_buz_lending_flag'], inplace=True)

    # Require instrument availability (mask only for now)
    mask_instrument_available = ~df['sophistication_index_z'].isna()

    # Commercial bank flag based on BKCLASS
    # See FFIEC Call Report documentation for BKCLASS codes.
    df['is_commercial_bank'] = np.where(df['BKCLASS'].isin(COMMERCIAL_BKCLASS), 1, 0)
    df.drop(columns=['BKCLASS'], inplace=True)
    mask_commercial_bank = df['is_commercial_bank'] == 1
    
    # # Generate lag-1 for all control variables (from controls.csv) - disabled
    # control_variables = [c for c in controls.columns if c not in ['rssd9001', 'rssd9999']]
    # control_variables = [c for c in control_variables if c in df.columns]
    # lagged_controls = df.groupby('Bank ID')[control_variables].shift(1)
    # lagged_controls.columns = [f"lag1_{c}" for c in control_variables]
    # df = pd.concat([df, lagged_controls], axis=1)
    
    # Policy window mask (do not filter yet)
    mask_policy_window = (df['Date'] >= DATE_START) & (df['Date'] <= DATE_END)
    
    # Base mask used to compute quantiles and for reporting
    base_mask = mask_rates_present & mask_instrument_available & mask_commercial_bank & mask_policy_window
    
    # Count before winsorizing
    print('Bank-quarter before winsorizing: ', int(base_mask.sum()))
    
    # Drop outliers in rate series using 0.5% / 99.5% thresholds
    low_dep = df.loc[base_mask, 'interest_rate_on_deposit'].quantile(OUTLIER_Q_LOW)
    high_dep = df.loc[base_mask, 'interest_rate_on_deposit'].quantile(OUTLIER_Q_HIGH)
    low_ib = df.loc[base_mask, 'interest_rate_on_interest_bearing_deposit'].quantile(OUTLIER_Q_LOW)
    high_ib = df.loc[base_mask, 'interest_rate_on_interest_bearing_deposit'].quantile(OUTLIER_Q_HIGH)
    mask_rate_range = (
        (df['interest_rate_on_deposit'] >= low_dep) & (df['interest_rate_on_deposit'] <= high_dep) &
        (df['interest_rate_on_interest_bearing_deposit'] >= low_ib) & (df['interest_rate_on_interest_bearing_deposit'] <= high_ib)
    )

    # Keep z-scores strictly within [-Z_LIMIT, Z_LIMIT]
    mask_z_scores = (
        df['sophistication_index_z'].between(-Z_LIMIT, Z_LIMIT) &
        df['hhi_z'].between(-Z_LIMIT, Z_LIMIT) &
        df['branch_density_z'].between(-Z_LIMIT, Z_LIMIT)
    )
    
    # Apply all masks at once
    all_masks = base_mask & mask_rate_range & mask_z_scores
    df = df[all_masks].copy()
    df.drop(columns=['is_commercial_bank'], inplace=True)

    # Bank-level flag: 1 if the bank is present in the first quarter of the sample
    first_quarter_date = df['Date'].min()
    df['in_first_quarter'] = (df.groupby('Bank ID')['Date'].transform('min') == first_quarter_date).astype(int)

    # Cumulative changes in bank deposit rates, analogous to cum_d_ffr, only for banks in first quarter
    df.sort_values(['Bank ID', 'Date'], inplace=True)
    cum_dep = df.groupby('Bank ID')['d_interest_rate_on_deposit'].apply(lambda s: s.fillna(0).cumsum())
    cum_ib = df.groupby('Bank ID')['d_interest_rate_on_interest_bearing_deposit'].apply(lambda s: s.fillna(0).cumsum())
    df['cum_d_interest_rate_on_deposit'] = np.where(df['in_first_quarter'] == 1, cum_dep, np.nan)
    df['cum_d_interest_rate_on_interest_bearing_deposit'] = np.where(df['in_first_quarter'] == 1, cum_ib, np.nan)

    # Merge FFR and keep policy window
    ffr = pd.read_csv(FFR_CSV)
    df = df.merge(ffr, on=['Date'], how='left')

    # Large bank indicator (size threshold)
    df['large_bank'] = np.where(df['ASSET'] > ASSET_LARGE_THRESHOLD, 1, 0)
    df.drop(columns=['ASSET'], inplace=True)

    # # Winsorize ROA and asset_to_equity at 0.5% / 99.5%; cap core_deposit_share below 1 - disabled
    # low_roa = df['ROA'].quantile(OUTLIER_Q_LOW)
    # high_roa = df['ROA'].quantile(OUTLIER_Q_HIGH)
    # df['ROA'] = df['ROA'].clip(lower=low_roa, upper=high_roa)

    # low_ae = df['asset_to_equity'].quantile(OUTLIER_Q_LOW)
    # high_ae = df['asset_to_equity'].quantile(OUTLIER_Q_HIGH)
    # df['asset_to_equity'] = df['asset_to_equity'].clip(lower=low_ae, upper=high_ae)

    # df['core_deposit_share'] = np.minimum(df['core_deposit_share'], 0.999)

    # # Drop contemporaneous control variables if still present - disabled
    # contemporaneous_controls = ['ROA', 'core_deposit_share', 'wholesale_share', 'asset_to_equity', 'log_asset']
    # to_drop = [c for c in contemporaneous_controls if c in df.columns]
    # if len(to_drop) > 0:
    #     df.drop(columns=to_drop, inplace=True)
    
    # Count after winsorizing
    print('Bank-quarter after winsorizing: ', len(df))
    print('Large bank: ', len(df[df['large_bank'] == 1]))
    print('Small bank: ', len(df[df['large_bank'] == 0]))

    # Save
    df.to_csv(OUTPUT_CSV, index=False)


if __name__ == "__main__":
    main()