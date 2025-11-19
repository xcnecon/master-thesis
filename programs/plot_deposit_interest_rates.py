import pandas as pd
import matplotlib.pyplot as plt


def main() -> None:
    df = pd.read_csv("data/processed/deposit_interest_rate.csv")

    # Ensure time axis parses as datetime for correct ordering
    df['rssd9999'] = pd.to_datetime(df['rssd9999'], errors='coerce')

    # Aggregate (sum interest / sum deposits) to reduce outliers
    # Reconstruct total interest from rates and averages to avoid carrying raw interest column
    df['_implied_interest'] = (df['interest_rate_on_deposit'] * df['average_deposit']) / 4
    ts_weighted = df.groupby('rssd9999', as_index=False).agg(
        total_interest=('_implied_interest', 'sum'),
        total_avg_deposit=('average_deposit', 'sum'),
        total_avg_interest_bearing=('average_interest_bearing_deposit', 'sum'),
    )
    ts_weighted['weighted_interest_rate_on_deposit'] = (
        ts_weighted['total_interest'] / ts_weighted['total_avg_deposit']
    ) * 4
    ts_weighted['weighted_interest_rate_on_interest_bearing_deposit'] = (
        ts_weighted['total_interest'] / ts_weighted['total_avg_interest_bearing']
    ) * 4
    ts_weighted.sort_values('rssd9999', inplace=True)

    # Simple average across banks per date (winsorized)
    ts_rates_input = df[['rssd9001', 'rssd9999', 'interest_rate_on_deposit', 'interest_rate_on_interest_bearing_deposit']].copy()
    per_bank_rates = ts_rates_input.groupby(['rssd9001', 'rssd9999'], as_index=False).mean(numeric_only=True)

    # Winsorize per-date simple averages (0.5% / 99.5%) before plotting
    winsor_cols = ['interest_rate_on_deposit', 'interest_rate_on_interest_bearing_deposit']
    per_bank_w = per_bank_rates.copy()
    for col in winsor_cols:
        lower = per_bank_w.groupby('rssd9999')[col].transform(lambda s: s.quantile(0.005))
        upper = per_bank_w.groupby('rssd9999')[col].transform(lambda s: s.quantile(0.995))
        per_bank_w[col] = per_bank_w[col].clip(lower=lower, upper=upper)
    ts_simple_w = per_bank_w.groupby('rssd9999', as_index=False).mean(numeric_only=True)
    ts_simple_w.sort_values('rssd9999', inplace=True)

    # Plot
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


if __name__ == "__main__":
    main()

