*******************************************************
* Stage 2: Effect of deposit rate changes on loan growth
*------------------------------------------------------
* Endogenous regressor : d_interest_rate_on_deposit
* Instrument           : zS_dffr
* Baseline controls    : quarter FE and deposit-weighted region×quarter FE
* Samples              : full / large_bank / small_bank
*******************************************************


*------------------------------------------------------
* 0. Dependencies
*------------------------------------------------------
cap which ivreghdfe
if _rc {
    ssc install ivreghdfe, replace
    ssc install reghdfe,   replace
    ssc install ftools,    replace
    ssc install ivreg2,    replace
    ssc install ranktest,  replace
}
mata: mata mlib index

* Panel declaration (for reference)
xtset bankid qdate

* Keep 2022Q1–2023Q4 = hike + plateau window
keep if inrange(qdate, tq(2022q1), tq(2023q4))


*------------------------------------------------------
* 3. Descriptive checks (optional)
*------------------------------------------------------
* You can uncomment these if you want to inspect the data

* summarize d_total_loans d_interest_rate_on_deposit zS_dffr if sample_stage2
* tab large_bank if sample_stage2

*------------------------------------------------------
* 4. Log file
*------------------------------------------------------
capture log close stage2
cap mkdir "$result"
log using "$result/stage2_results.log", text replace name(stage2)

*------------------------------------------------------
* 5. IV regressions (baseline, no lagged bank controls)
*------------------------------------------------------

* 5.1 Full sample
ivreghdfe d_total_loans_not_for_sale ///
		c.metro_dummy#c.d_ffr ///
		c.log_median_hh_income_z#c.d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (d_interest_rate_on_interest_ = c.sophistication_index#c.d_ffr c.branch_density_z#c.d_ffr c.hhi_z#c.d_ffr), ///
        absorb(bankid) ///
        cluster(bankid)
		
ivreghdfe d_total_loans_not_for_sale ///
		c.metro_dummy#c.d_ffr ///
		c.log_median_hh_income_z#c.d_ffr ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (d_interest_rate_on_interest_bear = c.sophistication_index#c.d_ffr c.branch_density_z#c.d_ffr c.hhi_z#c.d_ffr), ///
        absorb(bankid) ///
        cluster(bankid)

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
        (cum_d_interest_rate_on_interest_ = c.sophistication_index#c.cum_d_ffr c.branch_density_z#c.cum_d_ffr c.hhi_z#c.cum_d_ffr), ///
        absorb(bankid) ///
        cluster(bankid)

*------------------------------------------------------
* 6. Wrap up
*------------------------------------------------------
log close stage2
