* installation requirements: rdrobust
import delimited "output/sermons.csv", bindquote(strict) varnames(1) encoding(UTF-8) clear

* --- election mentions plots --- *

tempfile original
save `original'
collapse (mean) election_mentions, by(months_to_nearest_election)

reg election_mentions months_to_nearest_election if inrange(months_to_nearest_election, -12, 0)
predict fit_left if inrange(months_to_nearest_election, -12, 0)
reg election_mentions months_to_nearest_election if inrange(months_to_nearest_election, 1, 12)
predict fit_right if inrange(months_to_nearest_election, 1, 12)

twoway ///
	(scatter election_mentions months_to_nearest_election if inrange(months_to_nearest_election, -12, 12), msymbol(o) mcolor(gs8)) ///
	(line fit_left months_to_nearest_election if inrange(months_to_nearest_election, -12, 0), lcolor(black)) ///
	(line fit_right months_to_nearest_election if inrange(months_to_nearest_election, 1, 12), lcolor(black)) ///
	, ///
	title("RDD Plot - All Election years") ///
	xtitle("Months to Nearest Election") ///
	ytitle("Average Election Mentions") ///
	ylabel(0(0.5)4) ///
	yscale(range(0 4)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/election_mentions/rdd_plot_months_election_years.png", replace


use `original', clear
collapse (mean) election_mentions, by(weeks_to_nearest_election)

reg election_mentions weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 0)
predict fit_left if inrange(weeks_to_nearest_election, -4, 0)
reg election_mentions weeks_to_nearest_election if inrange(weeks_to_nearest_election, 1, 4)
predict fit_right if inrange(weeks_to_nearest_election, 1, 4)

twoway ///
	(scatter election_mentions weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 4), msymbol(o) mcolor(gs8)) ///
	(line fit_left weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 0), lcolor(black)) ///
	(line fit_right weeks_to_nearest_election if inrange(weeks_to_nearest_election, 1, 4), lcolor(black)) ///
	, ///
	title("RDD Plot - All Election years") ///
	xtitle("Weeks to Nearest Election") ///
	ytitle("Average Election Mentions") ///
	ylabel(0(0.5)4) ///
	yscale(range(0 4)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/election_mentions/rdd_plot_weeks_election_years.png", replace


use `original', clear
collapse (mean) election_mentions if !inrange(weeks_to_nearest_election, -4, 4), by(weeks_to_nearest_tuesday)

reg election_mentions weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -4, 0)
predict fit_left if inrange(weeks_to_nearest_tuesday, -4, 0)
reg election_mentions weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, 1, 4)
predict fit_right if inrange(weeks_to_nearest_tuesday, 1, 4)

twoway ///
	(scatter election_mentions weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -4, 4), msymbol(o) mcolor(gs8)) ///
	(line fit_left weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -4, 0), lcolor(black)) ///
	(line fit_right weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, 1, 4), lcolor(black)) ///
	, ///
	title("RDD Plot - All Non-Election years") ///
	xtitle("Weeks to Nearest Election Tuesday") ///
	ytitle("Average Election Mentions") ///
	ylabel(0(0.5)4) ///
	yscale(range(0 4)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/election_mentions/rdd_plot_weeks_non_election_years.png", replace


use `original', clear
collapse (mean) election_mentions, by(weeks_to_2004_election)

reg election_mentions weeks_to_2004_election if inrange(weeks_to_2004_election, -4, 0)
predict fit_left if inrange(weeks_to_2004_election, -4, 0)
reg election_mentions weeks_to_2004_election if inrange(weeks_to_2004_election, 1, 4)
predict fit_right if inrange(weeks_to_2004_election, 1, 4)

twoway ///
	(scatter election_mentions weeks_to_2004_election if inrange(weeks_to_2004_election, -4, 4), msymbol(o) mcolor(gs8)) ///
	(line fit_left weeks_to_2004_election if inrange(weeks_to_2004_election, -4, 0), lcolor(black)) ///
	(line fit_right weeks_to_2004_election if inrange(weeks_to_2004_election, 1, 4), lcolor(black)) ///
	, ///
	title("RDD Plot - 2004 Election") ///
	xtitle("Weeks to Election") ///
	ytitle("Average Election Mentions") ///
	ylabel(0(0.5)4) ///
	yscale(range(0 4)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/election_mentions/rdd_plot_weeks_2004_election.png", replace


use `original', clear
collapse (mean) election_mentions, by(weeks_to_2008_election)

reg election_mentions weeks_to_2008_election if inrange(weeks_to_2008_election, -4, 0)
predict fit_left if inrange(weeks_to_2008_election, -4, 0)
reg election_mentions weeks_to_2008_election if inrange(weeks_to_2008_election, 1, 4)
predict fit_right if inrange(weeks_to_2008_election, 1, 4)

twoway ///
	(scatter election_mentions weeks_to_2008_election if inrange(weeks_to_2008_election, -4, 4), msymbol(o) mcolor(gs8)) ///
	(line fit_left weeks_to_2008_election if inrange(weeks_to_2008_election, -4, 0), lcolor(black)) ///
	(line fit_right weeks_to_2008_election if inrange(weeks_to_2008_election, 1, 4), lcolor(black)) ///
	, ///
	title("RDD Plot - 2008 Election") ///
	xtitle("Weeks to Election") ///
	ytitle("Average Election Mentions") ///
	ylabel(0(0.5)4) ///
	yscale(range(0 4)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/election_mentions/rdd_plot_weeks_2008_election.png", replace


use `original', clear
collapse (mean) election_mentions, by(weeks_to_2012_election)

reg election_mentions weeks_to_2012_election if inrange(weeks_to_2012_election, -4, 0)
predict fit_left if inrange(weeks_to_2012_election, -4, 0)
reg election_mentions weeks_to_2012_election if inrange(weeks_to_2012_election, 1, 4)
predict fit_right if inrange(weeks_to_2012_election, 1, 4)

twoway ///
	(scatter election_mentions weeks_to_2012_election if inrange(weeks_to_2012_election, -4, 4), msymbol(o) mcolor(gs8)) ///
	(line fit_left weeks_to_2012_election if inrange(weeks_to_2012_election, -4, 0), lcolor(black)) ///
	(line fit_right weeks_to_2012_election if inrange(weeks_to_2012_election, 1, 4), lcolor(black)) ///
	, ///
	title("RDD Plot - 2012 Election") ///
	xtitle("Weeks to Election") ///
	ytitle("Average Election Mentions") ///
	ylabel(0(0.5)4) ///
	yscale(range(0 4)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/election_mentions/rdd_plot_weeks_2012_election.png", replace


use `original', clear
collapse (mean) election_mentions, by(weeks_to_2016_election)

reg election_mentions weeks_to_2016_election if inrange(weeks_to_2016_election, -4, 0)
predict fit_left if inrange(weeks_to_2016_election, -4, 0)
reg election_mentions weeks_to_2016_election if inrange(weeks_to_2016_election, 1, 4)
predict fit_right if inrange(weeks_to_2016_election, 1, 4)

twoway ///
	(scatter election_mentions weeks_to_2016_election if inrange(weeks_to_2016_election, -4, 4), msymbol(o) mcolor(gs8)) ///
	(line fit_left weeks_to_2016_election if inrange(weeks_to_2016_election, -4, 0), lcolor(black)) ///
	(line fit_right weeks_to_2016_election if inrange(weeks_to_2016_election, 1, 4), lcolor(black)) ///
	, ///
	title("RDD Plot - 2016 Election") ///
	xtitle("Weeks to Election") ///
	ytitle("Average Election Mentions") ///
	ylabel(0(0.5)4) ///
	yscale(range(0 4)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/election_mentions/rdd_plot_weeks_2016_election.png", replace


use `original', clear
collapse (mean) election_mentions, by(weeks_to_2020_election)

reg election_mentions weeks_to_2020_election if inrange(weeks_to_2020_election, -4, 0)
predict fit_left if inrange(weeks_to_2020_election, -4, 0)
reg election_mentions weeks_to_2020_election if inrange(weeks_to_2020_election, 1, 4)
predict fit_right if inrange(weeks_to_2020_election, 1, 4)

twoway ///
	(scatter election_mentions weeks_to_2020_election if inrange(weeks_to_2020_election, -4, 4), msymbol(o) mcolor(gs8)) ///
	(line fit_left weeks_to_2020_election if inrange(weeks_to_2020_election, -4, 0), lcolor(black)) ///
	(line fit_right weeks_to_2020_election if inrange(weeks_to_2020_election, 1, 4), lcolor(black)) ///
	, ///
	title("RDD Plot - 2020 Election") ///
	xtitle("Weeks to Election") ///
	ytitle("Average Election Mentions") ///
	ylabel(0(0.5)4) ///
	yscale(range(0 4)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/election_mentions/rdd_plot_weeks_2020_election.png", replace


use `original', clear
gen month = date(contribution_monthly, "YMD")
format month %td

collapse (sum) election_mentions, by(month)

twoway (line election_mentions month, lcolor(black) lwidth(medium)) ///
	, ///
	xline(`=date("2004-11-01","YMD")' ///
			`=date("2008-11-01","YMD")' ///
			`=date("2012-11-01","YMD")' ///
			`=date("2016-11-01","YMD")' ///
			`=date("2020-11-01","YMD")', ///
			lcolor(black) lpattern(dash) lwidth(thin)) ///
	title("Election Mentions in Religious Sermons Over Time") ///
	xtitle("Month") /// 
	ytitle("Mentions") ///
	xlabel(, angle(45)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/election_mentions/word_count.png", replace


use `original', clear
gen in_window_dummy = (weeks_to_nearest_tuesday >= -4 & weeks_to_nearest_tuesday <= 4)
gen election_year_dummy = (weeks_to_nearest_election >= -8 & weeks_to_nearest_election <= 8)
gen interaction = in_window_dummy * election_year_dummy

eststo: regress election_mentions in_window_dummy election_year_dummy interaction if inrange(weeks_to_nearest_tuesday, -8, 8), robust
estadd ysumm

predict pred, xb

collapse (mean) election_mentions pred, by(weeks_to_nearest_tuesday)

twoway ///
    (scatter election_mentions weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -8, 8), msymbol(circle) mcolor(black%40)) ///
    (scatter pred weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -8, 8), msymbol(circle) mcolor(red%40)) ///
    (lfit election_mentions weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -8, 0), lcolor(black)) ///
    (lfit election_mentions weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, 1, 8), lcolor(black)) ///
    (lfit pred weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -8, 0), lcolor(red)) ///
    (lfit pred weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, 1, 8), lcolor(red)) ///
    , ///
    xline(0, lcolor(black)) ///
    title("All Topics") ///
    xtitle("Weeks to Nearest Tuesday in Nov 2-8") ///
    ytitle("Average Election Mentions") ///
    legend(order(1 "Actual" 2 "Predicted"))

graph export "output/figs/election_mentions/DiD_regression.png", replace



* --- election word count plots --- *

use `original', clear
collapse (mean) election_word_count, by(months_to_nearest_election)

reg election_word_count months_to_nearest_election if inrange(months_to_nearest_election, -12, 0)
predict fit_left if inrange(months_to_nearest_election, -12, 0)
reg election_word_count months_to_nearest_election if inrange(months_to_nearest_election, 1, 12)
predict fit_right if inrange(months_to_nearest_election, 1, 12)

twoway ///
	(scatter election_word_count months_to_nearest_election if inrange(months_to_nearest_election, -12, 12), msymbol(o) mcolor(gs8)) ///
	(line fit_left months_to_nearest_election if inrange(months_to_nearest_election, -12, 0), lcolor(black)) ///
	(line fit_right months_to_nearest_election if inrange(months_to_nearest_election, 1, 12), lcolor(black)) ///
	, ///
	title("RDD Plot - All Election years") ///
	xtitle("Months to Nearest Election") ///
	ytitle("Average Election Word Count") ///
	ylabel(0(0.25)2) ///
	yscale(range(0 2)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/election_word_count/rdd_plot_months_election_years.png", replace


use `original', clear
collapse (mean) election_word_count, by(weeks_to_nearest_election)

reg election_word_count weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 0)
predict fit_left if inrange(weeks_to_nearest_election, -4, 0)
reg election_word_count weeks_to_nearest_election if inrange(weeks_to_nearest_election, 1, 4)
predict fit_right if inrange(weeks_to_nearest_election, 1, 4)

twoway ///
	(scatter election_word_count weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 4), msymbol(o) mcolor(gs8)) ///
	(line fit_left weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 0), lcolor(black)) ///
	(line fit_right weeks_to_nearest_election if inrange(weeks_to_nearest_election, 1, 4), lcolor(black)) ///
	, ///
	title("RDD Plot - All Election years") ///
	xtitle("Weeks to Nearest Election") ///
	ytitle("Average Election Word Count") ///
	ylabel(0(0.25)2) ///
	yscale(range(0 2)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/election_word_count/rdd_plot_weeks_election_years.png", replace


use `original', clear
collapse (mean) election_word_count if !inrange(weeks_to_nearest_election, -4, 4), by(weeks_to_nearest_tuesday)

reg election_word_count weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -4, 0)
predict fit_left if inrange(weeks_to_nearest_tuesday, -4, 0)
reg election_word_count weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, 1, 4)
predict fit_right if inrange(weeks_to_nearest_tuesday, 1, 4)

twoway ///
	(scatter election_word_count weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -4, 4), msymbol(o) mcolor(gs8)) ///
	(line fit_left weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -4, 0), lcolor(black)) ///
	(line fit_right weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, 1, 4), lcolor(black)) ///
	, ///
	title("RDD Plot - All Non-Election years") ///
	xtitle("Weeks to Nearest Election Tuesday") ///
	ytitle("Average Election Word Count") ///
	ylabel(0(0.25)2) ///
	yscale(range(0 2)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/election_word_count/rdd_plot_weeks_non_election_years.png", replace



* --- candidate mentions plots --- *

use `original', clear
collapse (mean) candidate_mentions, by(months_to_nearest_election)

reg candidate_mentions months_to_nearest_election if inrange(months_to_nearest_election, -12, 0)
predict fit_left if inrange(months_to_nearest_election, -12, 0)
reg candidate_mentions months_to_nearest_election if inrange(months_to_nearest_election, 1, 12)
predict fit_right if inrange(months_to_nearest_election, 1, 12)

twoway ///
	(scatter candidate_mentions months_to_nearest_election if inrange(months_to_nearest_election, -12, 12), msymbol(o) mcolor(gs8)) ///
	(line fit_left months_to_nearest_election if inrange(months_to_nearest_election, -12, 0), lcolor(black)) ///
	(line fit_right months_to_nearest_election if inrange(months_to_nearest_election, 1, 12), lcolor(black)) ///
	, ///
	title("RDD Plot - All Election years") ///
	xtitle("Months to Nearest Election") ///
	ytitle("Average Candidate Mentions") ///
	ylabel(0(0.025)0.2) ///
	yscale(range(0 0.2)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/candidate_mentions/rdd_plot_months_election_years.png", replace


use `original', clear
collapse (mean) candidate_mentions, by(weeks_to_nearest_election)

reg candidate_mentions weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 0)
predict fit_left if inrange(weeks_to_nearest_election, -4, 0)
reg candidate_mentions weeks_to_nearest_election if inrange(weeks_to_nearest_election, 1, 4)
predict fit_right if inrange(weeks_to_nearest_election, 1, 4)

twoway ///
	(scatter candidate_mentions weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 4), msymbol(o) mcolor(gs8)) ///
	(line fit_left weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 0), lcolor(black)) ///
	(line fit_right weeks_to_nearest_election if inrange(weeks_to_nearest_election, 1, 4), lcolor(black)) ///
	, ///
	title("RDD Plot - All Election years") ///
	xtitle("Weeks to Nearest Election") ///
	ytitle("Average Candidate Mentions") ///
	ylabel(0(0.025)0.2) ///
	yscale(range(0 0.2)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/candidate_mentions/rdd_plot_weeks_election_years.png", replace


use `original', clear
collapse (mean) candidate_mentions if !inrange(weeks_to_nearest_election, -4, 4), by(weeks_to_nearest_tuesday)

reg candidate_mentions weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -4, 0)
predict fit_left if inrange(weeks_to_nearest_tuesday, -4, 0)
reg candidate_mentions weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, 1, 4)
predict fit_right if inrange(weeks_to_nearest_tuesday, 1, 4)

twoway ///
	(scatter candidate_mentions weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -4, 4), msymbol(o) mcolor(gs8)) ///
	(line fit_left weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -4, 0), lcolor(black)) ///
	(line fit_right weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, 1, 4), lcolor(black)) ///
	, ///
	title("RDD Plot - All Non-Election years") ///
	xtitle("Weeks to Nearest Election Tuesday") ///
	ytitle("Average Candidate Mentions") ///
	ylabel(0(0.025)0.2) ///
	yscale(range(0 0.2)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/candidate_mentions/rdd_plot_weeks_non_election_years.png", replace



* --- government word count plots --- *

use `original', clear
collapse (mean) government_word_count, by(months_to_nearest_election)

reg government_word_count months_to_nearest_election if inrange(months_to_nearest_election, -12, 0)
predict fit_left if inrange(months_to_nearest_election, -12, 0)
reg government_word_count months_to_nearest_election if inrange(months_to_nearest_election, 1, 12)
predict fit_right if inrange(months_to_nearest_election, 1, 12)

twoway ///
	(scatter government_word_count months_to_nearest_election if inrange(months_to_nearest_election, -12, 12), msymbol(o) mcolor(gs8)) ///
	(line fit_left months_to_nearest_election if inrange(months_to_nearest_election, -12, 0), lcolor(black)) ///
	(line fit_right months_to_nearest_election if inrange(months_to_nearest_election, 1, 12), lcolor(black)) ///
	, ///
	title("RDD Plot - All Election years") ///
	xtitle("Months to Nearest Election") ///
	ytitle("Average Government Word Count") ///
	ylabel(0(0.5)4) ///
	yscale(range(0 4)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/government_word_count/rdd_plot_months_election_years.png", replace


use `original', clear
collapse (mean) government_word_count, by(weeks_to_nearest_election)

reg government_word_count weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 0)
predict fit_left if inrange(weeks_to_nearest_election, -4, 0)
reg government_word_count weeks_to_nearest_election if inrange(weeks_to_nearest_election, 1, 4)
predict fit_right if inrange(weeks_to_nearest_election, 1, 4)

twoway ///
	(scatter government_word_count weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 4), msymbol(o) mcolor(gs8)) ///
	(line fit_left weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 0), lcolor(black)) ///
	(line fit_right weeks_to_nearest_election if inrange(weeks_to_nearest_election, 1, 4), lcolor(black)) ///
	, ///
	title("RDD Plot - All Election years") ///
	xtitle("Weeks to Nearest Election") ///
	ytitle("Average Government Word Count") ///
	ylabel(0(0.5)4) ///
	yscale(range(0 4)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/government_word_count/rdd_plot_weeks_election_years.png", replace


use `original', clear
collapse (mean) government_word_count if !inrange(weeks_to_nearest_election, -4, 4), by(weeks_to_nearest_tuesday)

reg government_word_count weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -4, 0)
predict fit_left if inrange(weeks_to_nearest_tuesday, -4, 0)
reg government_word_count weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, 1, 4)
predict fit_right if inrange(weeks_to_nearest_tuesday, 1, 4)

twoway ///
	(scatter government_word_count weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -4, 4), msymbol(o) mcolor(gs8)) ///
	(line fit_left weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -4, 0), lcolor(black)) ///
	(line fit_right weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, 1, 4), lcolor(black)) ///
	, ///
	title("RDD Plot - All Non-Election years") ///
	xtitle("Weeks to Nearest Election Tuesday") ///
	ytitle("Average Government Word Count") ///
	ylabel(0(0.5)4) ///
	yscale(range(0 4)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/government_word_count/rdd_plot_weeks_non_election_years.png", replace



* --- general plots --- *

use `original', clear
contract months_to_nearest_election if inrange(months_to_nearest_election, -12, 12)
rename _freq sermon_count

reg sermon_count months_to_nearest_election if inrange(months_to_nearest_election, -12, 0)
predict fit_left if inrange(months_to_nearest_election, -12, 0)
reg sermon_count months_to_nearest_election if inrange(months_to_nearest_election, 1, 12)
predict fit_right if inrange(months_to_nearest_election, 1, 12)

twoway ///
	(scatter sermon_count months_to_nearest_election if inrange(months_to_nearest_election, -12, 12), msymbol(o) mcolor(gs8)) ///
	(line fit_left months_to_nearest_election if inrange(months_to_nearest_election, -12, 0), lcolor(black)) ///
	(line fit_right months_to_nearest_election if inrange(months_to_nearest_election, 1, 12), lcolor(black)) ///
	, ///
	title("RDD Plot - All Election years") ///
	xtitle("Months to Nearest Election") ///
	ytitle("Sermon Count") ///
	ylabel(0(1000)5000) ///
	yscale(range(0 5000)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/sermon_count/rdd_plot_months_election_years.png", replace


use `original', clear
contract weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 4)
rename _freq sermon_count

reg sermon_count weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 0)
predict fit_left if inrange(weeks_to_nearest_election, -4, 0)
reg sermon_count weeks_to_nearest_election if inrange(weeks_to_nearest_election, 1, 4)
predict fit_right if inrange(weeks_to_nearest_election, 1, 4)

twoway ///
	(scatter sermon_count weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 4), msymbol(o) mcolor(gs8)) ///
	(line fit_left weeks_to_nearest_election if inrange(weeks_to_nearest_election, -4, 0), lcolor(black)) ///
	(line fit_right weeks_to_nearest_election if inrange(weeks_to_nearest_election, 1, 4), lcolor(black)) ///
	, ///
	title("RDD Plot - All Election years") ///
	xtitle("Weeks to Nearest Election") ///
	ytitle("Sermon Count") ///
	ylabel(0(500)2500) ///
	yscale(range(0 2500)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/sermon_count/rdd_plot_weeks_election_years.png", replace


use `original', clear
contract weeks_to_nearest_tuesday if !inrange(weeks_to_nearest_election, -4, 4)
rename _freq sermon_count

reg sermon_count weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -4, 0)
predict fit_left if inrange(weeks_to_nearest_tuesday, -4, 0)
reg sermon_count weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, 1, 4)
predict fit_right if inrange(weeks_to_nearest_tuesday, 1, 4)

twoway ///
	(scatter sermon_count weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -4, 4), msymbol(o) mcolor(gs8)) ///
	(line fit_left weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, -4, 0), lcolor(black)) ///
	(line fit_right weeks_to_nearest_tuesday if inrange(weeks_to_nearest_tuesday, 1, 4), lcolor(black)) ///
	, ///
	title("RDD Plot - All Non-Election years") ///
	xtitle("Weeks to Nearest Election Tuesday") ///
	ytitle("Sermon Count") ///
	ylabel(0(500)2500) ///
	yscale(range(0 2500)) ///
	xline(0, lcolor(black)) ///
	legend(off) ///
	scheme(s2color)
graph export "output/figs/sermon_count/rdd_plot_weeks_non_election_years.png", replace




* --- pastor level controls --- *

use `original', clear

* experience variable
gen exp_bin = .
by contributor, sort: gen nvals = _n == 1

replace exp_bin = 10 if strpos(experience, "I have been preaching now for about 7 years.") | strpos(experience, "7 yrs. as senior minister @ Oak Hills Christian Church, Cincinnati.2006-2007") | strpos(experience, "Director of Crossroads School of Biblical Studies International 5 years, and pastor for 10") | strpos(experience, "Ministered form 1993 - 1997 in High Point, North Carolina at Peace Christian Church1997 - current at Wilkinson Church of Christ, Wilkinson Indiana") | strpos(experience, "Christian Camp Director since 1998.  I pastored in The Church of the Nazarene for 3 years prior to that.") | strpos(experience, "i was the interim pastor of friendship baptist church for 18 months.") | strpos(experience, "Became pastor of West Springfield Baptist in 2005") | strpos(experience, "3 years - Pastor/Co-pastor of inner-city chapel.1 year") | strpos(experience, "2 years serving as senior pastor here at Calvary Baptist Church.") | strpos(experience, "Preaching - 9 yearsPastoring - 5 years") | strpos(experience, "Nearly two years as senior pastor at current church.  Background in youth ministry.") | strpos(experience, "Started ministry at the age of 12. I am currently 17.") | strpos(experience, "I have been preaching for about eight years!") | strpos(experience, "God delivered me from years of drug abuse. I been on the streets,") | strpos(experience, "Youth Pastor -- West Tenth Street Baptst Church 6 MonthsSr. Pastor") | strpos(experience, "Christian for over 25 years, Bus Captain, Sunday School Teacher, Evangelist, College Staff,") | strpos(experience, "Grew up in the street's of Miami Fl. selling drugs") | strpos(experience, "{July 2003 - Present---Pastor---Bear Creek Baptist Church}") | strpos(experience, "I pastored my First Church in Kinston, NC for 10 years, 1983-1987.I") | strpos(experience, "Church Planter 19910-1998  New Directions Church in Wilsonville,ORSenior Pastor 2000-present Springwater Church in Gresham, OR") | strpos(experience, "Licensed to preach June 2001.") | strpos(experience, "Baring Baptist Church is my first church. As of January 2018, I've been pastoring here for 10 years.") | strpos(experience, "Double Spring Baptist, 1999-2003Willow Grove Baptist, 2003-2007Bethel Baptist, 2007-Present") | strpos(experience, "Founder and Senior Pastor of Grace Church Gulf Coast since it's inception in April 1998") | strpos(experience, "I have assisted in ministry in various churches through out my life but I have been the Lead Pastor at LCN for just over 2 years now.") | strpos(experience, "I have served at Globe Christian Church as their youth minister for close to a year.") | strpos(experience, "youth minister since 1998.") | strpos(experience, "1 Year as a Preaching Associate5 Years as Lead Minister") | strpos(experience, "1989-1992 I was a Youth Minister at Minier Christian Church, Minier IL.1992-1993") | strpos(experience, "Discipleship Pastor- 2009- 2012Lead Pastor 2012 to present") | strpos(experience, "I became an assoc. pastor in 1997, a full time pastor in 1999,") | strpos(experience, "Pastored for 10 years in Tennessee.Pastor in Salem, IL - September 2006 - June 2009Pastor in Craig, CO - June 2009 - September 2010") | strpos(experience, "I have been the lead pastor of the Stanford Church of the Nazarene since April 2012, interim executive pastor from August 2011-April 2012, and associate pastor from January 2010-August 2011.") | strpos(experience, "Caleb Anderson has been the Lead Pastor at Mariners Church in Huntington Beach since 2012,") | strpos(experience, "Have been in the ministry starting my 10th year. I have served Troy UMC in Troy, Iowa as a 1/10 time pastor. Spent the last two years serving Early UMC and Nemaha UMC as a parish Fulltime Local Licensed Pastor.") | strpos(experience, "Served St. John's Evangelical Lutheran Church of Gladwin, MI, & Good Shepherd Evangelical Lutheran Church of Beaverton, MI, from July, 2000 until August, 2004.Serving") | strpos(experience, "Pulpit supply 1yearFull time ministry 3 years") | strpos(experience, "June 2022 - Present") | strpos(experience, "Youth pastor Pastoring my first church as senior pastor") | strpos(experience, "Choe served his pastoral internship at Junction City First Baptist. He then served as Pastor of Grove Ridge Baptist Church from December 26th 2010 to December 2nd 2012.") | strpos(experience, "Pastoring since 2004") | strpos(experience, "I have been a youth pastor for the past four years, to include the last year of my life as a pastor.") | strpos(experience, "I began working with my home congregations youth group at the age of 16 and by 21 was working in a joint lay-ministry with another brother in Christ.")

replace exp_bin = 20 if strpos(experience, "I was a Youth Minister at First Christian Church in Sallisaw, OK") | strpos(experience, "Pastor for 15 years.") | strpos(experience, "20 years in ministry") | strpos(experience, "I was dean and teacher at a Bible institute in México for 12 years.") | strpos(experience, "After graduating from college, I spent ten years in secular employment.") | strpos(experience, "I have been pasturing a church as a full time pastor since 1992. Was ordained 2000.") | strpos(experience, "11 years solo pastor, small church") | strpos(experience, "1980 to 1985 On-the-job training in Community Outreach, Sermon preparation and delivery,") | strpos(experience, "I have been a youth pastor for 16 years") | strpos(experience, "I have been in some type of ministry since January of 1993.  I have traveled extensively throughout the United States") | strpos(experience, "This my first full time pastorate. I have been at Rosedale for 18 years") | strpos(experience, "Born in Haines City, Florida, this ambassador of Christ gave his life to the Lord in May 1988.") | strpos(experience, "Missionary to the Seminole Tribe of Florida since 1990.") | strpos(experience, "We have been Pastors for a year know and where Assisting Pastors for 10 years in Pico") | strpos(experience, "12 years as lead pastor at Above and Beyond Community Church") | strpos(experience, "Youth Minister, New Friendship Baptist Church, Dallas, TX Senior Pastor") | strpos(experience, "Ordination 1991. Traveled USA, Israel, Philippines") | strpos(experience, "7 Summer ministries during college/seminary years followed by 37 years of full time pastoral ministry.") | strpos(experience, "3 yrs as Worship Leader of Jesus Is the Word Church - Indianapolis, IN. 5 yrs as a Cell Church Leader at Jesus Is The Word Church. 5 yrs as a Lay-Speaker - various churches & denominations.") | strpos(experience, "Three Rivers Baptist Church (Bi-Vocational) 1986-87Ozark Baptist Church (Full Time) 1987-1990Trinity Baptist Church (Full Time) 1990-2002First Baptist Church (Full Time) 2002-present") | strpos(experience, "Youth Ministry- South Carolina and North CarolinaSenior Pastor - 3 yrs in South FloridaSenior Pastor - 3 yrs in North CarolinaSenior Pastor - 110 yrs at present church in Clemson, SC") | strpos(experience, "Served as a Southern Baptist Pastor for 20 years.Served present pastorate for") | strpos(experience, "12 years as a pastor/counselor") | strpos(experience, "Brady joined the staff of New Vision as Senior Pastor in August 2003.") | strpos(experience, "Fourteen years as a Lead Pastor as well as serving on staff at Saddleback Church. Now Lead Pastor of a church planted in 2011.") | strpos(experience, "15 years in Church ministry") | strpos(experience, "I have been preaching the word of God since October of 2000.") | strpos(experience, "Called to vocational ministry in my mid-30's, but was active in ministry through my church, the Gideons, and helping with campus ministry at SDSU.") | strpos(experience, "1991 - 19910 Associate Minister, Outer Banks Worship Center, Nags Head, NC19910 - 1997 Youth Pastor, Cornerstone Assembly of God, New Bern, NC1997 - Present Senior Pastor, Christian Life Center, Gibsonville, NC") | strpos(experience, "MINISTRY {Pastor, Senior}2003-NOW     Light On The Corner - Montrose CA 2001, 2002   Community Baptist Church - East Los Angeles CA                  (interim) 2000         White Stone Christian Fellowship - Temple City CA") | strpos(experience, "Pastor since 2008") | strpos(experience, "Served congregations in Detroit, Mi for three years.  Two Years in St. Louis as a missionary at Large for the Missiouri District of the LCMS.") | strpos(experience, "16+ years as minister") | strpos(experience, "I pastored for ten years, was an active duty Army chaplain for three years, and have been a federal prison chaplain ever since.") | strpos(experience, "Been Sr. Pastor of this last church we planted for 110 years.") | strpos(experience, "Started in the Ministry right after college at CornerStone in Las Vegas, as the multimedia director in charge of video, web multimedia stuff.") | strpos(experience, "I have 7 years of youth ministry experience (which means I have a little bit of experience in everything under the sun!), and 10 years pulpit experience. ") | strpos(experience, "18 years of Pastoral Experience") | strpos(experience, "Started first church in 1998; been breaking the Bread of Life ever since.") | strpos(experience, "Pastoring 15 years, former golf professional") | strpos(experience, "Pastor, First Church of the Nazarene, Nicholasville, KY (1992-19910)Christian Life Director, First Church of the Nazarene, Huntsville, AL (19910-1995)Claims Management,") | strpos(experience, "Pastored Bethlehem Baptist Church in Pinola, Ms (2 years)Pastored Pine Grove Baptist Church in Magee, MS") | strpos(experience, "5 years' teaching experience (English & math) in People's Republic of China2 years as Assistant Professor of Physics and Mathematics, King College, Bristol Tenn.7 years as communications systems engineer  with NEC and Motorola")

replace exp_bin = 30 if strpos(experience, "Called to the ministry at 17 I have served as a vocational minister since I was 19.") | strpos(experience, "Retired as U.Methodist Pastor after 26 years.  Serving New Church Plant since 2012") | strpos(experience, "Military 11.8 yearsMissionary in Wales, UK 10 yearsPastor 2.8 years") | strpos(experience, "Eleven years in church musicFive years in ministry to youth and childrenEight years in pastoral ministry") | strpos(experience, "August 1988-November 1991 St. Francis on the Hill") | strpos(experience, "Retired from ministry in 2017 to serve one year as a Christian Academy Principal and High School teacher.") | strpos(experience, "Billy Bob preached his first sermon at the age of 110") | strpos(experience, "Been in Ministry since Nov 1993, Been a Pastor; Youth Minister; Sunday School Teacher") | strpos(experience, "I was called to the ministry in 1983 and have served in 7 Churches over the past 25 years") | strpos(experience, "Served as United Methodist Pastor for 23 years serving congregations in Scranton, PA, Rogers, Greenbrier, Hoxie, Norphlet and Marked Tree, Arkansas.") | strpos(experience, "30 years in the ministry.") | strpos(experience, "Youth Pastor - Parkview Baptist Church - Metairie, LA 1995-96Pastor - Mt Vernon") | strpos(experience, "Pastor since 19810.") | strpos(experience, "Pastor here at Pathway since 1995.  Twelve years pastor at Emmanuel Free Will Baptist Church, Wabash, Indiana.") | strpos(experience, "2001- present -- Pastor,Cornerstone Baptist Church, Jefferson City, MO.1993-2001 -- SBC Representative,") | strpos(experience, "I began in ministry in 1988 with a small church youth group.  I have served churches in South Carolina, Kentucky, Texas, Indiana and North Carolina.") | strpos(experience, "25 + years of ministry") | strpos(experience, "I worked in the fields of youth and education ministry for five-plus years. In January 1990, I began serving as pastor of Brentwood Baptist Church in High Point, North Carolina.  I served at Fellowship Community Church, Mercer, PA from April 1993-October 2006, and came to Marietta at that point.") | strpos(experience, "My public ministry started as a teen (1982), licensed as a minister, and later ordained as an Elder by Presiding Bishop Charles E. Blake, Sr. I served as a National Evangelist [1996-1999]. I organized the Refinery Church [2005-present] where I'm Chairman/Senior Pastor") | strpos(experience, "Preaching and teaching God's Word faithfully for over 210 years now.") | strpos(experience, "Preaching & teaching for over 25 years.") | strpos(experience, "Former Police Officer in both the Ft. Worth, Texas and Dodge City, Kansas areas.  Began serving in lay ministry as a Sunday School teacher, deacon, and pulpit supply.  Took first pastorate in 1999.") | strpos(experience, "I've been in ministry for 29 years...") | strpos(experience, "20 years + as:Sunday School Teacher of all ages;Christian Education Director;Sunday School Superintendent;Minister of Christian Education.") | strpos(experience, "I have been in the gospel ministry for30 years. I preached my first sermon in February 1985. I recieved my license in Oct. 1985, and was ordained to the gospel minsitry in January 1992.") | strpos(experience, "15 years at South Peninsula Baptist10 years prior to that in various support staff positions.Author of "Cuppa Christ" Coffee Break Devotions for the busy Christian") | strpos(experience, "20 years Youth Ministry; 6 years Pastor") | strpos(experience, "Nineteen years full ministrySix years Army Officer") | strpos(experience, "As a pastor, author, coach, and teacher for 25 years, my goal has been to help people around the world breakout of spiritual ruts to live out God's purpose for their lives.-") | strpos(experience, "21 Years full time ministry") | strpos(experience, "21 Years full time ministry")

replace exp_bin = 100 if strpos(experience, "Thirty nine years of ministry.") | strpos(experience, "17 years student ministry12 years family ministry6 years senior pastor") | strpos(experience, "Returned-August 16,2020 Pastor, First Baptist Church, McAdoo, TXRetired- December 31, 2019Pastor-Shady Shores Baptist Church, Shady Shores,") | strpos(experience, "Following a couple years serving abroad (Europe and India), served for over 33 years as the Senior Pastor of the Westside Vineyard Church (1991-20210)") | strpos(experience, "Brent has been in the ministry for 20 years as a pastor & conference speaker.") | strpos(experience, "Been in ministry since 1986 when I started preaching at a small church while in college. I've worked with local churches and international ministries.") | strpos(experience, "Senior Pastor since 1987Chaplain Supervisor Pastoral Care UK King's Daughters Hospital") | strpos(experience, "I have been teaching the Bible since 1983.") | strpos(experience, "Church Planter in Midland, MI (1986-1989), Ellsworth, KS (1989-2001), and Oskaloosa, KS (2001-2005).  Pastor at Bethel Evangelical Free Church on Washington Island, WI (2005 - 2012).") | strpos(experience, "Called at 16 and run from God until 50.") | strpos(experience, "over 30 Years Pastoral experience") | strpos(experience, "Been in ministry since 1981")

replace exp_bin = 50 if strpos(experience, "Saved Eastside baptist church Copperas Cove texas 3rd Sund in Sept 1980.Licensed in 1983Ordained Oakalla Baptist Church") | strpos(experience, "30 + years as a Pastor") | strpos(experience, "Elder Arthur Lee Mason, over 30 years in the ministry.") | strpos(experience, "102 years in Ministry") | strpos(experience, "Preached my first sermon in 19710. Received my ministry license in 2006 and ordination in 20110. Faculty member") | strpos(experience, "7 Summer ministries during college/seminary years followed by 37 years of full time pastoral ministry.") | strpos(experience, "Four years in radio in Oklahoma, Texas and Tennessee, on-air,") | strpos(experience, "50 years experience, serving as Bible class teacher, Deacon, Youth Minister, Elder, Minster of Education, Ministerial Counselor, Teaching Minister and Hospice Chaplain.") | strpos(experience, "I became a Christian in 1975 at the age of 16 and started a puppet ministry. I worked with the youth until 2004 when I became a minister. Now I work with the adults as well as the youth.") | strpos(experience, "Served for 1 1/2 years as an Associate in Michigan; Have served as Sr. Pastor in my present location for 39 years.") | strpos(experience, "After 16 years at Carey Association and 31 years as a Pastor I have re-treaded in ministry to preaching and counseling.") | strpos(experience, "Pastor - 30 years, Organizational Executive - 11 years, Author 1010+ books, Ministry Monday webcast at Facebook page,") | strpos(experience, "My experience in religious studies began at an early age in the Roman Catholic faith over 103 years ago.") | strpos(experience, "I have  been preaching since 1982 and pastoring since 1996. I have traveled throughout the U.S. preaching the Gospel of Jesus Christ.")

replace exp_bin = 60 if strpos(experience, "Preaching more than 59 years.  Pastoring the same church for 37 years.") | strpos(experience, "32 years Pastor, Associate Pastor, Christian Education Director, Pastoral Coinselor/Clinician12 years counselor in Correctional setting8 years counselor in Mental Health setting") | strpos(experience, "Ordained in 1958, have served 3 Christian Churches and  10 Anglican Churches as pastor.Have taught classes and served as Dean at St. Alban's Center, a school that helps prepare men for ministry.") | strpos(experience, "Sixty years in pastoral ministry. Presently serving as the pastor of Community of Grace church in Vinton, Louisiana.") | strpos(experience, "Retired U.S. Marine (F/18 aircraft mechanic) as of 1996.Five years as pastor of Mayflower Hills Baptist Church in Roanoke, VA.  Senior Pastor of Staunton Baptist since Novermber 2002.")

save "output/sermons.dta", replace
