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
log using "$result/appendix_results.log", text replace name(combined)

// small banks only
* Loans not for sale — small banks
ivreghdfe d_total_loans_not_for_sale ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (cum_d_interest_rate_on_deposit = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr) ///
        if large_bank==0, ///
        absorb(bankid) ///
        cluster(bankid)

ivreghdfe d_total_loans_not_for_sale ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (cum_d_interest_rate_on_interest_ = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr) ///
        if large_bank==0, ///
        absorb(bankid) ///
        cluster(bankid)

ivreghdfe d_total_loans_not_for_sale ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (d_core_deposit = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr) ///
        if large_bank==0, ///
        absorb(bankid) ///
        cluster(bankid)

ivreghdfe d_total_loans_not_for_sale ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (cum_d_core_deposit = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr) ///
        if large_bank==0, ///
        absorb(bankid) ///
        cluster(bankid)

// loan sub-categories
ivreghdfe d_single_family_loans ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (cum_d_interest_rate_on_deposit = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr), ///
        absorb(bankid) ///
        cluster(bankid)

ivreghdfe d_multifamily_loans ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (cum_d_interest_rate_on_deposit = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr), ///
        absorb(bankid) ///
        cluster(bankid)

ivreghdfe d_ci ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (cum_d_interest_rate_on_deposit = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr), ///
        absorb(bankid) ///
        cluster(bankid)

log close combined