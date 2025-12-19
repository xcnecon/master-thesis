global root "C:\Users\CHENY\Documents\GitHub\thesis-bank"
global data "$root/data"
global result "$root/results"
global working "$data/working"

*******************************************************
* Robustness analysis: Stage 1 (first stage) + Stage 2 (IV)
* Sections:
*   1) Setup and data preparation
*   2) Stage 1 robustness: pass-through to deposit rates/quantities
*   3) Stage 2 robustness: IV effect of deposit pricing/quantities on loans
* Identification:
*   - Instruments: zS (sophistication), zR (branch density), zH (HHI),
*     each interacted with cum ΔFFR (policy slope shifters)
*   - Fixed effects: bank FE; time FE: quarter FE
*   - Region×Quarter controls: deposit-weighted region shares × quarter FE
*     (PC omitted). Absorb geography-time demand/supply shifts
* Sample window: 2022q1–2023q4 (hike + plateau)
* Output: results/robustness_results.log
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
* 1) Setup and data preparation
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

*------------------------------------------------------
* Notes on sample and controls
*  - Require non-missing outcomes, policy shock, and region-share controls
*  - Interactions with i.qdate are formed later; PC share is omitted
*  - All models: cluster SEs by bank and absorb bank FE + quarter FE
*------------------------------------------------------

*------------------------------------------------------
* Open results log (setup)
*------------------------------------------------------
cap mkdir "$result"
capture log close combined
log using "$result/robustness_results.log", text replace name(combined)
 
*------------------------------------------------------
* 2) Stage 1 robustness: pass-through to deposit pricing and quantities
*    - Variants: levels vs first-differences; all vs interest-bearing; core share
*    - Controls: bank FE; quarter FE; region×quarter shares (PC omitted)
*    - For each block, report joint F-tests of {zS,zR,zH}×cum ΔFFR
*------------------------------------------------------

* 2a) Deposit rate (levels): all deposits — cum Δ deposit rate
reghdfe cum_d_interest_rate_on_deposit ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        , ///
        absorb(bankid) ///
        cluster(bankid)

* Joint significance of {zS, zR, zH}×cum ΔFFR
test c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr

reghdfe cum_d_interest_rate_on_interest_ ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        , ///
        absorb(bankid) ///
        cluster(bankid)

* Joint significance of {zS, zR, zH}×cum ΔFFR
test c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr

* 2d) Deposit rate (first-difference): all deposits — Δ deposit rate
reghdfe d_interest_rate_on_deposit ///
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

reghdfe d_interest_rate_on_interest_bear ///
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

* 2e) Deposit quantity (first-difference): average deposits
reghdfe d_core_deposit ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        , ///
        absorb(bankid) ///
        cluster(bankid)

* Joint significance of {zS, zR, zH}×cum ΔFFR
test c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr

* 2f) Deposit quantity (first-difference): interest-bearing deposits
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

* 2g) Deposit composition (first-difference): core deposit share
reghdfe d_average_interest_bearing_depos ///
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

* 2h) Deposit quantity (cum change): average deposits
reghdfe cum_d_average_deposit ///
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

*------------------------------------------------------
* 3) Stage 2 robustness: IV effect on loan growth
*    - Endogenous regressor variants:
*       3a) cum_d_interest_rate_on_interest_ (pricing, levels)
*       3b) d_average_interest_bearing_depos (quantities, first-difference)
*       3c) cum_d_average_deposit (quantities, cum change)
*    - Instruments: {zS, zR, zH}×cum ΔFFR
*    - Same FE and controls as Stage 1
*------------------------------------------------------
* ------------------------
/// without metro and income controls
ivreghdfe d_total_loans_not_for_sale ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (cum_d_interest_rate_on_deposit = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr) ///
        , ///
        absorb(bankid) ///
        cluster(bankid)

ivreghdfe d_total_loans_not_for_sale ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (cum_d_core_deposit = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr) ///
        , ///
        absorb(bankid) ///
        cluster(bankid)

* 3c) Quantities (cum change): instrument cum_d_average_deposit
ivreghdfe d_total_loans_not_for_sale ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (cum_d_average_deposit = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr) ///
        , ///
        absorb(bankid) ///
        cluster(bankid)

ivreghdfe d_total_loans_not_for_sale ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (cum_d_average_interest_bearing_d = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr) ///
        , ///
        absorb(bankid) ///
        cluster(bankid)

*------------------------------------------------------
* End — close log
log close combined