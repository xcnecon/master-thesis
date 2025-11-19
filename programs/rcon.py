import pandas as pd
import numpy as np

rcon1 = pd.read_csv("data/raw/rcon1.csv", parse_dates=["rssd9999"]).drop_duplicates()
rcon2 = pd.read_csv("data/raw/rcon2.csv", parse_dates=["rssd9999"]).drop_duplicates()

# Merge on rssd9001 and rssd9999 after de-duplication (column exists in both)
df = rcon1.merge(rcon2, on=["rssd9001", "rssd9050", "rssd9999"], how="left")

df['small_biz_loan'] = df['rcon5584'] + df['rcon5578'] + df['rcon5570'] + df['rcon5564'] + df['rcon5585'] + df['rcon5579'] + df['rcon5569'] + df['rcon5587'] + df['rcon5581'] + df['rcon5573'] + df['rcon5567'] + df['rcon5589'] + df['rcon5573'] + df['rcon5583'] + df['rcon5575'] + df['rcon5571'] + df['rcon5565']
df.drop(columns=['rcon5584', 'rcon5578', 'rcon5570', 'rcon5564', 'rcon5585', 'rcon5579', 'rcon5569', 'rcon5587', 'rcon5581', 'rcon5573', 'rcon5567', 'rcon5589', 'rcon5573', 'rcon5583', 'rcon5575', 'rcon5571', 'rcon5565'], inplace=True)

df['average_net_fed_funds_bought'] = df['rcon3353'] - df['rcon3365']
df.drop(columns=['rcon3353', 'rcon3365'], inplace=True)



df.to_csv("data/processed/rcon.csv", index=False)