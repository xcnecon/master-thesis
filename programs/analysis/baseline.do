global root "C:\Users\CHENY\Documents\GitHub\thesis-bank"
global data "$root/data"
global result "$root/results"
global working "$data/working"

*******************************************************
* Combined Stage 1 + Stage 2 analysis (master do-file)
* Purpose:
*  - Stage 1: Estimate pass-through of policy (cum ΔFFR) to banks'
*    deposit rates and deposit quantities.
*  - Stage 2: IV effect of cum ΔDeposit rate on loan growth.
* Identification:
*  - Instruments = sophistication (zS), branch density (zR), market
*    concentration (zH) interacted with cum ΔFFR (policy slope shifters).
*  - Fixed effects: bank FE; time FE: quarter FE.
*  - Region×Quarter controls: deposit-weighted region shares × quarter FE
*    (PC omitted). Controls absorb geography-time demand/supply shifts.
* Sample window:
*  - 2022q1–2023q4 (hike + plateau). We report all banks and small banks
*    (large_bank==0) specifications.
* Output:
*  - Single text log at results/regressions_results.log
*******************************************************

clear all
set more off

*------------------------------------------------------
* 0. Dependencies
*  - Ensure packages are installed only if missing.
*  - ivreghdfe relies on ivreg2 and ranktest for weak-ID tests.
*------------------------------------------------------
cap which reghdfe
if _rc {
    ssc install reghdfe, replace
    ssc install ftools,  replace
}
cap which ivreghdfe
if _rc {
    ssc install ivreghdfe, replace
    ssc install reghdfe,   replace
    ssc install ftools,    replace
    ssc install ivreg2,    replace
    ssc install ranktest,  replace
}
mata: mata mlib index

*------------------------------------------------------
* 1. Import data and build panel
*------------------------------------------------------
* Load pre-built working panel; read all columns as strings to avoid
* locale-dependent type guessing. We explicitly destring below.
import delimited "$working/working_panel.csv", clear varnames(1) stringcols(_all)

* Convert all non-date variables from string to numeric when possible
ds date, not
local vars_nodate `r(varlist)'
capture destring `vars_nodate', replace ignore(",")

* Convert string 'date' to Stata daily, then quarterly date used for FE.
* Adjust "YMD" if the raw format differs
gen float date_d = daily(date, "YMD")
format date_d %td

* Quarterly date key
gen qdate = qofd(date_d)
format qdate %tq

* Panel declaration (not required by reghdfe, but good practice)
* Ensure bankid is numeric (encode if still string)
capture confirm numeric variable bankid
if _rc {
    encode bankid, gen(bankid_num)
    drop bankid
    rename bankid_num bankid
}

* Recast all numeric variables (including dates and ids) to float
* (saves memory and yields consistent storage types)
ds, has(type numeric)
recast float `r(varlist)'

xtset bankid qdate

* Keep 2022Q1–2023Q4 = hike + plateau window
keep if inrange(qdate, tq(2022q1), tq(2023q4))

global control "roa asset_to_equity core_deposit_share wholesale_share log_asset"

*------------------------------------------------------
* 2. Define analysis sample for Stage 1
*------------------------------------------------------
* Require non-missing outcomes, policy shock, and region-share controls.
* Interactions with i.qdate are formed later; PC share is omitted.

*------------------------------------------------------
* 3. Open single results log
*------------------------------------------------------
cap mkdir "$result"
capture log close combined
log using "$result/regressions_results.log", text replace name(combined)

*------------------------------------------------------
* 4. Stage-1 regressions
*  - Outcomes: deposit rate changes and deposit quantities
*  - Bank FE via absorb(bankid); Quarter FE: i.qdate
*  - Region×Quarter controls: c.<region_share>#i.qdate (PC omitted)
*  - Policy slope shifters: c.<shifter>#c.cum_d_ffr with shifters {zS, zR, zH}
*  - We report joint F-tests for {zS, zR, zH}×cum ΔFFR
*------------------------------------------------------
// Outcome: cum_d_interest_rate_on_deposit
* All banks
reghdfe cum_d_interest_rate_on_deposit ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        , ///
        absorb(bankid) ///
        cluster(bankid)

* Joint significance of {zS, zR, zH}×cum ΔFFR
test c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr

reghdfe cum_d_interest_rate_on_deposit ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        if large_bank==0, ///
        absorb(bankid) ///
        cluster(bankid)

* Joint significance of {zS, zR, zH}×cum ΔFFR
test c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr

* Outcome: d_average_interest_bearing_depos
* All banks
reghdfe d_average_deposit ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        , ///
        absorb(bankid) ///
        cluster(bankid)

* Joint significance of {zS, zR, zH}×cum ΔFFR
test c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr

reghdfe d_average_deposit ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        if large_bank==0, ///
        absorb(bankid) ///
        cluster(bankid)

* Joint significance of {zS, zR, zH}×cum ΔFFR
test c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr

*------------------------------------------------------
* 5. Stage-2 IV regressions (baseline, no lagged bank controls)
*  - Endogenous regressor: cum_d_interest_rate_on_deposit (cum Δ deposit rate)
*  - Instrument set: zS, zR, zH × cum ΔFFR
*  - Controls: bank FE, quarter FE, region×quarter controls
*  - Weak-ID diagnostics (KP rk tests) reported in the log
*------------------------------------------------------

* Loans not for sale — all banks
ivreghdfe d_total_loans_not_for_sale ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (cum_d_interest_rate_on_deposit = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr), ///
        absorb(bankid) ///
        cluster(bankid)

ivreghdfe d_total_loans_not_for_sale ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (d_average_deposit = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr) ///
        if large_bank==0, ///
        absorb(bankid) ///
        cluster(bankid)

* Loans not for sale — small banks
ivreghdfe d_total_loans_not_for_sale ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (d_average_deposit = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr) ///
        , ///
        absorb(bankid) ///
        cluster(bankid)

ivreghdfe d_total_loans_not_for_sale ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (d_average_deposit = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr) ///
        if large_bank==0, ///
        absorb(bankid) ///
        cluster(bankid)

*------------------------------------------------------
* 6. Close log
*------------------------------------------------------
log close combined