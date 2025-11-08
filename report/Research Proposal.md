---
title: "Deposit Funding Shocks and Credit Supply: Bank-Level IV Estimates and Heterogeneous Responses"
format:
  pdf:
    author: Chenning Xu
    documentclass: article
    geometry: margin=1in
    toc: false
    number-sections: false
    pdf-engine: xelatex
---
# 1) Motivation

Since the March 2022 liftoff, U.S. banks have faced higher funding costs as depositors shifted into higher-yield accounts and many institutions turned to more expensive borrowings, developments that pressured net interest margins (FDIC, 2024). A rapidly growing literature explains **cross-sectional variation in deposit rate pass-through** and outflows (e.g., bank size, depositor sophistication, digital intensity, AOCI/HTM mix). Far fewer studies follow the shock through the **deposit channel to credit supply** and its **cross-sectional heterogeneity**.

Classic branch-level designs (policy shocks × county HHI in Drechsler, Savov, & Schnabl, 2017) have been questioned. **Begenau and Stafford (2023)** document **uniform deposit pricing** at large banks, weakening county-level price dispersion and raising **aggregability** concerns. A recent **sophistication-index** paper shows depositor composition strongly predicts pass-through and outflows, shifting attention from local market structure (HHI) to **who the depositors are** (Narayanan & Ratnadiwakara, 2024).

**Central question:** **Does a policy-driven rise in effective deposit funding costs reduce lending for banks whose costs are shifted by our exposure × policy instrument (bank-level LATE)?** Having established that complier-average effect, I will *optionally* assess **size heterogeneity** to test whether small or community banks contract lending more for the same shock.


# 2) Research Questions

**RQ1 (First-stage exposure validity and scope).**  
To what extent do pre-2021 bank exposures that are plausibly predetermined with respect to the 2022–2024 cycle—specifically, **depositor sophistication** and **relationship intensity** (with **footprint HHI** for robustness)—predict the **policy-induced** change in a bank’s **effective deposit rate** when interacted with high-frequency monetary policy variation $\Delta \mathrm{FFR}_t$? This is a relevance question for the instrument set $Z_{it}=\mathrm{Exposure}_i \times \Delta \mathrm{FFR}_t$, estimated with bank fixed effects and **deposit-weighted region×quarter fixed effects** that purge common and local demand shocks (Begenau & Stafford, 2023).

**RQ2 (Average lending response to a funding-cost shock).**  
What is the **local average treatment effect (LATE)** of a 100 bp **instrumented** increase in the **effective deposit rate** on bank-level lending growth $\Delta \ln L^k_{i,t+h}$ over horizons $h\in\{0,1,2\}$ for major portfolios (Total, C&I, CRE, 1–4 family)? The identifying variation is **policy-driven funding-cost movement** among **complier banks** whose deposit rates load on the instrument; deposit-weighted region×quarter fixed effects absorb regional demand. A negative coefficient on the instrumented funding-cost change is evidence that the **deposit channel reduces lending** on average.

**RQ3 (Extension: size-heterogeneous lending response).**  
Conditional on RQ2, does the LATE differ by bank size? Test whether the elasticity varies across pre-set size bins (<$10B, $10–50B, >$50B) or via an interaction between the instrumented funding-cost change and a small-bank indicator. This answers whether the **same funding-cost shock** produces a **disproportionate lending contraction** among small/community banks, without changing the interpretation of RQ2.

> *Notes:* RQ1 is an instrument-relevance problem; RQ2 identifies a bank-level **credit-supply** effect under a standard exclusion restriction; RQ3 is heterogeneity conditional on RQ2.

# 3) Positioning

Many recent papers explain **who** has higher deposit betas; **few** establish the **second stage**: whether a **funding-cost shock** reduces **lending** and how that effect **varies across banks**. The design here is **bank-level** (not branch-level price dispersion), uses **pre-2021 exposures × policy shocks** to instrument **effective deposit-cost changes**, and includes **deposit-weighted region×quarter fixed effects** to purge local demand—directly responding to the uniform-pricing and aggregability concerns in **Begenau and Stafford (2023)** and incorporating the depositor-mix critique of **Drechsler et al. (2017)** via **Narayanan and Ratnadiwakara (2024)**.

# 4) Data & Key Variables

- **Call Reports (FFIEC 031/041/051)**, 2019Q1–2024Q4; domestically chartered banks.  
- **FDIC Summary of Deposits (SOD)**; snapshot **2021-06-30** to build time-invariant bank footprints and deposit weights by region/county.  
- **Optional exposures:** county ACS/HMDA features (income, %BA+, age 65+, refi intensity) aggregated to bank footprints using SOD-2021 deposit weights.

**Constructs**  
- **Effective deposit rate:**  
  $$
  r^d_{it}=\frac{\mathrm{Deposit\ interest\ expense}_{it}}{\tfrac12\big(\mathrm{IB\ deposits}_{it}+\mathrm{IB\ deposits}_{i,t-1}\big)},
  \qquad \Delta r^d_{it}=r^d_{it}-r^d_{i,t-1}.
  $$
- **Loan growth:** $\Delta \ln L^{k}_{i,t+h}$ for $k\in\{\mathrm{Total},\mathrm{C\&I},\mathrm{CRE},\mathrm{1\!-\!4}\}$ and $h\in\{0,1,2\}$. Include **Small-business loans** (RC-C Part II, June-to-June long difference) as a complementary outcome.  
- **Pre-hike exposures (fixed at 2021):** depositor sophistication $S_i$, relationship intensity $R_i$, footprint HHI $HHI_i$ (robustness).  
- **Policy shocks:** $\Delta \mathrm{FFR}_t$ baseline; robustness: cumulative FFR or a Post-2022 indicator.

# 5) Identification & Methodology (Bank-Level 2SLS)

**First stage (2022Q1–2023Q4):** Bartik-style instruments $Z_{it}=\mathrm{Exposure}_i \times \Delta \mathrm{FFR}_t$ isolate the policy-driven component of $\Delta r^d_{it}$:
$$
\Delta r^d_{it}
= \alpha_i + \tau_t
+ \pi_S \big(S_i\,\Delta \mathrm{FFR}_t\big)
+ \pi_R \big(R_i\,\Delta \mathrm{FFR}_t\big)
+ \pi_H \big((-HHI_i)\,\Delta \mathrm{FFR}_t\big)
+ X'_{i,t-1}\beta
+ \sum_r \delta_{rt}\, w_{ir}
+ \varepsilon_{it}.
$$
Expect $\pi_S>0$ and $\pi_R<0$. Report Kleibergen–Paap F and partial $R^2$ overall and by size.

**Second stage (credit-supply LATE):**
$$
\Delta \ln L^k_{i,t+h}
= \alpha_i + \tau_{t+h}
+ \lambda\, \widehat{\Delta r^d_{it}}
+ X'_{i,t-1}\gamma
+ \sum_r \phi_{r,t+h}\, w_{ir}
+ u_{i,t+h}.
$$
Optionally add a size interaction $\widehat{\Delta r^d_{it}}\times \mathrm{Small}_i$ or re-estimate by size bins (<$10B, $10–50B, >$50B).

# 6) Validity & Diagnostics (brief)

- **Local demand purge:** deposit-weighted **region×quarter fixed effects** in both stages.  
- **Placebos:** 2019–2021 pre-period (near-zero shocks).  
- **IV strength & over-ID:** KP-F, partial $R^2$; Hansen J when over-identified.  
- **Robustness:** deposit-weighted vs unweighted; exclude Top-25/Top-50 banks; winsorize tails and drop merger quarters.

# 7) Scope, Limits, and Policy Relevance

- **Scope:** Bank-level quantities (with RC-C Part II for small-business loans).  
- **Limits:** Instrument relevance may weaken for mega-banks; addressed via size splits. Exclusion rests on exposures affecting lending **only via funding costs** during hikes; supported by fixed effects, placebos, and standard IV diagnostics.  
- **Policy:** Identifies bank profiles that **amplify monetary transmission** to SME-relevant credit and clarifies when **liquidity backstops** temper the lending impact of rate hikes.

# 8) Expected Contribution to the Literature

- **Second-stage causal evidence.** Provides bank-level LATE estimates for the effect of a **policy-induced funding-cost shock** on lending, moving beyond pass-through/outflow determinants to the **credit-supply consequence** (cf. Drechsler et al., 2017; Narayanan & Ratnadiwakara, 2024; Reghezza et al., 2024).  
- **Design aligned with critiques.** Offers an identification strategy that is robust to **uniform pricing** and **aggregability** critiques (Begenau & Stafford, 2023) by (i) working at the **bank level**, (ii) using **exposure×policy** instruments, and (iii) employing **footprint-weighted region×time** controls.  
- **Heterogeneity as an extension.** Documents whether **small/community banks** exhibit **larger** lending elasticities to the same shock, informing distributional assessments of monetary transmission.  
- **Portable template.** The framework generalizes to other funding channels and jurisdictions, complementing bank–firm matched approaches (e.g., Reghezza et al., 2024).

---

### Selected references (core deposit-channel papers)

- Begenau, J., & Stafford, E. (2023). *Uniform pricing of U.S. bank deposits* (Working paper).  
- Drechsler, I., Savov, A., & Schnabl, P. (2017). The deposits channel of monetary policy. *Quarterly Journal of Economics, 132*(4), 1819–1876.  
- Narayanan, A., & Ratnadiwakara, D. (2024). *Depositor sophistication and bank funding in the 2022–23 hiking cycle* (Working paper).  
- d’Avernas, A., Eisfeldt, A. L., & Weill, P.-O. (2025). *Large vs. small banks: Deposit rate elasticities, uniform pricing, and location* (Working paper).  
- Egan, M., Hortaçsu, A., & Matvos, G. (2017). Deposit competition and financial fragility: Evidence from the U.S. banking sector. *Journal of Finance, 72*(6), 2511–2567.  
- Egan, M., Lewellen, S., & Sunderam, A. (2021). The deposit franchise of banks. *Quarterly Journal of Economics, 136*(1), 1–46.  
- Reghezza, C., et al. (2024). *As interest rates surge: Flighty deposits and lending* (ECB Working Paper No. 2923).
