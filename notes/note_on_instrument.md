# Note on Construction of Sophistication Index, HHI, and Branch Density (2021 baseline)

## Data and timing

* **Reference year:** 2021 for all cross-sectional exposures to keep them predetermined for rate-hike episodes.
* **Sources:** ACS (county demographics), IRS SOI (tax composition), HMDA 2020–2021 (mortgage/refi activity), FDIC SOD 2021 (branch-level deposits and locations).
* **Geography:** county (FIPS); Puerto Rico excluded. HMDA counties with very thin volume are median-imputed for refi share (see below).

---

## County Sophistication Index → Bank Exposure

### Variables (county)

* `median_hh_income` (logged), `share_ba_plus`, `share_age_65plus`, `share_internet_sub`, `share_dividend`, `share_interest`, `refi_share`.

**Pre-processing**

* **HMDA refi share:** set to missing when `orig_total ≤ 20` to avoid small-n noise; then impute with the cross-county median.
* **Transform:** `median_hh_income` → `log(median_hh_income)`. Others in proportional form kept as levels.
* **Standardize:** z-score each feature across counties in 2021.

**PCA (county level)**

* Run PCA on the standardized county features (SVD on the mean-centered Z matrix).
* Keep **PC1** as the sophistication construct. Orient the sign so higher = more educated, richer, more connected, more asset-income, more refi activity. Implementation detail: define `sophistication_index = −PC1` to lock a positive interpretation. Outputs include score, loadings, and explained variance. 

**Aggregation to banks (exposure)**

* Compute each bank’s deposit-share weights across counties using SOD-2021:
  [
  w_{bc}=\frac{\text{deposits of bank }b\text{ in county }c}{\sum_{c'} \text{deposits of bank }b\text{ in }c'},,\quad \sum_c w_{bc}=1.
  ]
* Bank exposure is the deposit-weighted average of county sophistication:
  [
  S_b=\sum_c w_{bc},\text{SophIndex}_c.
  ]
* **Bank-level scaling:** z-score (S_b) across banks in the estimation sample for unit comparability. Freeze the mean and sd for any out-of-sample use.

**Why county-first, then bank weighting**

* The latent trait lives where depositors reside; county PCA uses the largest cross-section and yields stable, interpretable loadings.
* PCA does not commute with aggregation. Weighting county scores into banks preserves one common measurement system; bank-first PCA would let sample composition change the factor.

---

## HHI (two complementary measures)

### 1) Market concentration where the bank operates (exogenous environment)

* **County market HHI (2021):**
  [
  \text{HHI}*c=\sum*{b}\left(100,\frac{\text{dep}*{bc}}{\sum*{b'}\text{dep}_{b'c}}\right)^{2}\in[0,10000].
  ]
  This is the standard DOJ/FRB definition using deposit shares by county.
* **Bank exposure to market concentration:**
  [
  \text{MarketHHI}*b=\sum_c w*{bc},\text{HHI}_c.
  ]
  Interpretation: the average competitive intensity of the deposit markets a bank faces.

### 2) Geographic concentration of the bank’s own footprint (endogenous concentration)

* **Footprint HHI (bank-level):**
  [
  \text{FootprintHHI}*b=\sum_c w*{bc}^{2}\in[0,1].
  ]
  Interpretation: how concentrated a bank’s deposits are in a few counties (higher = more concentrated).

**Usage notes**

* Report both where relevant: the first is a **market-structure control**, the second a **bank geography control**. They answer different questions and are not substitutes.

---

## Branch Density (relationship/localness proxy)

**Definition**

* **Raw intensity:**
  [
  \text{branch_density}_b=\frac{\text{number of branches}_b}{\text{total deposits}_b/10^9}\quad\text{(branches per $1B deposits)}.
  ]

**Transformation and scaling**

1. Winsorize lightly (e.g., 0.5% tails) to cap outliers.
2. Apply **log1p** to encode diminishing returns and tame the right tail:
   [
   x_b=\log\bigl(1+\text{branch_density}_b\bigr).
   ]
3. z-score (x_b) across banks for use in composites or regressions.

**Optional, cleaner “size-free” version**

* Residualize physical branching from size and state mix:
  [
  \log(\text{branches}_b)=\alpha+\beta,\log(\text{deposits}*b)+\gamma*{\text{state}}+\varepsilon_b,
  ]
  and use the standardized residual (\hat\varepsilon_b) as “excess branching.” This removes the mechanical correlation with size and local market structure.

**Justification**

* Branch presence is a widely used proxy for soft-information, proximity, and relationship intensity. Normalizing by deposits makes a bank with the same size but more local points of contact score higher. The **log** transform preserves rank while preventing a handful of extreme branchers from dominating.

---

## Practical choices and diagnostics

* **Freeze year:** all weights and features are from **2021** to ensure predetermined exposures.
* **Sign discipline:** once PC1 is oriented so higher = more sophisticated, keep that convention throughout.
* **Missingness:** for HMDA thin cells, the median imputation avoids spurious extremes without shifting the cross-section materially.
* **Sensitivity checks:**

  * Re-run the county PCA dropping `share_age_65plus` and, separately, dropping `median_hh_income`; county PC1 scores should be highly rank-correlated with the baseline.
  * Deposit-weighted PCA at the county level (using county deposits as weights) should not materially change PC1 loadings.
  * For HHI, replicate with MSA or commuting-zone markets as a robustness to county borders.

**Deliverables**

* County-level PCA scores, loadings, explained variance, plus county sophistication index.
* Bank-level sophistication exposure (S_b) (z-scored), MarketHHI and FootprintHHI, and transformed branch density (and optional residualized variant).

Implementation details of the PCA step, the z-scaling, and the sign orientation of PC1 are encoded in the processing script that merges ACS/IRS/HMDA to counties and writes out scores and loadings. 
