global root "C:\Users\CHENY\Documents\GitHub\thesis-bank"
global data "$root/data"
global result "$root/results"
global working "$data/working"

*******************************************************
* Combined Stage 1 + Stage 2 analysis
*  - Stage 1: Pass-through to deposit rates and quantities
*  - Stage 2: Effect of deposit rate changes on loan growth (IV)
*  - Keep a single log file
*******************************************************

clear all
set more off

*------------------------------------------------------
* 0. Dependencies
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
import delimited "$working/robustness_panel.csv", clear varnames(1) stringcols(_all)

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

global control "roa asset_to_equity core_deposit_share wholesale_share log_asset"

*------------------------------------------------------
* 3. Open single results log
*------------------------------------------------------
cap mkdir "$result"
capture log close combined
log using "$result/robustness_results.log", text replace name(combined)

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

test c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr

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

test c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr

reghdfe cum_d_average_interest_bearing_d ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
		, ///
        absorb(bankid) ///
        cluster(bankid)

test c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr


* Outcome: d_average_interest_bearing_depos
* All banks
reghdfe d_average_interest_bearing_depos ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        $control ///
        , ///
        absorb(bankid) ///
        cluster(bankid)

* Joint significance of {zS, zR, zH}×cum ΔFFR
test c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr

* Outcome: d_average_deposit
reghdfe d_average_interest_bearing_depos ///
        c.sophistication_index#c.cum_d_ffr ///
		c.branch_density_z#c.cum_d_ffr ///
		c.hhi_z#c.cum_d_ffr ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        $control ///
        , ///
        absorb(bankid) ///
        cluster(bankid)

test c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr


ivreghdfe d_total_loans ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (cum_d_interest_rate_on_interest_ = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr), ///
        absorb(bankid) ///
        cluster(bankid)

* Loans not for sale — all banks
ivreghdfe d_total_loans_not_for_sale ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (cum_d_interest_rate_on_interest_ = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr), ///
        absorb(bankid) ///
        cluster(bankid)

ivreghdfe d_total_loans ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        $control ///
        (cum_d_interest_rate_on_interest_ = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr), ///
        absorb(bankid) ///
        cluster(bankid)

* Loans not for sale — all banks
ivreghdfe d_total_loans_not_for_sale ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        $control ///
        (cum_d_interest_rate_on_interest_ = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr), ///
        absorb(bankid) ///
        cluster(bankid)

* Single-family mortgages — all banks
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

* Commercial & industrial loans — all banks
ivreghdfe d_ci ///
		c.metro_dummy#c.cum_d_ffr ///
		c.log_median_hh_income_z#c.cum_d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (cum_d_interest_rate_on_deposit = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr), ///
        absorb(bankid) ///
        cluster(bankid)

*------------------------------------------------------
* 2. Close log
*------------------------------------------------------
log close combined