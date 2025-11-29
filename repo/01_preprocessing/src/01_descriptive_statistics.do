* installation requirements: asdoc, shp2dta, spmap
import delimited "input/extracted_data.csv", bindquote(strict) varnames(1) encoding(UTF-8) maxquotedrows(40) clear

* ===== CLEANING ===== *

* --- church address --- *

* drop if church address is missing or not in US
drop if strpos(churchaddress, "*Province/Other")
drop if missing(churchaddress)
drop if churchaddress == ","

* extract states without phone number and zip
* define state by last group of alphabetic characters in church address
gen state = ""
replace state = regexs(1) if regexm(churchaddress, "([A-Za-z]+)\s*\d*$")

* drop if state not in US
drop if state == "Norfolk"
drop if state == "Manitoba"

* extract state from zip or phone number
gen state_from_zip = substr(churchaddress, strrpos(churchaddress, ",") + 1, length(churchaddress))

* drop if state zip is missing or not in US
drop if missing(state_from_zip)
drop if strpos(state_from_zip, "New Brunswick") | strpos(state_from_zip, "Queensland") | strpos(state_from_zip, "Tamilnadu")
drop if strpos(state_from_zip, "tamilnadu") | strpos(state_from_zip, "yucatan") | strpos(state_from_zip, "Metro Manila")
drop if strpos(state_from_zip, "N/A") | strpos(state_from_zip, "Maharashtra") | strpos(state_from_zip, "chiquimulilla")
drop if strpos(state_from_zip, "Zamboanga") | strpos(state_from_zip, "Western") | strpos(state_from_zip, "WESTERN")
drop if strpos(state_from_zip, "Wellington") | strpos(state_from_zip, "Wc") | strpos(state_from_zip, "Wales")
drop if strpos(state_from_zip, "Waikato") | strpos(state_from_zip, "karnataka") | strpos(state_from_zip, "W10")
drop if strpos(state_from_zip, "Victoria") | strpos(state_from_zip, "Uttar")
drop if strpos(state_from_zip, "TW13") | strpos(state_from_zip, "Tamil") | strpos(state_from_zip, "Tarlac") | strpos(state_from_zip, "Telangana")
drop if strpos(state_from_zip, "TRINIDAD") | strpos(state_from_zip, "Sibiu") | strpos(state_from_zip, "Rivers") | strpos(state_from_zip, "Region") | strpos(state_from_zip, "QLD")
drop if strpos(state_from_zip, "Prince") | strpos(state_from_zip, "PRETORIA") | strpos(state_from_zip, "Punjab") | strpos(state_from_zip, "Oyo") | strpos(state_from_zip, "Otago")
drop if strpos(state_from_zip, "Ontario") | strpos(state_from_zip, "Ogun") | strpos(state_from_zip, "Northern") | strpos(state_from_zip, "Norfolk")
drop if strpos(state_from_zip, "Newfoundland") | strpos(state_from_zip, "Nairobi") | strpos(state_from_zip, "NSW") | strpos(state_from_zip, "NCR")
drop if strpos(state_from_zip, "Mpumalanga") | strpos(state_from_zip, "Midlothian") | strpos(state_from_zip, "Middlesex") | strpos(state_from_zip, "Marianao")
drop if strpos(state_from_zip, "Manitoba") | strpos(state_from_zip, "M4H1P4") | strpos(state_from_zip, "London") | strpos(state_from_zip, "Lincolnshire")
drop if strpos(state_from_zip, "Leinster") | strpos(state_from_zip, "Lancashire") | strpos(state_from_zip, "Lagos") | strpos(state_from_zip, "Kerala")
drop if strpos(state_from_zip, "Karnataka") | strpos(state_from_zip, "Karnatak") | strpos(state_from_zip, "Isabela") | strpos(state_from_zip, "Imo")
drop if strpos(state_from_zip, "Ilocos") | strpos(state_from_zip, "Hessen") | strpos(state_from_zip, "Hawkes") | strpos(state_from_zip, "Haryana")
drop if strpos(state_from_zip, "Grand") | strpos(state_from_zip, "Goa") | strpos(state_from_zip, "Federal") | strpos(state_from_zip, "FCT") | strpos(state_from_zip, "Enugu")
drop if strpos(state_from_zip, "England") | strpos(state_from_zip, "Edo") | strpos(state_from_zip, "Eastern") | strpos(state_from_zip, "District") | strpos(state_from_zip, "Copperbelt")
drop if strpos(state_from_zip, "Cebu") | strpos(state_from_zip, "Caltanissetta") | strpos(state_from_zip, "Bulacan") | strpos(state_from_zip, "British") | strpos(state_from_zip, "Benguet")
drop if strpos(state_from_zip, "Bay") | strpos(state_from_zip, "Bavaria") | strpos(state_from_zip, "Bataan") | strpos(state_from_zip, "BT750RL") | strpos(state_from_zip, "BT5")
drop if strpos(state_from_zip, "BH7") | strpos(state_from_zip, "Andhra") | strpos(state_from_zip, "Alimosho") | strpos(state_from_zip, "Abuja") | strpos(state_from_zip, "AB13")
drop if strpos(state_from_zip, "2750-515") | strpos(state_from_zip, "*Nariño") | strpos(state_from_zip, "*Attikh")
drop if strpos(state_from_zip, "SA")

* get first word of state_from_zip
gen state_new = word(state_from_zip, 1)
replace state_new = "" if real(state_new) != .

* replace phone number with state name
replace state_new = "New York" if state_new == "1-833-628-7227"
replace state_new = "Minnesota" if state_new == "952-221-3730"
replace state_new = "Tennessee" if state_new == "865-483-4357"
replace state_new = "Illinois" if state_new == "61726-1244"
replace state_new = "Iowa" if state_new == "515-262-7133"
replace state_new = "California" if state_new == "(323)"
replace state_new = "Tennessee" if state_new == "ext."

* drop if state is missing
drop if missing(state_new)

* manual cleaning
drop if strpos(state_new, "+91-8790791295")
drop if strpos(state_new, "512/676-6627")
drop if strpos(state_new, "205-642-9210")

* formatting and dropping if not in US
replace state_new = "Mississippi" if state_new == "MS"
replace state_new = "Oklahoma" if state_new == "OK"
replace state_new = "Arkansas" if state_new == "AR"
replace state_new = "West Virginia" if state_new == "West"
replace state_new = "Rhode Island" if state_new == "Rhode"
* 'south' contains South Carolina, South Dakota, and South Austrailia
replace state_new = "South Carolina" if strpos(state_from_zip, "South Carolina")
replace state_new = "South Dakota" if strpos(state_from_zip, "South Dakota")
drop if strpos(state_from_zip, "South Australia")
* 'north' contains North Carolina, North Dakota, and North Celebes
replace state_new = "North Carolina" if strpos(state_from_zip, "North Carolina")
replace state_new = "North Dakota" if strpos(state_from_zip, "North Dakota")
drop if strpos(state_from_zip, "North Celebes")
* 'new' contains New Hampshire, New Jersey, New Mexico, and New York
replace state_new = "New Hampshire" if strpos(state_from_zip, "New Hampshire")
replace state_new = "New Jersey" if strpos(state_from_zip, "New Jersey")
replace state_new = "New Mexico" if strpos(state_from_zip, "New Mexico")
replace state_new = "New York" if strpos(state_from_zip, "New York")
* 'Hampshire' contains New Hampshire and Hampshire, UK
drop if strpos(state_from_zip, "PO14 4LY") | strpos(state_from_zip, "PO3 6JH")

* rename state_new as state
drop state
rename state_new state

* --- denomination --- *

replace denomination = "Independent Bible" if denomination == "Independent/Bible"
replace denomination = "*Other" if denomination == "*other"
replace denomination = "*Other" if denomination == "Other"
replace denomination = "Assembly of God" if denomination == "Assembly Of God"
replace denomination = "Christian/Church of Christ" if denomination == "Christian/Church Of Christ" 
replace denomination = "Church of God" if denomination == "Church Of God"
replace denomination = "Disciples of Christ" if denomination == "Disciples Of Christ"
replace denomination = "Seventh-day Adventist" if denomination == "Seventh-Day Adventist"
drop if missing(denomination)

* ---- other missing observations ---- *

drop if missing(numberofratings)


* ===== DESCRIPTIVE STATISTICS ===== *

* --- coverage by state --- *

* absolute coverage
by state, sort: egen abs_state = count(sermontext)

* relative coverage
gen rel_state = abs_state/166308 * 100
// asdoc table state, c(mean abs_state)
// asdoc table state, c(mean rel_state)

* merge states to state population data [state | population of state]
merge m:1 state using "input/state_population.dta"
drop if _merge == 2

* adjusted relative coverage (relative coverage / percent of total population)
rename ResidentPopulation pop
gen pop_percentage = pop/281421906 * 100
gen adj_rel_state = rel_state / pop_percentage
// asdoc table state, c(mean adj_rel_state)

drop _merge

* --- coverage by year --- *

* extract year from contribution date
gen year = substr(contributiondate, -4, .)

* absolute coverage
by year, sort: egen abs_year = count(sermontext)

* relative coverage
gen rel_year = abs_year/166308 * 100

* extract and format dates
gen date = date(contributiondate, "DMY")
format date %d
// asdoc table year, c(mean abs_year)
// asdoc table year, c(mean rel_year)

destring year, replace

* merge data on presidential election candidates 
merge m:1 year using "input/presidents.dta"
drop _merge

* convert election dates to date variable
gen election04 = date(election2004, "DM20Y")
format election04 %d
gen time_to_election04 = date - election04 
drop election2004

gen election08 = date(election2008, "DM20Y")
format election08 %d
gen time_to_election08 = date - election08
drop election2008

gen election12 = date(election2012, "DM20Y")
format election12 %d
gen time_to_election12 = date - election12
drop election2012

gen election16 = date(election2016, "DM20Y")
format election16 %d
gen time_to_election16 = date - election16
drop election2016

gen election20 = date(election2020, "DM20Y")
format election20 %d
gen time_to_election20 = date - election20
drop election2020

gen election24 = date(election2024, "DM20Y")
format election24 %d
gen time_to_election24 = date - election24
drop election2024

* create monthly contributions variable
gen contribution_month = month(date)
gen contribution_year = year(date)
gen contribution_monthly = ym(contribution_year, contribution_month)
format contribution_monthly %tm

* --- coverage by denomination --- *

* absolute coverage
by denomination, sort: egen abs_denom = count(sermontext)

* relative coverage
gen rel_denom = abs_denom/166308 * 100
// asdoc table denomination, c(mean abs_denom)
// asdoc table denomination, c(mean rel_denom)

* --- coverage by religious family --- *

* merge denominations to religious family data [denomination, religious family of denomination]
merge m:1 denomination using "input/denomination_ARDA.dta"

* absolute coverage
by familyarda, sort: egen abs_family = count(sermontext)

* relative coverage
gen rel_family = abs_family/166308 * 100
// asdoc table familyarda, c(mean abs_family) dec(3)
// asdoc table familyarda, c(mean rel_family) dec(3)

* percent adherents by family
gen adh_percentage = adherents/145399350 * 100

* adjusted relative coverage (relative coverage / percent of adherents to religious family)
gen adj_rel_family = rel_family/adh_percentage
// asdoc table familyarda, c(mean adj_rel_family) dec(3)

drop _merge

* --- tabulation of numerical variables --- *

// asdoc tab stars

egen bin_views = cut(views), at(0 25 50 100 500 1000) icodes label
// tab bin_views
// asdoc tab bin_views

egen bin_sermonscontributed = cut(sermonscontributed), at(0 25 50 100 500 1515) icodes label
// tab bin_sermonscontributed
// asdoc tab bin_sermonscontributed

* --- save cleaned data --- *

save "intermediate/sermons.dta", replace

* --- make dataset for state coverage map --- *

drop index urlsermon title contributor contributiondate dateretrieved stars numberofratings views scripture denomination summary sermontext scriptures sermontopics talkaboutit urlcontributor contributingsermonssince churchname jobposition sermonscontributed denominationofsermon churchaddress education experience commenttothoselookingatmysermons sermonorseriesthatmadeadifferenc oneofmyfavoriteillustrations family whatmyparentsthinkofmysermons whatmyspousereallythinksofmyserm bestadvicegiventomeaboutpreachin booksthathavehadanimpact hobbies ificouldpreachonemoretimeiwoulds somethingfunnythathappenedwhilep whatiwantonmytombstone state_from_zip year abs_year rel_year date abs_denom rel_denom familyarda congregation adherents adherencerate abs_family rel_family adh_percentage adj_rel_family election04 election08 election12 election16 election20 election24 time_to_election04 time_to_election08 time_to_election12 time_to_election16 time_to_election20 time_to_election24 contribution_month contribution_year
sort state
quietly by state: gen dup = cond(_N == 1, 0, _n)
drop if dup > 1

save "output/state_coverage_map.dta", replace

* --- state coverage map --- *

* shape file from https://catalog.data.gov/dataset/tiger-line-shapefile-current-nation-u-s-state-and-equivalent-entities
shp2dta using "input/tl_2023_us_state/tl_2023_us_state.shp", ///
	data("input/tl_2023_us_state/us_states_data.dta") ///
	coordinates("input/tl_2023_us_state/us_states_coords.dta") ///
	genid(id) replace
	
use "input/tl_2023_us_state/us_states_data.dta", clear
rename NAME state
quietly destring STATEFP, generate(fips)
drop if fips > 56
save "input/tl_2023_us_state/us_states_data_for_map.dta", replace

* find ID for Alaska and Hawaii (32 and 41)
l fips id if fips == 2 | fips == 15

use "input/tl_2023_us_state/us_states_coords.dta", clear
* resize Hawaii
gen order = _n
drop if _X < -165 & _X != . & _ID == 32
replace _X = _X + 55 if _X != . & _ID == 32
replace _Y = _Y + 4 if _Y != . & _ID == 32
* resize Alaska
replace _X = _X * .4 - 55 if _X != . & _ID == 41
replace _Y = _Y * .4 + 1 if _Y != . & _ID == 41
drop if _X > -10 & _X != . & _ID == 41
sort order 
sort _ID
drop order
save "input/tl_2023_us_state/us_states_coords_for_map.dta", replace

use "input/tl_2023_us_state/us_states_data_for_map.dta", clear

* spmap using us_coords2, id(id)
merge 1:m state using "output/state_coverage_map.dta"
drop if _merge == 1

* absolute coverage for state
spmap rel_state using "input/tl_2023_us_state/us_states_coords_for_map.dta", id(id) fcolor(Blues) legend(on) title("Heat Map: Relative Coverage of Religious Sermons") legtitle("Relative Coverage")

* relative coverage for state
spmap adj_rel_state using "input/tl_2023_us_state/us_states_coords_for_map.dta", id(id) fcolor(Blues) legend(on) title("Heat Map: Adjusted Relative Coverage of Religious Sermons") legtitle("Adj Relative Coverage")
