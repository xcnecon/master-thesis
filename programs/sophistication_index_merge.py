import pandas as pd
import numpy as np

acs = pd.read_csv("data/raw/ACS.csv")
irs = pd.read_csv("data/raw/IRS.csv")
hmda = pd.read_csv("data/raw/HMDA.csv")

hmda["fips5"] = hmda["fips5"].str[2:]
hmda.loc[hmda["orig_total"] <= 20, "refi_share"] = pd.NA
hmda.rename(columns={"fips5": "fips"}, inplace=True)
na_pct = hmda["refi_share"].isna().mean() * 100
print(f"refi_share NA counties: {na_pct:.2f}% ({hmda['refi_share'].isna().sum()} of {len(hmda)})")
med_refi = pd.to_numeric(hmda["refi_share"], errors="coerce").median()
hmda["refi_share"] = hmda["refi_share"].fillna(med_refi)

df = acs.merge(irs, on="fips", how="inner")
df['fips'] = df['fips'].astype(str).str.zfill(5)
df = df.merge(hmda, on="fips", how="inner")
df = df[df['state_fips_x'] != '72'] 
df.drop(columns=['state_abbr', 'state_fips_y', 'county_fips_y', 'county_name'], inplace=True)

df['median_hh_income'] = np.log(df['median_hh_income'])
df['median_hh_income_z'] = (df['median_hh_income'] - df['median_hh_income'].mean()) / df['median_hh_income'].std()
df['share_ba_plus_z'] = (df['share_ba_plus'] - df['share_ba_plus'].mean()) / df['share_ba_plus'].std()
df['share_age_65plus_z'] = (df['share_age_65plus'] - df['share_age_65plus'].mean()) / df['share_age_65plus'].std()
df['share_internet_sub_z'] = (df['share_internet_sub'] - df['share_internet_sub'].mean()) / df['share_internet_sub'].std()
df['share_dividend_z'] = (df['share_dividend'] - df['share_dividend'].mean()) / df['share_dividend'].std()
df['share_interest_z'] = (df['share_interest'] - df['share_interest'].mean()) / df['share_interest'].std()
df['refi_share_z'] = (df['refi_share'] - df['refi_share'].mean()) / df['refi_share'].std()

FEATURE_COLUMNS = [
    "median_hh_income_z",
    "share_ba_plus_z",
    "share_age_65plus_z",
    "share_internet_sub_z",
    "share_dividend_z",
    "share_interest_z",
    "refi_share_z",
]

# PCA on z-scored features
work = df.dropna(subset=FEATURE_COLUMNS).copy()
X = work[FEATURE_COLUMNS].to_numpy(dtype=float)
X_centered = X - X.mean(axis=0, keepdims=True)
U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)
n = X_centered.shape[0]
eigvals = (S ** 2) / (n - 1)
explained_ratio = eigvals / eigvals.sum()
components = Vt.T
scores = X_centered @ components
loadings = components * np.sqrt(eigvals.reshape(1, -1))
pc_cols = [f"PC{i+1}" for i in range(scores.shape[1])]

scores_df = pd.DataFrame(scores, columns=pc_cols, index=work.index)
scores_df.insert(0, "fips", work["fips"].astype(str).values)
scores_df.to_csv("data/processed/sophistication_index_pca_scores.csv", index=False)

loadings_df = pd.DataFrame(loadings, index=FEATURE_COLUMNS, columns=pc_cols).reset_index()
loadings_df = loadings_df.rename(columns={"index": "variable"})
loadings_df.to_csv("data/processed/sophistication_index_pca_loadings.csv", index=False)

explained_df = pd.DataFrame({"component": pc_cols, "explained_variance_ratio": explained_ratio})
explained_df.to_csv("data/processed/sophistication_index_pca_explained_variance.csv", index=False)

# Keep PC1 and PC2 in the main df
df = df.merge(scores_df[["fips","PC1","PC2"]], on="fips", how="left")
df['sophistication_index'] = -df['PC1']

df.to_csv("data/processed/sophistication_index.csv", index=False)
