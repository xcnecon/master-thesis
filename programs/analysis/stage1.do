global root "C:\Users\CHENY\Documents\GitHub\thesis-bank"
global data "$root/data"
global result "$root/results"
global working "$data/working"

*******************************************************
* Stage-1 regressions: pass-through to deposit rates and quantities
*  - Outcomes: d_interest_rate_on_deposit, d_average_deposit,
*              d_average_interest_bearing_depos, d_total_loans_not_for_sale, d_ci
*  - Deposit-weighted region shares: NE MA EC WC SA ES WS MT (PC omitted)
*  - Policy shock: d_ffr (quarterly change in FFR)
*******************************************************

clear all
set more off

*------------------------------------------------------
* 0. Install reghdfe if needed
*------------------------------------------------------
cap which reghdfe
if _rc {
    ssc install reghdfe, replace
    ssc install ftools,  replace
}

*------------------------------------------------------
* 1. Import data and build panel
*------------------------------------------------------
import delimited "$working/working_panel.csv", clear varnames(1) stringcols(_all)

* Convert all non-date variables from string to numeric when possible
ds date, not
local vars_nodate `r(varlist)'
capture destring `vars_nodate', replace ignore(",")

* Convert Date (string) to daily date; adjust "YMD" if your format differs
gen float date_d = daily(date, "YMD")
format date_d %td

* Quarterly date
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
ds, has(type numeric)
recast float `r(varlist)'

xtset bankid qdate

* Keep 2022Q1–2023Q4 = hike + plateau window
keep if inrange(qdate, tq(2022q1), tq(2023q4))

*------------------------------------------------------

*------------------------------------------------------
* 3. Define analysis sample
*   (you can add more variables to the missing() list if needed)
*------------------------------------------------------
gen byte sample_stage1 = ///
    !missing(d_interest_rate_on_deposit, d_ffr, ///
             ne, ma, ec, wc, sa, es, ws, mt, pc)

* Prepare results logging
cap mkdir "$result"
capture log close stage1
log using "$result/stage1_results.log", text replace name(stage1)

*------------------------------------------------------
* 4. Stage-1 regression
*
* Bank FE: absorbed via absorb(bankid)
* Quarter FE: i.qdate
* Deposit-weighted region×quarter controls:
*   c.<region_share>#i.qdate, with PC omitted to avoid perfect collinearity
*------------------------------------------------------
// Outcome: cum_d_interest_rate_on_deposit
reghdfe cum_d_interest_rate_on_deposit ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        if sample_stage1, ///
        absorb(bankid) ///
        cluster(bankid)
		
reghdfe cum_d_interest_rate_on_deposit ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        if sample_stage1 & large_bank==0, ///
        absorb(bankid) ///
        cluster(bankid)

// Outcome: cum_d_interest_rate_on_interest_bearing_deposit
reghdfe cum_d_interest_rate_on_interest_ ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        if sample_stage1, ///
        absorb(bankid) ///
        cluster(bankid)
		
reghdfe cum_d_interest_rate_on_interest_ ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        if sample_stage1 & large_bank==0, ///
        absorb(bankid) ///
        cluster(bankid)

*------------------------------------------------------
* Outcome: d_average_deposit

reghdfe d_average_deposit ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        if sample_stage1, ///
        absorb(bankid) ///
        cluster(bankid)
		
reghdfe d_average_deposit ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        if sample_stage1 & large_bank==0, ///
        absorb(bankid) ///
        cluster(bankid)


* Outcome: d_average_interest_bearing_depos
reghdfe d_average_interest_bearing_depos ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        if sample_stage1, ///
        absorb(bankid) ///
        cluster(bankid)
		
reghdfe d_average_interest_bearing_depos ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        if sample_stage1 & large_bank==0, ///
        absorb(bankid) ///
        cluster(bankid)

* Outcome: d_core_deposit
reghdfe d_core_deposit ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        if sample_stage1, ///
        absorb(bankid) ///
        cluster(bankid)

reghdfe d_core_deposit ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        if sample_stage1 & large_bank==0, ///
        absorb(bankid) ///
        cluster(bankid)
*------------------------------------------------------
* Outcome: d_total_loans_not_for_sale
reghdfe d_total_loans_not_for_sale ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        if sample_stage1, ///
        absorb(bankid) ///
        cluster(bankid)

reghdfe d_total_loans_not_for_sale ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        if sample_stage1 & large_bank == 0, ///
        absorb(bankid) ///
        cluster(bankid)


* Close results log
log close stage1