import pandas as pd
import numpy as np
import os

df = pd.read_csv("data/working/working_panel.csv")

# First Paragraph
# Filter to 2022Q1 (quarter end date 2022-03-31)
quarter_end = "2022-03-31"
df_q1 = df[df["Date"] == quarter_end].copy()

# Basic counts
num_bank_quarters = len(df_q1)
num_banks = df_q1["Bank ID"].nunique()

# Asset statistics
assets = df_q1["ASSET"].dropna()
mean_asset = assets.mean()
median_asset = assets.median()

# Share of assets held by top decile (top 10% banks by ASSET)
if num_bank_quarters > 0:
    top_k = max(1, int(np.ceil(0.10 * num_bank_quarters)))
    top_assets_sum = assets.sort_values(ascending=False).head(top_k).sum()
    total_assets_sum = assets.sum()
    top_decile_share = (top_assets_sum / total_assets_sum) if total_assets_sum > 0 else np.nan
else:
    top_decile_share = np.nan

# Counts above and below threshold
threshold = 1_000_000
num_above = int((assets > threshold).sum())
num_below = int((assets < threshold).sum())

print(f"Quarter: 2022Q1 (Date: {quarter_end})")
print(f"Number of bank-quarters: {num_bank_quarters}")
print(f"Number of banks: {num_banks}")
print(f"Mean ASSET: {mean_asset*1000:,.0f}")
print(f"Median ASSET: {median_asset*1000:,.0f}")
print(f"Top decile asset share: {top_decile_share:.2%}" if pd.notna(top_decile_share) else "Top decile asset share: NA")
print(f"Count ASSET > {threshold*1000:,}: {num_above}")
print(f"Count ASSET < {threshold*1000:,}: {num_below}")

# Table 2

# Summary statistics for 2022Q1 cross-section
# Variables:
# - Depositor sophistication index (z): sophistication_index_z
# - Branch-intensity index (z): branch_density_z
# - HHI exposure (z): hhi_z
# - Metropolitan dummy: metro_dummy
# - Deposit-weighted household income (z): z-score of log_median_hh_income within 2022Q1
var_columns = {
    "zS": "sophistication_index_z",
    "zR": "branch_density_z",
    "zH": "hhi_z",
    "Metropolitan dummy": "metro_dummy",
    "zY": "log_median_hh_income_z",
}

summary_rows = []
row_index = []

# Handle variables that already exist in z/unscaled form
for label, col in var_columns.items():
    if col in df_q1.columns:
        s = pd.to_numeric(df_q1[col], errors="coerce").dropna()
        if len(s) > 0:
            desc = s.describe(percentiles=[0.25, 0.75])
            summary_rows.append([
                desc.get("mean", np.nan),
                desc.get("std", np.nan),
                desc.get("min", np.nan),
                desc.get("25%", np.nan),
                desc.get("75%", np.nan),
                desc.get("max", np.nan),
            ])
            row_index.append(label)

if len(summary_rows) > 0:
    summary_df = pd.DataFrame(
        summary_rows,
        index=row_index,
        columns=["mean", "std", "min", "25%", "75%", "max"],
    ).round(3)

    # Ensure results directory exists and export as a txt table
    os.makedirs("results", exist_ok=True)
    output_path = os.path.join("results", "table_2.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Summary statistics for 2022Q1 cross-section\n\n")
        # Write Markdown header for Quarto compatibility
        f.write("| Variable | mean | std | min | 25% | 75% | max |\n")
        f.write("|---|:---:|:---:|:---:|:---:|:---:|:---:|\n")
        for idx, row in summary_df.iterrows():
            f.write(
                f"| {idx} | {row['mean']:.3f} | {row['std']:.3f} | {row['min']:.3f} | "
                f"{row['25%']:.3f} | {row['75%']:.3f} | {row['max']:.3f} |\n"
            )
    print(f"Exported summary table to {output_path}")


# table 3

# Summary statistics for 2022Q1 cross-section: deposit and loan growth
growth_vars = {
    "All deposits (growth)": "d_average_deposit",
    "Interest-bearing deposits (growth)": "d_average_interest_bearing_deposit",
    "Core deposits (growth)": "d_core_deposit",
    "Total loans (growth)": "d_total_loans",
    "Loans not for sale (growth)": "d_total_loans_not_for_sale",
    "Single-family mortgages (growth)": "d_single_family_loans",
    "C&I loans (growth)": "d_C&I",
}

growth_rows = []
growth_index = []
for label, col in growth_vars.items():
    if col in df_q1.columns:
        s = pd.to_numeric(df_q1[col], errors="coerce").dropna()
        if len(s) > 0:
            desc = s.describe(percentiles=[0.25, 0.75])
            growth_rows.append([
                desc.get("mean", np.nan),
                desc.get("std", np.nan),
                desc.get("min", np.nan),
                desc.get("25%", np.nan),
                desc.get("75%", np.nan),
                desc.get("max", np.nan),
            ])
            growth_index.append(label)

if len(growth_rows) > 0:
    growth_df = pd.DataFrame(
        growth_rows,
        index=growth_index,
        columns=["mean", "std", "min", "25%", "75%", "max"],
    ).round(3)

    # Export as Markdown table for Quarto
    os.makedirs("results", exist_ok=True)
    output_path_growth = os.path.join("results", "table_growth.txt")
    with open(output_path_growth, "w", encoding="utf-8") as f:
        f.write("Summary statistics for 2022Q1 cross-section: deposit and loan growth\n\n")
        # Write Markdown header
        f.write("| Variable | mean | std | min | 25% | 75% | max |\n")
        f.write("|---|:---:|:---:|:---:|:---:|:---:|:---:|\n")
        for idx, row in growth_df.iterrows():
            f.write(
                f"| {idx} | {row['mean']:.3f} | {row['std']:.3f} | {row['min']:.3f} | "
                f"{row['25%']:.3f} | {row['75%']:.3f} | {row['max']:.3f} |\n"
            )
    print(f"Exported growth summary table to {output_path_growth}")