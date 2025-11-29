* estout required

* --- in-window dummy pattern matching docs --- *

eststo clear

import delimited "intermediate/regression/pattern_matching_in_window/labels.csv", clear ///
    varnames(1) ///
    stringcols(_all)
destring topic, replace

levelsof topic, local(topic_levels)
foreach t of local topic_levels {
    quietly levelsof label if topic == `t', local(lbl)
    local name = subinstr("`t'", "-", "m", .)
    local topic_label_`name' "`lbl'"
}

import delimited "intermediate/regression/pattern_matching_in_window/data.csv", clear ///
    varnames(1) ///
    stringcols(_all) ///
    bindquote(strict)
destring weeks_to_nearest_tuesday, replace
destring weeks_to_nearest_election, replace


gen in_window_dummy = (weeks_to_nearest_tuesday >= -4 & weeks_to_nearest_tuesday <= 4)
gen election_year_dummy = (weeks_to_nearest_election >= -44 & weeks_to_nearest_election <= 8)
gen interaction = in_window_dummy * election_year_dummy


preserve

gen mentions = strtrim(mentioned_topics) != "[]"

* OLS regression
eststo: regress mentions in_window_dummy election_year_dummy interaction, robust
estadd ysumm

predict pred, xb

collapse (mean) mentions pred, by(weeks_to_nearest_tuesday)

twoway ///
    (scatter mentions weeks_to_nearest_tuesday, msymbol(circle) mcolor(black%40)) ///
    (scatter pred weeks_to_nearest_tuesday, msymbol(circle) mcolor(red%40)) ///
    (lfit mentions weeks_to_nearest_tuesday if weeks_to_nearest_tuesday <= 0, lcolor(black)) ///
    (lfit mentions weeks_to_nearest_tuesday if weeks_to_nearest_tuesday > 0, lcolor(black)) ///
    (lfit pred weeks_to_nearest_tuesday if weeks_to_nearest_tuesday <= 0, lcolor(red)) ///
    (lfit pred weeks_to_nearest_tuesday if weeks_to_nearest_tuesday > 0, lcolor(red)) ///
    , ///
    xline(0, lcolor(black)) ///
    title("All Topics") ///
    xtitle("Weeks to Nearest Tuesday in Nov 2-8") ///
    ytitle("% of Sermons that Mention Any Topic") ///
    legend(order(1 "Actual" 2 "Predicted"))

graph export "output/regression/pattern_matching_in_window/figs/all_topics_regression_plot.png", replace

restore


local topics -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15

foreach topic of local topics {
    preserve

    gen mentions = regexm(mentioned_topics, "(?<!-)(\[`topic'\]|, `topic'|`topic',)")

    * OLS regression
    eststo: regress mentions in_window_dummy election_year_dummy interaction, robust
    estadd ysumm

    predict pred, xb

    collapse (mean) mentions pred, by(weeks_to_nearest_tuesday)

    if `topic' == -1 {
        local topic_label `topic_label_m1'
        local plot_title "Outlier Topic: `topic_label'"
    }
    else {
        local topic_label `topic_label_`topic''
        local plot_title "Topic `topic': `topic_label'"
    }

    twoway ///
    (scatter mentions weeks_to_nearest_tuesday, msymbol(circle) mcolor(black%40)) ///
    (scatter pred weeks_to_nearest_tuesday, msymbol(circle) mcolor(red%40)) ///
    (lfit mentions weeks_to_nearest_tuesday if weeks_to_nearest_tuesday <= 0, lcolor(black)) ///
    (lfit mentions weeks_to_nearest_tuesday if weeks_to_nearest_tuesday > 0, lcolor(black)) ///
    (lfit pred weeks_to_nearest_tuesday if weeks_to_nearest_tuesday <= 0, lcolor(red)) ///
    (lfit pred weeks_to_nearest_tuesday if weeks_to_nearest_tuesday > 0, lcolor(red)) ///
    , ///
    xline(0, lcolor(black)) ///
    title(`plot_title') ///
    xtitle("Weeks to Nearest Tuesday in Nov 2-8") ///
    ytitle("% of Sermons that Mention Topic") ///
    legend(order(1 "Actual" 2 "Predicted"))

    graph export "output/regression/pattern_matching_in_window/figs/topic_`topic'_regression_plot.png", replace

    restore
}

esttab using "output/regression/pattern_matching_in_window/coefficients_by_topic.csv", replace csv se label nodepvar ///
    stats(ymean ysd r2_a N, labels ("Mean of Dep. Var." "Std. Dev. of Dep. Var." "Adj. R-squared" "Observations") fmt(4 4 4 0)) ///
    star(* 0.1 ** 0.05 *** 0.01)


* --- pre-Tuesday dummy pattern matching docs --- *

eststo clear

import delimited "intermediate/regression/pattern_matching_pre_tuesday/labels.csv", clear ///
    varnames(1) ///
    stringcols(_all)
destring topic, replace

levelsof topic, local(topic_levels)
foreach t of local topic_levels {
    quietly levelsof label if topic == `t', local(lbl)
    local name = subinstr("`t'", "-", "m", .)
    local topic_label_`name' "`lbl'"
}

import delimited "intermediate/regression/pattern_matching_pre_tuesday/data.csv", clear ///
    varnames(1) ///
    stringcols(_all) ///
    bindquote(strict)
destring weeks_to_nearest_tuesday, replace
destring weeks_to_nearest_election, replace


gen pre_tuesday_dummy = (weeks_to_nearest_tuesday >= -4 & weeks_to_nearest_tuesday <= 0)
gen election_year_dummy = (weeks_to_nearest_election >= -4 & weeks_to_nearest_election <= 4)
gen interaction = pre_tuesday_dummy * election_year_dummy


preserve

gen mentions = strtrim(mentioned_topics) != "[]"

* OLS regression
eststo: regress mentions pre_tuesday_dummy election_year_dummy interaction, robust
estadd ysumm

predict pred, xb

collapse (mean) mentions pred, by(weeks_to_nearest_tuesday)

twoway ///
    (scatter mentions weeks_to_nearest_tuesday, msymbol(circle) mcolor(black%40)) ///
    (scatter pred weeks_to_nearest_tuesday, msymbol(circle) mcolor(red%40)) ///
    (lfit mentions weeks_to_nearest_tuesday if weeks_to_nearest_tuesday <= 0, lcolor(black)) ///
    (lfit mentions weeks_to_nearest_tuesday if weeks_to_nearest_tuesday > 0, lcolor(black)) ///
    (lfit pred weeks_to_nearest_tuesday if weeks_to_nearest_tuesday <= 0, lcolor(red)) ///
    (lfit pred weeks_to_nearest_tuesday if weeks_to_nearest_tuesday > 0, lcolor(red)) ///
    , ///
    xline(0, lcolor(black)) ///
    title("All Topics") ///
    xtitle("Weeks to Nearest Tuesday in Nov 2-8") ///
    ytitle("% of Sermons that Mention Any Topic") ///
    legend(order(1 "Actual" 2 "Predicted"))

graph export "output/regression/pattern_matching_pre_tuesday/figs/all_topics_regression_plot.png", replace

restore


local topics -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15

foreach topic of local topics {
    preserve

    gen mentions = regexm(mentioned_topics, "(?<!-)(\[`topic'\]|, `topic'|`topic',)")

    * OLS regression
    eststo: regress mentions pre_tuesday_dummy election_year_dummy interaction, robust
    estadd ysumm

    predict pred, xb

    collapse (mean) mentions pred, by(weeks_to_nearest_tuesday)

    if `topic' == -1 {
        local topic_label `topic_label_m1'
        local plot_title "Outlier Topic: `topic_label'"
    }
    else {
        local topic_label `topic_label_`topic''
        local plot_title "Topic `topic': `topic_label'"
    }

    twoway ///
    (scatter mentions weeks_to_nearest_tuesday, msymbol(circle) mcolor(black%40)) ///
    (scatter pred weeks_to_nearest_tuesday, msymbol(circle) mcolor(red%40)) ///
    (lfit mentions weeks_to_nearest_tuesday if weeks_to_nearest_tuesday <= 0, lcolor(black)) ///
    (lfit mentions weeks_to_nearest_tuesday if weeks_to_nearest_tuesday > 0, lcolor(black)) ///
    (lfit pred weeks_to_nearest_tuesday if weeks_to_nearest_tuesday <= 0, lcolor(red)) ///
    (lfit pred weeks_to_nearest_tuesday if weeks_to_nearest_tuesday > 0, lcolor(red)) ///
    , ///
    xline(0, lcolor(black)) ///
    title(`plot_title') ///
    xtitle("Weeks to Nearest Tuesday in Nov 2-8") ///
    ytitle("% of Sermons that Mention Topic") ///
    legend(order(1 "Actual" 2 "Predicted"))

    graph export "output/regression/pattern_matching_pre_tuesday/figs/topic_`topic'_regression_plot.png", replace

    restore
}

esttab using "output/regression/pattern_matching_pre_tuesday/coefficients_by_topic.csv", replace csv se label nodepvar ///
    stats(ymean ysd r2_a N, labels ("Mean of Dep. Var." "Std. Dev. of Dep. Var." "Adj. R-squared" "Observations") fmt(4 4 4 0)) ///
    star(* 0.1 ** 0.05 *** 0.01)


* --- pre-Tuesday dummy gpt docs --- *

eststo clear

import delimited "intermediate/regression/gpt_pre_tuesday/labels.csv", clear ///
    varnames(1) ///
    stringcols(_all)
destring topic, replace

levelsof topic, local(topic_levels)
foreach t of local topic_levels {
    quietly levelsof label if topic == `t', local(lbl)
    local name = subinstr("`t'", "-", "m", .)
    local topic_label_`name' "`lbl'"
}

import delimited "intermediate/regression/gpt_pre_tuesday/data.csv", clear ///
    varnames(1) ///
    stringcols(_all) ///
    bindquote(strict)
destring weeks_to_nearest_tuesday, replace
destring weeks_to_nearest_election, replace


gen pre_tuesday_dummy = (weeks_to_nearest_tuesday >= -4 & weeks_to_nearest_tuesday <= 0)
gen election_year_dummy = (weeks_to_nearest_election >= -4 & weeks_to_nearest_election <= 4)
gen interaction = pre_tuesday_dummy * election_year_dummy


preserve

gen mentions = strtrim(mentioned_topics) != "[]"

* OLS regression
eststo: regress mentions pre_tuesday_dummy election_year_dummy interaction, robust
estadd ysumm

predict pred, xb

collapse (mean) mentions pred, by(weeks_to_nearest_tuesday)

twoway ///
    (scatter mentions weeks_to_nearest_tuesday, msymbol(circle) mcolor(black%40)) ///
    (scatter pred weeks_to_nearest_tuesday, msymbol(circle) mcolor(red%40)) ///
    (lfit mentions weeks_to_nearest_tuesday if weeks_to_nearest_tuesday <= 0, lcolor(black)) ///
    (lfit mentions weeks_to_nearest_tuesday if weeks_to_nearest_tuesday > 0, lcolor(black)) ///
    (lfit pred weeks_to_nearest_tuesday if weeks_to_nearest_tuesday <= 0, lcolor(red)) ///
    (lfit pred weeks_to_nearest_tuesday if weeks_to_nearest_tuesday > 0, lcolor(red)) ///
    , ///
    xline(0, lcolor(black)) ///
    title("All Topics") ///
    xtitle("Weeks to Nearest Tuesday in Nov 2-8") ///
    ytitle("% of Sermons that Mention Any Topic") ///
    legend(order(1 "Actual" 2 "Predicted"))

graph export "output/regression/gpt_pre_tuesday/figs/all_topics_regression_plot.png", replace

restore


local topics -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15

foreach topic of local topics {
    preserve

    gen mentions = regexm(mentioned_topics, "(?<!-)(\[`topic'\]|, `topic'|`topic',)")

    * OLS regression
    eststo: regress mentions pre_tuesday_dummy election_year_dummy interaction, robust
    estadd ysumm

    predict pred, xb

    collapse (mean) mentions pred, by(weeks_to_nearest_tuesday)

    if `topic' == -1 {
        local topic_label `topic_label_m1'
        local plot_title "Outlier Topic: `topic_label'"
    }
    else {
        local topic_label `topic_label_`topic''
        local plot_title "Topic `topic': `topic_label'"
    }

    twoway ///
    (scatter mentions weeks_to_nearest_tuesday, msymbol(circle) mcolor(black%40)) ///
    (scatter pred weeks_to_nearest_tuesday, msymbol(circle) mcolor(red%40)) ///
    (lfit mentions weeks_to_nearest_tuesday if weeks_to_nearest_tuesday <= 0, lcolor(black)) ///
    (lfit mentions weeks_to_nearest_tuesday if weeks_to_nearest_tuesday > 0, lcolor(black)) ///
    (lfit pred weeks_to_nearest_tuesday if weeks_to_nearest_tuesday <= 0, lcolor(red)) ///
    (lfit pred weeks_to_nearest_tuesday if weeks_to_nearest_tuesday > 0, lcolor(red)) ///
    , ///
    xline(0, lcolor(black)) ///
    title(`plot_title') ///
    xtitle("Weeks to Nearest Tuesday in Nov 2-8") ///
    ytitle("% of Sermons that Mention Topic") ///
    legend(order(1 "Actual" 2 "Predicted"))

    graph export "output/regression/gpt_pre_tuesday/figs/topic_`topic'_regression_plot.png", replace

    restore
}

esttab using "output/regression/gpt_pre_tuesday/coefficients_by_topic.csv", replace csv se label nodepvar ///
    stats(ymean ysd r2_a N, labels ("Mean of Dep. Var." "Std. Dev. of Dep. Var." "Adj. R-squared" "Observations") fmt(4 4 4 0)) ///
    star(* 0.1 ** 0.05 *** 0.01)
