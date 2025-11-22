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
* 2. Sample definition
*------------------------------------------------------
* Baseline sample: non-missing main variables and instrument
gen byte sample_stage2 = !missing(d_total_loans, d_interest_rate_on_deposit, ///
    lag1_roa, lag1_core_deposit_share, lag1_wholesale_share, ///
    lag1_asset_to_equity, lag1_log_asset, ///
    large_bank, zS_dffr, ///
    ne, ma, ec, wc, sa, es, ws, mt, pc)

label var sample_stage2 "=1 if observation used in Stage 2 IV regressions"

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
ivreghdfe d_total_loans ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (d_interest_rate_on_deposit = zS_dffr) ///
        if sample_stage2, ///
        absorb(bankid) ///
        cluster(bankid)

* 5.2 Large banks only
ivreghdfe d_total_loans ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (d_interest_rate_on_deposit = zR_dffr) ///
        if sample_stage2 & large_bank == 1, ///
        absorb(bankid) ///
        cluster(bankid)

* 5.3 Small banks only
ivreghdfe d_total_loans ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (d_interest_rate_on_deposit = zS_dffr) ///
        if sample_stage2 & large_bank == 0, ///
        absorb(bankid) ///
        cluster(bankid)

* 5.1 Full sample
ivreghdfe d_single_family_loans ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (d_interest_rate_on_deposit = zS_dffr) ///
        if sample_stage2, ///
        absorb(bankid) ///
        cluster(bankid)

* 5.2 Large banks only
ivreghdfe d_single_family_loans ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (d_interest_rate_on_deposit = zR_dffr) ///
        if sample_stage2 & large_bank == 1, ///
        absorb(bankid) ///
        cluster(bankid)

* 5.3 Small banks only
ivreghdfe d_single_family_loans ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (d_interest_rate_on_deposit = zS_dffr) ///
        if sample_stage2 & large_bank == 0, ///
        absorb(bankid) ///
        cluster(bankid)

* 5.1 Full sample
ivreghdfe d_ci ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (d_interest_rate_on_deposit = zS_dffr) ///
        if sample_stage2, ///
        absorb(bankid) ///
        cluster(bankid)

* 5.2 Large banks only
ivreghdfe d_ci ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (d_interest_rate_on_deposit = zR_dffr) ///
        if sample_stage2 & large_bank == 1, ///
        absorb(bankid) ///
        cluster(bankid)

* 5.3 Small banks only
ivreghdfe d_ci ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        (d_interest_rate_on_deposit = zS_dffr) ///
        if sample_stage2 & large_bank == 0, ///
        absorb(bankid) ///
        cluster(bankid)

local controls lag1_roa lag1_core_deposit_share lag1_wholesale_share ///
               lag1_asset_to_equity lag1_log_asset


*------------------------------------------------------
* 5b. IV regressions (+ lagged bank controls)
*------------------------------------------------------

* 5b.1 Full sample
ivreghdfe d_total_loans ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        `controls' ///
        (d_interest_rate_on_deposit = zS_dffr) ///
        if sample_stage2, ///
        absorb(bankid) ///
        cluster(bankid)

* 5b.2 Large banks only
ivreghdfe d_total_loans ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        `controls' ///
        (d_interest_rate_on_deposit = zR_dffr) ///
        if sample_stage2 & large_bank == 1, ///
        absorb(bankid) ///
        cluster(bankid)

* 5b.3 Small banks only
ivreghdfe d_total_loans ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        `controls' ///
        (d_interest_rate_on_deposit = zS_dffr) ///
        if sample_stage2 & large_bank == 0, ///
        absorb(bankid) ///
        cluster(bankid)

* 5b.1 Full sample
ivreghdfe d_single_family_loans ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        `controls' ///
        (d_interest_rate_on_deposit = zS_dffr) ///
        if sample_stage2, ///
        absorb(bankid) ///
        cluster(bankid)

* 5b.2 Large banks only
ivreghdfe d_single_family_loans ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        `controls' ///
        (d_interest_rate_on_deposit = zR_dffr) ///
        if sample_stage2 & large_bank == 1, ///
        absorb(bankid) ///
        cluster(bankid)

* 5b.3 Small banks only
ivreghdfe d_single_family_loans ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        `controls' ///
        (d_interest_rate_on_deposit = zS_dffr) ///
        if sample_stage2 & large_bank == 0, ///
        absorb(bankid) ///
        cluster(bankid)

* 5b.1 Full sample
ivreghdfe d_ci ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        `controls' ///
        (d_interest_rate_on_deposit = zS_dffr) ///
        if sample_stage2, ///
        absorb(bankid) ///
        cluster(bankid)

* 5b.2 Large banks only
ivreghdfe d_ci ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        `controls' ///
        (d_interest_rate_on_deposit = zR_dffr) ///
        if sample_stage2 & large_bank == 1, ///
        absorb(bankid) ///
        cluster(bankid)

* 5b.3 Small banks only
ivreghdfe d_ci ///
        i.qdate ///
        c.ne#i.qdate c.ma#i.qdate c.ec#i.qdate c.wc#i.qdate ///
        c.sa#i.qdate c.es#i.qdate c.ws#i.qdate c.mt#i.qdate ///
        `controls' ///
        (d_interest_rate_on_deposit = zS_dffr) ///
        if sample_stage2 & large_bank == 0, ///
        absorb(bankid) ///
        cluster(bankid)


*------------------------------------------------------
* 6. Wrap up
*------------------------------------------------------
log close stage2
