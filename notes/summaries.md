
{
  "citekey": "DrechslerSavovSchnabl2016",
  "full_citation": "Drechsler, I., Savov, A., & Schnabl, P. (2016). The deposits channel of monetary policy (NBER Working Paper No. 22152). National Bureau of Economic Research.",
  "research_question": "Does a higher federal funds rate widen bank deposit spreads and shrink deposit supply—especially where local deposit-market competition is low—creating a deposits channel of monetary policy?",
  "setting/data": "United States; 1994–2008 (branch deposits), 1997–2008 (branch rates); FDIC branch-level deposits (906,125 branch–year obs.), RateWatch branch-level deposit rates (287,928 branch–quarter obs.), 3,104 counties, bank call reports (424,606 bank–quarter obs.). Table 1 reports sample sizes. (pp. 54–55, 56–57) ",
  "method": "Monopolistic-competition model linking the fed funds rate to banks’ effective market power over liquidity; empirical tests using branch-level OLS with bank×time and other fixed effects; county Herfindahl as competition proxy; weekly event studies around FOMC dates; decomposition of expected vs unexpected rate changes using fed funds futures. (pp. 10–16, 21–26, 28–30, 51–52) ",
  "key_mechanisms": [
    "Higher fed funds rate raises the opportunity cost of cash, increasing banks’ effective market power and deposit spreads. (pp. 12–16) ",
    "Households substitute away from liquid deposits into less liquid deposits/bonds when spreads rise. (pp. 4–6, 12–16) ",
    "Effects are stronger where deposit-market competition is low. (pp. 15–16, 24–26) ",
    "Banks partly replace lost core deposits with wholesale funding, but total assets and lending still fall. (pp. 66–67) "
  ],
  "main_findings": [
    "A 100 bp increase in the fed funds rate raises savings (MMA) deposit spreads by ~15 bps more in low-competition counties than in high-competition counties, with bank×time FE. (Table 2 Panel A Col.1, p. 56) ",
    "For 12-month CDs, a 100 bp T-bill increase raises spreads by ~8 bps more in low-competition counties. (Table 2 Panel B Col.1, p. 56) ",
    "Deposit growth falls by ~0.86% more in low- vs high-competition counties per +100 bp fed funds move. (Table 3 Col.1, p. 57) ",
    "Event study: the spread gap between low- and high-competition counties appears within a week of an FOMC change (~7–11 bps cumulated in 1–2 weeks). (Fig. 5 Panels A–C, pp. 51–52) ",
    "At banks in less competitive markets, +100 bp fed funds is associated with higher wholesale funding (+3.466%), lower total liabilities offset incomplete, and lower assets and loans (assets −0.979%, RE loans −0.528%, C&I −0.656%). (Tables 12–13, pp. 66–67) "
  ],
  "limits/caveats": [
    "Sample excludes the ZLB era and drops 2H 2008; findings pertain to 1994–2008/1997–2008. (p. 17) ",
    "Competition proxied by county Herfindahl; unobserved demand factors could vary locally. (pp. 18–21) ",
    "Identification assumes branches within a bank share internal funding (bank-time FE decouple lending and deposit-taking locally). (pp. 21–24) ",
    "Advertised new-account rates may differ from average paid rates. (pp. 17–18, 24) "
  ],
  "how_it_relates_to_my_project": [
    "Foundational evidence for a deposits channel and a competition interaction you can leverage when modeling deposit betas and credit supply responses.",
    "Their bank×time FE and event-study designs are ready-made templates for your deposit-channel specifications.",
    "Quantifies wholesale-funding substitution and lending effects you want to separate from pure pricing effects.",
    "Suggests measuring heterogeneity by local HHI and product type (demandable vs time deposits)."
  ],
  "notable_quotes": [
    {"page": 3, "quote": "We propose and test a new channel for the transmission of monetary policy, the deposits channel."},
    {"page": 25, "quote": "A 100 basis point increase in the Fed funds rate leads to 0.86% lower deposit growth in low-competition counties relative to high-competition counties."}
  ]
}

{
  "citekey": "NarayananRatnadiwakara2024",
  "full_citation": "Narayanan, R. P., & Ratnadiwakara, D. (2024). Depositor characteristics and deposit stability. Working paper.",
  "research_question": "How do depositor demographics and financial sophistication shape banks’ rate pass-through (deposit betas) and deposit stability in the 2022–2023 hiking cycle?",
  "setting/data": "United States; depositor profiles mapped from 2019 Advan geolocation to census tracts; outcomes over 2022–2023 (0% → 5.25% fed funds). Sources: Advan Monthly Patterns, FDIC SOD, bank Call Reports, RateWatch, ACS, HMDA, IRS. (pp. 2–3, 7–12) ",
  "method": "Construct bank-level depositor profiles (income, education, age, dividend income, refinance rate) via geolocation; define a ‘Sophisticated’ indicator; regress cumulative change in interest expense and deposit flows on sophistication/deciles with size, HHI, FE; dynamic DiD over quarters; product-level RateWatch checks; compute deposit-franchise factors DF(r′)=D(1−w)(1−β−c/r′). (pp. 7–9, 18–26, 37–42) ",
  "key_mechanisms": [
    "Banks with financially sophisticated depositor bases raise offered rates faster and by more (higher betas). (pp. 18–23) ",
    "Despite higher rates, these banks suffer larger deposit outflows, concentrated in core and uninsured deposits. (pp. 26–31) ",
    "Net effect reduces the economic value generated per dollar of deposits (deposit franchise). (pp. 39–42) ",
    "Responses start before SVB’s failure, indicating sensitivity to expected policy paths and low switching frictions. (pp. 24–26, 38) "
  ],
  "main_findings": [
    "Systemwide, a 5.25 pp rate increase raised interest expense by ~1.43% on average (β≈0.27); β rises with bank size (~0.25 small → ~0.44 large). (pp. 2–3) ",
    "Banks serving top-income or top-education depositors increased rates more; for large banks the top-quartile effect was ~0.79–0.80 pp higher interest expense than bottom-quartile. (Table 3 Panel B Cols.2–3, p. 22) ",
    "Branches with sophisticated depositors lost about 2% more deposits within the same bank (within-bank, county FE). (Table 6 Panel A Cols.1–4, p. 36) ",
    "Core deposits dropped on average −1.16% (small banks) and −6.04% (large banks) from Dec 2021 to Dec 2023. (Table 4 Panel A, p. 28) ",
    "Deposit-franchise factor: small banks 0.18 (sophisticated) vs 0.25 (non-sophisticated), large 0.14 vs 0.18, implying roughly 29–38% higher value per $1 for non-sophisticated depositor bases. (Table 8 Row 7, p. 42)"
  ],
  "limits/caveats": [
    "Depositor profiles use physical branch visits; online banking intensity can attenuate estimates, though tests suggest lower bounds. (pp. 44–48)",
    "2015–2019 comparison uses later-measured characteristics, assuming persistence. (pp. 41–45)",
    "Branch matching to POI data is incomplete for the smallest banks; addresses standardized to improve coverage. (pp. 9–12)"
  ],
  "how_it_relates_to_my_project": [
    "Offers a tractable way to measure depositor sophistication you can merge to banks/branches; use this as a control or treatment heterogeneity in your deposit-channel tests.",
    "Quantifies deposit betas and outflows during 2022–2023, informing identification of funding-cost shocks vs quantity shocks in your credit-supply equations.",
    "Provides a formulaic DF decomposition (β, w, c) you can port to your contribution section to show welfare/valuation implications of the deposit channel.",
    "Event-timing results support modeling immediate pass-through and withdrawals rather than slow adjustment."
  ],
  "notable_quotes": [
    {"page": 1, "quote": "We document considerable heterogeneity in terms of the age, income, education, and financial sophistication of depositors across banks and branches."},
    {"page": 1, "quote": "Banks with financially sophisticated depositors suffered greater deposit runoffs when market interest rates increased during 2022–2023."}
  ]
}

{
  "citekey": "BegenauStafford2023",
  "full_citation": "Begenau, J., & Stafford, E. (2023). Uniform rate setting and the deposit channel. Working paper.",
  "research_question": "Do banks set deposit rates uniformly across markets, and if so, does this undermine identification and aggregation of the deposits channel based on local market concentration?",
  "setting/data": "United States; 2001–2019 RateWatch branch offer rates linked to FDIC SOD branches; bank and BHC call reports; CRSP for market valuations; bank/county macro controls. (pp. 6–13, 24–27) :contentReference[oaicite:31]{index=31}",
  "method": "Document uniform rate-setting prevalence; replicate DSS branch-level spread regressions but include follower branches; re-estimate deposit flows with placebos; analyze big banks (≈90% of assets) separately; test alternative market-power proxies; decompose aggregate deposit flows into DC vs non-DC and debt substitution. (pp. 3–7, 16–24, 27–35, 52–54) :contentReference[oaicite:32]{index=32}",
  "key_mechanisms": [
    "Uniform rate setting (few unique rates per bank) implies little within-bank cross-market price variation for HHI to act upon. (pp. 11–15, 40–41) :contentReference[oaicite:33]{index=33}",
    "Observed branch deposit-growth sensitivities may reflect regional demand, not bank pricing power. (pp. 22–24, 31–35) :contentReference[oaicite:34]{index=34}",
    "At the aggregate, funding substitution (non-DC deposits, debt) offsets DC deposit outflows. (Table 11, pp. 53–54) :contentReference[oaicite:35]{index=35}"
  ],
  "main_findings": [
    "Including follower branches (≈90% of branch observations) drives the HHI×ΔFFR coefficient on spread passthrough to ~0; the within-bank first-stage vanishes. (Table 6 Cols.1–2, p. 48) :contentReference[oaicite:36]{index=36}",
    "Yet follower branches still show deposit-flow ‘sensitivities,’ indicating non-pricing drivers; pre-crisis negative, post-crisis positive. (Table 7 Panel B, p. 49) :contentReference[oaicite:37]{index=37}",
    "Among the banks holding ~90% of assets, spread and loan sensitivities are ~zero and deposit sensitivities have the opposite sign to the deposit-channel prediction. (Table 10 Panel B, p. 52) :contentReference[oaicite:38]{index=38}",
    "Aggregate: DC deposits fall with ΔFFR (e.g., −2.298 with no lags), while non-DC deposits and bank debt rise, implying strong substitution. (Table 11, pp. 53–54) :contentReference[oaicite:39]{index=39}",
    "Large banks set very few unique rates: e.g., Bank of America operated 5,728 branches across 694 counties in 2007 yet used only two MM rates, and since 2016 typically one unique rate. (pp. 3–5, 13–14, 41) :contentReference[oaicite:40]{index=40}"
  ],
  "limits/caveats": [
    "RateWatch lacks 1997–2000; branch-owner history linking is non-trivial. (pp. 7–9, 18) :contentReference[oaicite:41]{index=41}",
    "‘Rate-setter’ classification is vendor-defined; some networks share identical rates. (pp. 11–13) :contentReference[oaicite:42]{index=42}",
    "County HHI may be a poor proxy for market power; authors propose alternatives. (pp. 24–27) :contentReference[oaicite:43]{index=43}"
  ],
  "how_it_relates_to_my_project": [
    "Warns that DSS-style HHI×ΔFFR first-stage can fail once uniform pricing is acknowledged; motivates robustness checks using follower branches and big-bank subsamples.",
    "Encourages separating DC vs non-DC deposits and testing funding substitution when mapping deposit shocks into credit supply.",
    "Suggests exploring alternative market-power proxies (e.g., deposit productivity, rate-gap/flow indices) rather than county HHI alone.",
    "Supports adding regional-demand controls when estimating deposit-channel effects on lending."
  ],
  "notable_quotes": [
    {"page": 1, "quote": "US banks predominately use uniform deposit rate setting policies, particularly the largest banks."},
    {"page": 3, "quote": "When follower branches are included… there is no reliable relation between deposit rate pass-through and market concentration."}
  ]
}

{
  "citekey": "GreenwaldSchulhoferWohlYounger2023",
  "full_citation": "Greenwald, E., Schulhofer-Wohl, S., & Younger, J. (2023). Deposit convexity, monetary policy, and financial stability (FRB Dallas Working Paper No. 2315). https://doi.org/10.24149/wp2315",
  "research_question": "Do deposit betas rise with market rates, shortening deposit duration and amplifying monetary-policy transmission and fragility?",
  "setting/data": "United States; evidence spans prior hiking cycles and 2022–2023; sources: Senior Financial Officer Survey (~80 banks; Nov 2022 & May 2023), Call Reports, H.8, OCC survey stats. (pp. 6–8) ",
  "method": "Analytical model of dynamic (rate-level-dependent) deposit betas and duration; empirical calibration using SFOS betas, Call Reports, and 5-year yields to quantify ‘duration delivery’ to bank balance sheets and implications for lending and runs. (pp. 2–5, 10–14) ",
  "key_mechanisms": [
    "Deposit beta increases with the level of market rates, so effective deposit duration falls as rates rise. (pp. 2–4)",
    "Rate hikes shift the deposit mix toward time deposits, further raising betas and funding costs. (p. 8)",
    "Rising betas deliver large, time-varying duration risk to bank balance sheets, tightening lending capacity. (pp. 4, 12–14)",
    "Dynamic betas increase fragility in transitions away from the ELB by weakening the hedge from deposit franchises. (pp. 15–18)"
  ],
  "main_findings": [
    "From Dec 2021 to Jul 2023, banks absorbed duration equivalent to ~$4.5 trillion in 10-year Treasuries; ~40% (~$1.8T) due to dynamic betas. (p. 13)",
    "SFOS averages for Mar 2022–Apr 2023: retail/operational/non-operational betas 24%, 41%, and 50%; implied aggregate betas ~33% (to Apr 2023) and ~44% (to Nov 2023); for May–Nov 2023, ~60%. (pp. 12–13)",
    "Deposit mix change Mar 2022–Sep 2023: time deposits +~$700B while other deposits −~$1.7T. (p. 8)",
    "A one-year reduction in assumed deposit half-life adds ~+$600B 10-year equivalents of duration delivery. (p. 14)"
  ],
  "limits/caveats": [
    "Model relies on calibrated half-life (e.g., 5 years) and uses 5-year yields as the policy-relevant rate; actual bank practices vary. (pp. 13–14)",
    "SFOS reflects self-reported betas; realized pass-through can differ by product and bank. (pp. 6–8)"
  ],
  "how_it_relates_to_my_project": [
    "Quantifies dynamic betas you can map into your funding-cost shock to lending regressions during 2022–2023.",
    "Motivates modeling beta as rate-level-dependent (not constant) in your deposit-channel identification.",
    "Supplies magnitudes for duration-risk transmission to validate mechanisms behind credit-supply reductions."
  ],
  "notable_quotes": [
    {"page": 2, "quote": "We show empirically that the “beta” of deposit rates to market rates increases as market rates rise."},
    {"page": 2, "quote": "Deposit convexity amplifies monetary policy transmission and increases financial fragility."}
  ]
}

{
  "citekey": "KunduParkVats2023",
  "full_citation": "Kundu, S., Park, S., & Vats, N. (2023). The Geography of Bank Deposits and the Origins of Aggregate Fluctuations. Working paper.",
  "research_question": "How do geographically concentrated bank deposits transmit local shocks into aggregate fluctuations via banks’ internal capital markets?",
  "setting/data": "United States; 1994–2018; FDIC Summary of Deposits (branches), SHELDUS disasters, Call Reports, CRA small-business loans, HMDA mortgages, SNL; macro controls. (pp. 10–13)",
  "method": "Granular instrumental variables: bank-level deposit shocks built from within-bank deposit concentration interacted with county disaster damages; aggregate ‘granular’ shocks exclude common components; Jordà projections; 2SLS for elasticities and money multiplier. (pp. 18–22, 55–57)",
  "key_mechanisms": [
    "Within-bank deposit concentration (≈30% in one county) creates granular exposure; shocks propagate through internal capital markets. (pp. 12–13)",
    "Granular deposit shocks are orthogonal to aggregate factors yet explain part of GDP growth variation. (pp. 21–22, 55–56)",
    "Funding shocks reduce lending (small-business and jumbo mortgages), especially at large banks and where information frictions are larger. (pp. 28–36)"
  ],
  "main_findings": [
    "New fact: about 30% of a bank’s deposits are concentrated in a single county. (p. 12)",
    "A 1-SD granular deposit shock reduces GDP growth by ~0.05–0.07 pp; granular shocks explain ~3.30% of GDP growth variance. (Tables 2–3, pp. 55–56)",
    "Deposit elasticity of GDP ≈ 0.87; a 1 pp fall in deposit growth associates with ~0.87 pp lower GDP growth. (Table 5, p. 57)",
    "Money multiplier: a $1 fall in deposits is associated with ~$1.18 reduction in lending. (Table 5, p. 57)",
    "1-SD bank-deposit shock lowers bank deposit growth by ~0.98 pp and liquidity creation growth by ~0.19 pp, persistently for years. (Fig. 6, p. 49)"
  ],
  "limits/caveats": [
    "Identification hinges on disasters as exogenous local shocks; general equilibrium spillovers may attenuate or amplify results. (pp. 17–21)",
    "Granular shock explains a modest but non-trivial share of GDP variation; complements, not replaces, standard macro shocks. (pp. 55–56)"
  ],
  "how_it_relates_to_my_project": [
    "Establishes macro relevance for deposit shocks you study at the bank level.",
    "Offers an external instrument template (deposit concentration × disasters) to validate your funding-shock design.",
    "Provides benchmark elasticities (GDP–deposits, lending–deposits) for your contribution section."
  ],
  "notable_quotes": [
    {"page": 1, "quote": "30% of deposits are concentrated in a single county."},
    {"page": 1, "quote": "We identify the deposit elasticity of economic growth as 0.87 and the money multiplier as 1.18."}
  ]
}

{
  "citekey": "ErelLiebersohnYannelisEarnest2023",
  "full_citation": "Erel, I., Liebersohn, J., Yannelis, C., & Earnest, S. (2023, rev. 2025). Monetary policy transmission through online banks (NBER Working Paper No. 31380).",
  "research_question": "Do online banks pass through policy-rate hikes to deposit and loan rates more than traditional banks, and how do deposits and lending respond?",
  "setting/data": "United States; 2021–2023 (focus on Mar 2022–Apr 2023 hikes); RateWatch branch rates (~3,916 traditional & 30 online banks), FFIEC Call Reports, FDIC SOD, Nielsen ads, ACS demographics. (pp. 39–41)",
  "method": "Difference-in-differences and dynamic DiD: Online×Post(Mar 2022) and Online×FFR comparing online vs brick-and-mortar banks; deposit/lending quantities from Call Reports; robustness via matching and subsamples. (pp. 39–43, 45–48)",
  "key_mechanisms": [
    "Lower search frictions and national competition make online depositors less sticky, yielding higher deposit-rate passthrough. (pp. 3–6, 10–13)",
    "Online banks’ deposits grow (and lending rises) during hikes as they raise rates more, attracting inflows. (pp. 20–22, 28–30, 41–43)"
  ],
  "main_findings": [
    "100 bp FFR increase yields ~17–36 bp larger deposit-rate pass-through at online banks (e.g., +0.357 pp for savings, +0.174 pp money market, +0.245 pp 6-mo CD, +0.358 pp 24-mo CD). (Table 3, pp. 41–42)",
    "Online banks’ total deposits increased relative to traditional by about $5.8–$6.0B, concentrated in interest-bearing deposits. (Table 4, p. 42)",
    "Total lending at online banks rose by about $6.6B (personal loans +$4.6B) relative to traditional banks. (Table 10, p. 47)",
    "Loan-rate passthrough higher at online banks: +0.171–0.316 pp for auto loans and +0.368–0.407 pp for 15y/30y mortgages per 100 bp FFR. (Table 10, p. 47)"
  ],
  "limits/caveats": [
    "Online banks are fewer but large; results focus on short window with steep hikes; generalization to other regimes may differ. (pp. 39–41, 48)",
    "Ratewatch coverage and branch assignment may miss some smaller institutions’ online activity. (p. 15)"
  ],
  "how_it_relates_to_my_project": [
    "Provides U.S. quasi-experimental magnitudes for deposit-rate and quantity adjustment to benchmark your deposit-channel effects.",
    "Supports modeling depositor sophistication/search as a key heterogeneity dimension (online vs local friction).",
    "Links funding inflows to lending increases, useful for your credit-supply transmission step."
  ],
  "notable_quotes": [
    {"page": 3, "quote": "A 100 basis point increase in the federal funds rate leads to a 30 basis points larger increase in the deposit rates of online banks relative to traditional banks."},
    {"page": 20, "quote": "Online bank deposits have been growing at a much faster rate… with total deposits reaching about 13% of system deposits."}
  ]
}

{
  "citekey": "dAvernasEisfeldtHuangStantonWallace2023",
  "full_citation": "d’Avernas, A., Eisfeldt, A. L., Huang, C., Stanton, R., & Wallace, N. (2023). The deposit business at large vs. small banks (NBER Working Paper No. 31865).",
  "research_question": "How and why do deposit pricing and demand elasticities differ between large and small banks, and what does that imply for monetary transmission?",
  "setting/data": "United States; deposit rates: RateWatch 2001–2019; bank financials: Call Reports 1984–2020; branch deposits: FDIC SOD; demographics: Data Axle. Sample distinguishes 14 large SCAP/CCAR banks vs others. (pp. 10–13)",
  "method": "Document uniform pricing and rate levels by bank size; residual variance decompositions (bank×time vs local HHI); structural demand estimation at bank-county cluster level (IV on cost shifters) to recover elasticities. (pp. 12–16, 31–36)",
  "key_mechanisms": [
    "Large banks offer superior liquidity services and set lower, more uniform deposit rates; small banks compete more on price. (pp. 2–3, 12–16)",
    "Customer preferences and bank technologies, not just local market concentration, drive pricing and elasticities. (pp. 2–3, 12–16, 31–36)"
  ],
  "main_findings": [
    "Large banks set lower rates: 12-mo CDs −0.49 to −0.54 pp, MM −0.24 pp, savings −0.31 pp vs small banks. (Table 3, p. 19)",
    "Rate variation is mostly bank-time, not local HHI: bank×time FE explain ~0.88–0.95 of residual variation across products. (Table 2, p. 15)",
    "Large-bank deposit share exceeds 50% nationally by the 2010s. (Fig. 4, p. 21)",
    "Estimated demand elasticities: small banks mean ≈ −0.644 vs large banks ≈ −0.445 (more rate-sensitive at small banks). (Table 6, p. 36)"
  ],
  "limits/caveats": [
    "Uniform-pricing evidence is strongest for large banks/products with broad coverage; some community banks still price locally. (pp. 12–16)",
    "Elasticities use county-cluster aggregation and instruments for costs; micro heterogeneity remains. (pp. 31–36)"
  ],
  "how_it_relates_to_my_project": [
    "Explains size-based heterogeneity you’re testing: small banks’ deposits should be more price-elastic and more fragile during hikes.",
    "Supports using bank×time variation rather than local HHI as the core identification margin, aligning with uniform pricing at large banks.",
    "Provides elasticities to calibrate expected deposit outflows and pass-through by size."
  ],
  "notable_quotes": [
    {"page": 2, "quote": "Large banks offer superior liquidity services but lower deposit rates, and locate where customers value their services."},
    {"page": 2, "quote": "Much of the variation in deposit-pricing behavior… reflects differences in ‘preferences and technologies’."}
  ]
}

{
  "citekey": "VanDenHeuvel2002",
  "full_citation": "Van den Heuvel, S. J. (2002). The bank capital channel of monetary policy. Manuscript, The Wharton School, University of Pennsylvania (This version: December 2002).",
  "research_question": "How do risk-based capital requirements and imperfect equity issuance create a bank capital channel that transmits monetary policy to lending?",
  "setting/data": "Model for U.S. banks; quarterly calibration; no microdata. Key calibration: capital ratio γ = 0.08, corporate tax τ = 0.40, loan maturity ≈ 4 years (δ ≈ 0.25), interest-rate states 4–7% with AR(1) persistence 0.9. (p. 23)",
  "method": "Dynamic bank balance-sheet model with maturity transformation, risk-based (Basel) capital constraints, and an imperfect market for bank equity; value-function solution and simulation; impulse responses to funds-rate and default shocks. (pp. 3–8, 19–25, 34–37)",
  "key_mechanisms": [
    "Maturity mismatch makes profits and capital sensitive to short-rate changes, tightening capital constraints after hikes. (pp. 10–11, 36)",
    "Imperfect equity issuance means retained earnings govern capital; capital affects lending even when constraints are slack. (pp. 9–11, 27)",
    "Binding capital regulation can initially decouple lending from policy within the period, then amplify responses later. (pp. 35–36)",
    "Precautionary behavior: banks cut new lending to build capital buffers even before constraints bind. (pp. 30–31)"
  ],
  "main_findings": [
    "Capital adequacy violations occur about 0.43% of periods; bankruptcy ≈ 0.02%. (p. 26)",
    "Regulatory constraint binds in ≈ 19% of periods in simulation. (p. 31)",
    "Precautionary cuts in new lending occur ≈ 40% of the time with mean reduction 5.6% when regulation is slack. (p. 31)",
    "Following a funds-rate hike, a poorly capitalized bank’s loan stock falls ≈ 0.9 percentage points more by 12 quarters than in the unconstrained case. (p. 36)",
    "With a high initial rate, the excess loan decline reaches ≈ 1.1 percentage points at 12 quarters. (p. 36)",
    "Calibrated market-to-book for equity averages q ≈ 1.16. (p. 24)"
  ],
  "limits/caveats": [
    "Partial-equilibrium model; general-equilibrium feedbacks discussed but not solved within the core model. (pp. 38–41)",
    "Assumes perfect access to insured non-reservable debt; no special role for reserves, which shifts focus entirely to equity constraints. (pp. 14–16)",
    "Loan demand held fixed to isolate supply; identification is model-based not causal in microdata. (pp. 23–24)"
  ],
  "how_it_relates_to_my_project": [
    "Provides a clean mechanism to separate funding-cost shocks (rate hikes) from capital-constraint effects when mapping to credit supply.",
    "Quantifies when lending responses are delayed or amplified by low capital, useful for your bank-size/sophistication heterogeneity tests.",
    "Offers impulse-response magnitudes (e.g., −0.9 to −1.1 pp at 12q) you can benchmark against your empirical lending regressions."
  ],
  "notable_quotes": [
    {"page": 4, "quote": "This gives rise to a ‘bank capital channel’ by which monetary policy affects bank lending through its impact on bank equity capital."},
    {"page": 41, "quote": "Monetary policy effects on bank lending depend on the capital adequacy of the banking sector."}
  ]
}

{
  "citekey": "EganLewellenSunderam2021",
  "full_citation": "Egan, M., Lewellen, S., & Sunderam, A. (2021). The cross section of bank value. Working paper. https://ssrn.com/abstract=2938065",
  "research_question": "How much of bank value is created by deposit-taking versus lending, and what primitives explain cross-sectional differences?",
  "setting/data": "United States; publicly listed bank holding companies; 1994–2015; 847 BHCs, 25,845 bank–quarter observations; sources include FR Y-9C (financials), FDIC Summary of Deposits (branches/deposits), RateWatch (rates), CRSP (market value), Census/CFPB (demographics/complaints). (pp. 10–13, 41) ",
  "method": "Two-division framework estimating bank ‘deposit productivity’ (BLP-style demand for deposits with instruments: pass-through to 3-m LIBOR and competitor characteristics) and ‘asset productivity’ (IV production function for interest income with bank/time FE). Then regress market-to-book on both primitives; decompose value and run bounding exercises for deposit–asset synergies. (pp. 7–13, 27–31, 43–47) ",
  "key_mechanisms": [
    "Liability-side ‘deposit productivity’ is a primitive that shifts deposit demand up for a given rate/inputs, creating franchise value. (pp. 7–9) ",
    "Deposit productivity loads most strongly on savings deposits, consistent with safety-driven value creation. (pp. 22–24, 47) ",
    "Deposit and asset productivities are positively correlated (synergies), but liability-side still explains more value. (pp. 18–20, 46) ",
    "Customer mix and technology (pricing, service quality) drive productivity heterogeneity across banks. (pp. 24–27, 49–51) "
  ],
  "main_findings": [
    "A 1 SD increase in deposit productivity is associated with +0.20 to +0.77 points in M/B; asset productivity +0.08 to +0.17 points (Table 4). (pp. 45–46) ",
    "Deposit productivity accounts for a mean ~64% share of bank value in the model-implied decomposition (Figure 4). (p. 40) ",
    "Deposit vs asset synergy: 1 SD higher deposit productivity correlates with ~0.45 SD higher asset productivity (Table 5a). (p. 46) ",
    "Savings deposit productivity explains over ~3× the M/B variation of other deposit types; savings average ~39% of deposits (Table 6). (p. 47) ",
    "Deposits comprise on average ~83% of liabilities in the sample (Table 1). (p. 41) "
  ],
  "limits/caveats": [
    "Sample limited to publicly listed, largely traditional banks; nontraditional activities are deemphasized. (pp. 1–3, 10) ",
    "Deposit rates in demand come from average paid expense (and RateWatch for instruments), not full product-level realized rates for all banks. (pp. 11–13, 27–29) ",
    "Identification hinges on BLP instruments and pass-through heterogeneity; measurement error and synergies are bounded but not eliminated. (pp. 12–13, 18–20, 52–58) "
  ],
  "how_it_relates_to_my_project": [
    "Gives a defensible, bank-level measure of the deposit franchise (‘deposit productivity’) you can use as a right-hand-side driver of funding costs and as a heterogeneity dimension in your lending equations.",
    "Shows savings deposits are the value core; motivates splitting deposit categories in your pass-through and outflow analyses.",
    "Quantifies how much liability-side strength explains cross-bank outcomes, supporting your focus on deposit-channel mechanisms over pure asset-side stories."
  ],
  "notable_quotes": [
    {"page": 1, "quote": "Deposit productivity is responsible for two-thirds of the value of the median bank and most variation in value across banks."},
    {"page": 23, "quote": "A bank’s ability to collect savings deposits is the main driver of value, explaining over three times as much variation in M/B as any other factor."}
  ]
}

{
  "citekey": "KashyapStein1997",
  "full_citation": "Kashyap, A. K., & Stein, J. C. (1997). What do a million banks have to say about the transmission of monetary policy? (NBER Working Paper No. 6056).",
  "research_question": "Does the effect of monetary policy on bank lending depend on banks’ balance-sheet liquidity and bank size, as predicted by the bank-lending channel?",
  "setting/data": "United States; 1976Q1–1993Q2; 961,530 bank-quarter observations from Call Reports, after screens (e.g., exclude merger quarters). Banks split into size bins (small = bottom 95% of assets). (p. 43; pp. 11–15, 21) ",
  "method": "Two-step design. Step 1: for each bank, estimate a time-series sensitivity (β) of loan growth to monetary policy indicators. Step 2: cross-sectional regressions of β on bank liquidity (B = cash+securities/assets) and size categories. Monetary policy measured three ways: Boschen–Mills index, federal funds rate, and Bernanke–Mihov VAR shock; robustness across measures. (pp. 17–20; Tables 4–7, pp. 52–63) ",
  "key_mechanisms": [
    "Less liquid banks cannot buffer funding shocks, so loan supply contracts more after tightening. (pp. 8–11)",
    "Small banks face costlier/limited access to non-deposit funding, amplifying sensitivity to policy. (pp. 9–11, 14–16)",
    "Cross-sectional identification uses variation in B and bank size to pin down loan-supply effects. (pp. 17–22)"
  ],
  "main_findings": [
    "For small banks’ C&I loans, the sum of policy coefficients is negative and significant in all six baseline cases; in four of six, p-values are < 0.6%. (p. 28)",
    "Cross-sectional magnitude: the “total movement in β” for small banks after a +100 bp funds-rate shock is ≈ −0.013. (p. 34)",
    "Using liquidity heterogeneity (10th vs 90th percentile B: ~25% vs ~65%), the illiquid bank’s C&I loan level is ≈ 0.5 percentage points lower one year after a +100 bp shock. (p. 34)",
    "Aggregate effect: one year after a +100 bp funds-rate shock, aggregate C&I lending by small banks is reduced by roughly 3%. (p. 35)",
    "Effects for total loans are weaker than for C&I loans; identification is sharpest on C&I. (pp. 21–23; Table 4, p. 53)"
  ],
  "limits/caveats": [
    "Potential biases from correlation between liquidity and loan-demand cyclicality; authors discuss ‘heterogeneous risk aversion’ vs ‘rational buffer-stocking.’ (pp. 24–27)",
    "Breaks/measurement: post-1984 reporting changes (e.g., acceptances, securities definitions) require care; results robust to alternative measures. (pp. 44–46)",
    "‘Quasi-IV’ approach reduces but does not eliminate endogeneity concerns. (pp. 35–38)"
  ],
  "how_it_relates_to_my_project": [
    "Gives a clean bank-supply design you can mirror for the U.S.: use bank size and liquidity to isolate loan-supply responses to funding shocks.",
    "Pairs naturally with your deposit-channel estimates: small banks with low liquid buffers should show stronger quantity contraction for a given funding-cost shock.",
    "Provides benchmark magnitudes (e.g., −0.013 β; ~−3% C&I over 1 year per +100 bp) to compare with your lending equations."
  ],
  "notable_quotes": [
    { "page": 2, "quote": "The impact of monetary policy on lending behavior is significantly more pronounced for banks with weak liquid balance sheets… entirely attributable to the smaller banks." },
    { "page": 34, "quote": "The most conservative estimate of the total movement in β for small banks following a 100 basis point funds rate shock is about −0.013." }
  ]
}

{
  "citekey": "BernankeGertler1995",
  "full_citation": "Bernanke, B. S., & Gertler, M. (1995). Inside the black box: The credit channel of monetary policy transmission. Journal of Economic Perspectives, 9(4), 27–48.",
  "research_question": "What is the credit channel of monetary transmission, and how do the balance-sheet and bank-lending mechanisms amplify the effects of policy on real activity?",
  "setting/data": "United States; monthly VARs using 1965–1993 data (12 lags) on real GDP, prices, commodity prices, and the federal funds rate; additional series for spending components and cash-flow measures. (pp. 31, 34)",
  "method": "Narrative and VAR evidence: shock the funds-rate equation and trace responses (“Facts 1–4”); then document balance-sheet and bank-lending channels via coverage ratios, interest-rate spreads, and terms-of-lending indicators. (pp. 30–33, 36–42)",
  "key_mechanisms": [
    "External finance premium: policy changes move the wedge between external and internal funds, amplifying real effects. (pp. 35–36)",
    "Balance-sheet channel: tighter policy weakens borrower net worth/cash flow and collateral values, raising borrowing costs. (pp. 36–38)",
    "Bank-lending channel: tighter policy raises banks’ funding costs and tightens loan supply, especially for bank-dependent borrowers. (pp. 40–42)"
  ],
  "main_findings": [
    "Timing: after a tightening, real GDP begins falling in ~4 months and bottoms around 24 months; the funds rate returns near trend within 9–12 months. (p. 31)",
    "Composition: residential investment drops fastest and most; consumer durables and nondurables follow; business fixed investment declines with a lag, driven mainly by equipment. (p. 33)",
    "Inventory dynamics: final demand falls quickly, inventories initially rise then fall; inventory disinvestment accounts for a large share of the output decline. (p. 32)",
    "Coverage ratio co-moves positively with the funds rate, signaling a contemporaneous cash-flow squeeze under tightening. (p. 37)",
    "Spreads/terms: CD–T-bill and prime–T-bill spreads widen; small-business credit terms tighten in tight-money episodes (e.g., sharp CD spread spike in 1981). (p. 42)"
  ],
  "limits/caveats": [
    "Bank-lending channel harder to isolate post-1980 due to deregulation and managed liabilities; difficult to cleanly separate from balance-sheet effects. (pp. 41–42)",
    "Credit aggregates are poor tests of the channel; the relevant object is the external finance premium, not loan quantities. (pp. 43–44)"
  ],
  "how_it_relates_to_my_project": [
    "Frames your empirical work: model funding shocks transmitting via external-finance premia and borrower balance sheets, not just via deposit rates.",
    "Justifies focusing on quantities (loan supply) when prices adjust slowly and on heterogeneity by borrower bank-dependence and cash-flow sensitivity.",
    "Provides defensible timing patterns for identification windows in your lending regressions (e.g., 0–24 months horizons)."
  ],
  "notable_quotes": [
    { "page": 28, "quote": "We don’t think of the credit channel as a distinct, free-standing alternative… but rather as a set of factors that amplify and propagate conventional interest rate effects." },
    { "page": 35, "quote": "Monetary policy affects not only the general level of interest rates, but also the size of the external finance premium." }
  ]
}

{
  "citekey": "WangWhitedWuXiao2020",
  "full_citation": "Wang, Y., Whited, T. M., Wu, Y., & Xiao, K. (2020). Bank market power and monetary policy transmission: Evidence from a structural estimation (NBER Working Paper No. 27258).",
  "research_question": "How much do bank market power, capital regulation, and financing frictions shape the pass-through of monetary policy to lending, and can low rates become contractionary?",
  "setting/data": "United States; 1994–2017. Sources include Call Reports, FDIC Summary of Deposits, RateWatch branch rates, CRSP, and FRED macro series. (pp. 6–7)",
  "method": "Dynamic bank industry model with deposit and loan market power, reserve/capital regulation, and costly non-reservable funding; demand estimated via BLP; structural parameters via simulated minimum distance; counterfactual decompositions and VAR cross-checks. (pp. 2–6, 22–27, 28–29, 51)",
  "key_mechanisms": [
    "Deposit market power channel: higher policy rates raise deposit markups as cash becomes costlier, shrinking deposits and loans. (pp. 3–5, 19–20)",
    "Loan market power channel: banks cut loan markups as rates rise, mitigating quantity declines. (pp. 3–5, 20)",
    "Bank capital channel: maturity mismatch and profits affect equity buffers that constrain lending. (pp. 3–5, 29–32)",
    "Costly external finance links deposit quantity shocks to loan supply. (pp. 3–5, 27)"
  ],
  "main_findings": [
    "Baseline sensitivity: a +100 bp funds-rate shock reduces aggregate bank lending by ≈ 1.548%. (Table 5, p. 51)",
    "Channel contributions (remove each): reserve requirement 7.88%; capital regulation 27.65%; deposit market power 35.91%; loan market power −23.39% (mitigating). (Table 5, p. 51)",
    "Reversal rate: when the funds rate is below ≈ 0.9%, further cuts become contractionary via capital effects. (Figure 5B, p. 32)",
    "External funding cost: at non-reservables ≈ 30% of deposits, marginal cost ≈ 0.30% above the funds rate; mean deposit spread ≈ 1.29%. (pp. 27, 50)",
    "Equity valuation: a +100 bp shock lowers bank equity by ≈ 1.93% in data; model implies ≈ 2.84%. (p. 28)",
    "Heterogeneity: loan sensitivity is ≈ −1.103% for large banks vs ≈ −1.758% for small banks. (Table 7, p. 54)"
  ],
  "limits/caveats": [
    "Demand identification relies on supply shifters (salaries, fixed-asset expenses) being orthogonal to unobserved demand; structural assumptions are crucial. (pp. 22–25)",
    "Reserve channel small in this period; results may differ under different regimes or with interest on reserves prominence. (Table 5, p. 51)",
    "General-equilibrium extension yields smaller sensitivities but similar qualitative channel ranking. (Appendix G, pp. 90–91)"
  ],
  "how_it_relates_to_my_project": [
    "Gives defensible magnitudes and a decomposition to benchmark your U.S. deposit-channel estimates and robustness checks.",
    "Motivates modeling deposit vs loan market power and capital constraints separately, matching your focus on bank-size/sophistication heterogeneity.",
    "The reversal-rate result informs identification in low-rate subsamples where price effects can flip sign through capital."
  ],
  "notable_quotes": [
    {"page": 2, "quote": "We find that bank market power plays an important role in determining the degree of monetary policy transmission."},
    {"page": 2, "quote": "When the federal funds rate falls below 0.9%,…further cuts in the policy rate can be contractionary."}
  ]
}

{
  "citekey": "NeumarkSharpe1992",
  "full_citation": "Neumark, D., & Sharpe, S. A. (1992). Market structure and the nature of price rigidity: Evidence from the market for consumer deposits. Quarterly Journal of Economics, 107(2), 657–680.",
  "research_question": "How does local deposit-market concentration affect the level of retail deposit rates and the (potentially asymmetric) speed at which banks adjust those rates to market-rate shocks?",
  "setting/data": "United States; Oct 1983–Nov 1987; 12,495 bank–month observations (49 months × 255 banks across 105 MSAs); products: six-month CDs and MMDAs; explanatory covariates include FDIC Herfindahl index (HERF), state branching restrictions, population growth; marginal cost proxied by six-month T-bill. (pp. 662–665, 663) ",
  "method": "Panel partial-adjustment (Koyck) model relating deposit rates to T-bill rates with market characteristics in both steady-state markdown and adjustment speed; stochastic two-regime switching model to allow different speeds when rates are above vs. below equilibrium (asymmetry). Identification comes from cross-market variation in concentration, holding common rate shocks fixed. (pp. 667–673) ",
  "key_mechanisms": [
    "Higher concentration reduces long-run deposit rates (more surplus extraction). (Table III, p. 669) ",
    "Adjustment is asymmetric and depends on concentration: slower upward moves from below equilibrium, faster downward from above. (pp. 671–677) ",
    "Overall sluggishness differs by product (MMDAs slower than 6-month CDs). (Table III, p. 669) "
  ],
  "main_findings": [
    "Level effect: OLS bank-mean regressions imply HERF coefficients ≈ −2.56 to −2.79; a 0.04 s.d. rise in HERF lowers average deposit rates by ≈10–11 bps; moving from least to most concentrated markets lowers ≈60 bps. (Table II, p. 666) ",
    "Average monthly speed of adjustment λ ≈ 0.33 for 6-month CDs and ≈ 0.25 for MMDAs. (Table III, p. 669) ",
    "Asymmetry: adjustment from above is notably faster than from below; for MMDAs, X_A − X_B ≈ 0.225 (long sample). (Table V, p. 677) ",
    "Concentration accounts for roughly 25–50% of the mean asymmetry in adjustment speeds (X_HERF(A−B)). (Table V, p. 677) "
  ],
  "limits/caveats": [
    "Deposit rates are the 'most commonly paid' weekly rates; tiering and within-month adjustments are not fully observed. (p. 663) ",
    "Concentration varies mainly cross-sectionally, so dynamic identification relies on common T-bill shocks. (pp. 659–661, 663) ",
    "Asymmetry’s microfoundations are not pinned down; tacit-collusion speculation is offered. (p. 678) "
  ],
  "how_it_relates_to_my_project": [
    "Benchmarks pass-through frictions you can use to calibrate the spread gap in your deposit-channel first stage.",
    "Concentration-linked asymmetry supports instruments based on local market power for predicting deposit rate adjustment and outflow risk.",
    "Product heterogeneity (MMDA vs CD) motivates splitting deposit categories in your estimations."
  ],
  "notable_quotes": [
    {"page": 660, "quote": "Banks in concentrated markets tend to be slower to increase interest rates on deposits, but faster to lower them in response to declining market rates."},
    {"page": 674, "quote": "Symmetry is overwhelmingly rejected at conventional significance levels."}
  ]
}

{
  "citekey": "HannanBerger1991",
  "full_citation": "Hannan, T. H., & Berger, A. N. (1997). The rigidity of prices: Evidence from the banking industry. Journal of Reprints for Antitrust Law and Economics, 27(1), 245–254. (Reprinted from American Economic Review, 81, Sept. 1991.)",
  "research_question": "How do market structure and bank characteristics shape the probability of changing retail deposit rates, and are upward vs. downward adjustments equally likely?",
  "setting/data": "United States; Sep 1983–Dec 1986; 12,179 MMDA price-change decisions for 398 banks in 132 MSAs; FRB Monthly Survey of Selected Deposits and Other Accounts; 3-month T-bill as benchmark; Herfindahl concentration; market ‘customer base’ (MS_i × income); bank size (ln assets). (pp. 251–252) ",
  "method": "Multinomial logit for three outcomes (increase/decrease/no change). Explanators include (Δr)^2, (Δr)^2×CR, (Δr)^2×MS_i I, ln assets. Separate equations for increases vs decreases permit asymmetry tests. (pp. 250–252) ",
  "key_mechanisms": [
    "More concentrated markets reduce responsiveness to rate shocks (negative (Δr)^2×CR). (p. 252) ",
    "Larger customer bases increase responsiveness (positive (Δr)^2×MS_i I). (p. 252) ",
    "Deposit rates are more rigid for increases than for decreases (asymmetric adjustment costs/expectations). (pp. 252–253) "
  ],
  "main_findings": [
    "Composition of outcomes: 2,471 increases, 5,338 decreases, 4,370 no changes. (p. 251) ",
    "At sample means, a 29 bp market-rate move yields ≈62% probability of a decrease after a fall vs ≈39% probability of an increase after a rise, evidencing greater upward rigidity. (p. 253) ",
    "Signs/importance: (Δr)^2×CR < 0, (Δr)^2×MS_i I > 0 for both increase and decrease equations; many coefficients highly significant. (Table I, p. 252) ",
    "Larger banks adjust more frequently (positive ln assets in both equations). (Table I, p. 252) "
  ],
  "limits/caveats": [
    "Assumes 3-month T-bill as banks’ marginal funding cost; alternative wholesale benchmarks could differ. (p. 251) ",
    "Monthly snapshot of ‘most common’ branch rates may miss intra-month dynamics. (p. 251) ",
    "Multiple plausible causes of asymmetry are discussed; not uniquely identified. (pp. 250–251, 253) "
  ],
  "how_it_relates_to_my_project": [
    "Establishes asymmetric pass-through you can encode via different adjustment regimes for hikes vs cuts in your deposit-channel first stage.",
    "Supports using local concentration and market size as sources of cross-bank variation in deposit responsiveness.",
    "Provides clear numerical illustrations you can cite when motivating stickiness in your introduction."
  ],
  "notable_quotes": [
    {"page": 247, "quote": "Price rigidity is significantly greater in markets characterized by higher levels of concentration."},
    {"page": 247, "quote": "Deposit rates are significantly more rigid when the stimulus for a change is upward rather than downward."}
  ]
}

{
  "citekey": "DrechslerSavovSchnabl2021",
  "full_citation": "Drechsler, I., Savov, A., & Schnabl, P. (2021). Banking on deposits: Maturity transformation without interest rate risk. The Journal of Finance, 76(3), 1091–1143.",
  "research_question": "Does maturity transformation create interest-rate risk for banks, or does the deposit franchise hedge it, and how do banks manage interest-sensitivity matching between income and expense?",
  "setting/data": "United States; aggregate bank NIM (1955–2017); repricing maturity for assets/liabilities (1997–2017); bank-level panel (1984–2017) with 8,086 banks having ≥60 quarters; event-study of FOMC shocks (1994–2007 scheduled meetings); sources: FDIC Call Reports & Historical Statistics, FDIC Summary of Deposits (branches), RateWatch branch rates, CRSP/Fama-French industry portfolios, H.15. (Figures 1–3; Table I; pp. 1101–1104, 1113) :contentReference[oaicite:26]{index=26}",
  "method": "Two complementary approaches. (i) Present-value approach: regress industry/stock returns around FOMC announcements on one-year yield changes. (ii) Cash-flow approach: estimate bank-level ‘betas’ of interest expense/income/ROA to Fed funds changes (quarterly D’s with lags). Cross-sectional and panel ‘beta-on-beta’ regressions test one-for-one matching; asset composition regressions relate expense betas to repricing maturity and securities share. A model shows the deposit franchise is negative-duration (swap-like). (pp. 1092–1096, 1111–1126) :contentReference[oaicite:27]{index=27}",
  "key_mechanisms": [
    "Deposit franchise keeps deposit rates low and insensitive; banks hedge by holding long-term fixed-rate assets, matching income and expense sensitivities. (pp. 1092–1094, 1108) :contentReference[oaicite:28]{index=28}",
    "One-for-one sensitivity matching insulates NIM/ROA from rate shocks. (pp. 1118–1120, 1124) :contentReference[oaicite:29]{index=29}",
    "Market power lowers expense betas; banks with lower expense betas hold longer-duration assets and more securities. (pp. 1129–1132, 1136–1139) :contentReference[oaicite:30]{index=30}"
  ],
  "main_findings": [
    "Repricing maturity averages: assets ≈ 4.23 years, liabilities ≈ 0.34 years; mismatch ≈ 3.9 years (1997–2017). (Figure 1, p. 1101) :contentReference[oaicite:31]{index=31}",
    "Despite the mismatch, a +100 bp shock lowers bank stocks ≈ 4.24% vs ≈ 3.71% for the market—far smaller than the ≈ 34% equity drop implied by naive duration math. (Figure 2, pp. 1102–1103) :contentReference[oaicite:32]{index=32}",
    "Aggregate NIM is stable (≈2.2–3.8%), with annual ΔNIM s.d. ≈ 0.15% and ≈ 0 correlation with Fed funds. (Panel A, Figure 3, p. 1104) :contentReference[oaicite:33]{index=33}",
    "Average expense and income betas are ≈0.345 and ≈0.351; cross-sectional matching slope ≈0.810 (all banks) and ≈1.051 (top 5%); panel δ ≈0.886. (Table I p. 1114; Table II p. 1119–1120; Table IV p. 1124) :contentReference[oaicite:34]{index=34}",
    "Expense beta strongly predicts asset duration (slope ≈ −4.5 years) and lower securities share for high-beta banks. (Figure 9 p. 1129; Table VI pp. 1131–1132) :contentReference[oaicite:35]{index=35}",
    "Market-power instruments: bank HHI reduces expense beta (≈ −0.094 per unit), and retail deposit betas predict expense betas; induced changes are matched one-for-one in income. (Tables VIII–IX, pp. 1136–1139) :contentReference[oaicite:36]{index=36}"
  ],
  "limits/caveats": [
    "A key part of exposure—the deposit franchise—is off balance sheet (not capitalized); book vs. market accounting issues are discussed. (pp. 1095–1096, 1104–1106) :contentReference[oaicite:37]{index=37}",
    "Model abstracts from default risk; derivatives use exists (≈26% of banks) but results hold with/without users. (pp. 1110, 1106) :contentReference[oaicite:38]{index=38}"
  ],
  "how_it_relates_to_my_project": [
    "Gives measurement for ‘expense beta’ and shows one-for-one matching as a falsification check in your bank-level regressions.",
    "Links market power to funding-cost sensitivity, supporting instruments based on local concentration or retail deposit betas.",
    "Supplies magnitudes for interpreting funding-mix shifts and for separating price vs. quantity channels in your lending equations."
  ],
  "notable_quotes": [
    {"page": 1091, "quote": "We show that maturity transformation does not expose banks to interest rate risk—it hedges it."},
    {"page": 1108, "quote": "The deposit franchise functions like an interest rate swap whereby the bank pays the fixed leg and receives the floating leg."}
  ]
}
{
  "citekey": "ChoiRocheteau2021",
  "full_citation": "Choi, M., & Rocheteau, G. (2021). A model of retail banking and the deposits channel of monetary policy. SSRN Working Paper (Nov 2021).",
  "research_question": "Can a microfounded model of retail deposit markets explain a deposits channel of monetary policy and its dependence on information, market power, and fintech innovations?",
  "setting/data": "Theory with calibration to U.S. facts; stylized evidence compiled from Call Reports 1990Q1–2020Q4 on deposit spreads by product, correlations of deposit growth with ΔFFR, and semi-elasticities (pp. 4–6). ",
  "method": "Dynamic search-theoretic retail-banking model with bilateral relationships; complete- vs incomplete-information versions; generalized Nash/bargaining and second-degree price discrimination over deposit contracts; extension with two-sided bargaining and free entry linking concentration to outside options; comparative statics and calibrated quantitative exercises (pp. 3–4). ",
  "key_mechanisms": [
    "With private information, a higher policy rate widens the deposit spread and contracts aggregate deposits; the channel is stronger when markets are more concentrated (pp. 3–4). ",
    "Deposit outflow is concentrated among low-liquidity-needs consumers; pass-through is larger for small deposits than for large ones; with imperfectly liquid deposits the deposit–rate relation can be non-monotone (pp. 4, 24). ",
    "Fintech that improves outside options (online/mobile, CBDC) weakens transmission; better information that enables price discrimination can also weaken it (pp. 4–6). "
  ],
  "main_findings": [
    "Empirical targets summarized: a 100 bp funds-rate increase raises the deposit spread by about 54 bps (p. 5). ",
    "Pass-through differs by product: coefficients ~0.875 (checkable), 0.415 (savings), 0.238 (small time deposits) in Figure 1 (p. 5). ",
    "Aggregate deposits are strongly negatively correlated with ΔFFR (corr ≈ −0.49); by product, corr ≈ −0.28 (checkable), −0.55 (savings), and +0.30 (small time) (pp. 5–6). ",
    "Semi-elasticity benchmark: +100 bp FFR → ≈ 3.23 pp contraction in deposits (p. 5). "
  ],
  "limits/caveats": [
    "Quantitative implications depend on calibration choices and mapping from structural types to observed products (pp. 3–6). ",
    "Stylized facts are taken from prior literature; the paper itself does not provide new microdata estimation (pp. 4–6). "
  ],
  "how_it_relates_to_my_project": [
    "Gives a theory-consistent decomposition you can test: price pass-through → deposit outflows concentrated among low-liquidity types → quantity/credit effects; aligns with your bank-level identification of funding-cost shocks.",
    "Predicts stronger transmission in more concentrated markets, justifying interactions with HHI/depositor sophistication you already consider.",
    "Warns that fintech/online competition and information about customers change the strength of the channel; useful for heterogeneity and period splits."
  ],
  "notable_quotes": [
    { "page": 34, "quote": "When consumers have private information about their liquidity needs, a deposits channel emerges." },
    { "page": 4, "quote": "Deposit rates are lower in more concentrated markets; passthrough and the strength of the deposits channel are higher when concentration is higher." }
  ]
}

