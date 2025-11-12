import pandas as pd
import numpy as np

df = pd.read_csv("data/raw/rcon_full.csv", low_memory=False)

print(df.columns)