import pandas as pd
import numpy as np
import statsmodels.api as sm
from datetime import datetime
from matplotlib import style
from matplotlib import pyplot as plt
import csv

# import data
df = pd.read_stata("input/cleaned_data.dta")
df = df.replace("Hillary Clinton", "Hilary Clinton ")
sample = df[30000:40000]

# list of candidate names to search for
candidate_names = [
    "George W. Bush", "John Kerry", "George Bush", "kerry", "george bush",
    "Barack Obama", "John McCain", "obama", "john mccain", "John Mccain",
    "President obama", "barack", "Mitt Romney", "mitt romney", "romney",
    "Donald Trump", "Hillary Clinton", "Clinton", "hillary", "donald",
    "Joe Biden", "biden", "President Bush", "President Obama", "President Trump", "President Biden"
]

# list of election-related words
election_words = [
    "Vote", "vote", "voting", "voted", "Voting", "Voted", "ballot", "Ballot", "Candidate", "candidate",
    "nominate", "Nominate", "Elect", "elect", "President", "president", "Politicians", "politicians",
    "Politician", "politician"
]

# election dates in datetime format
election_dates = {
    2004: pd.to_datetime("2004-11-02"), 
    2008: pd.to_datetime("2008-11-04"), 
    2012: pd.to_datetime("2012-11-06"),
    2016: pd.to_datetime("2016-11-08"), 
    2020: pd.to_datetime("2020-11-03")
}
election_months = ["2004-11", "2008-11", "2012-11", "2016-11", "2020-11", "2024-11"]
election_months = pd.to_datetime(election_months)
election_years = [2004, 2008, 2012, 2016, 2020]


# --- utility functions for counts and plots --- #

def count_election_words(text, words):
    padded_text = f" {text} "
    
    return sum(padded_text.count(f" {word} ") for word in words)


def simple_rdd_plot(data, running_var, outcome_var, cutoff= 0, bandwidth= 12, year= None):
    data_limited = data[(data[running_var] >= -bandwidth) & (data[running_var] <= bandwidth)].copy()

    # average for each unique value of running variable
    averaged_data = data_limited.groupby(running_var, as_index= False)[outcome_var].mean()
    averaged_data_neq_cutoff = averaged_data[averaged_data[running_var] != cutoff]

    # split data into sets before and after cutoff
    data_before_cutoff = averaged_data_neq_cutoff[averaged_data[running_var] < cutoff]
    data_after_cutoff = averaged_data_neq_cutoff[averaged_data[running_var] > cutoff]

    # linear regression on both sets
    model_before = sm.OLS(data_before_cutoff[outcome_var], sm.add_constant(data_before_cutoff[running_var])).fit()
    model_after = sm.OLS(data_after_cutoff[outcome_var], sm.add_constant(data_after_cutoff[running_var])).fit()

    # predictions
    data_before_cutoff["predictions"] = model_before.predict(sm.add_constant(data_before_cutoff[running_var]))
    data_after_cutoff["predictions"] = model_after.predict(sm.add_constant(data_after_cutoff[running_var]))

    plt.figure(figsize=(10, 6))
    plt.scatter(averaged_data_neq_cutoff[running_var], averaged_data_neq_cutoff[outcome_var], alpha= 0.7, label= "Observed Averages", color= "blue")
    plt.plot(data_before_cutoff[running_var], data_before_cutoff["predictions"], color= "red", label= "Fitted Line (Before Election)")
    plt.plot(data_after_cutoff[running_var], data_after_cutoff["predictions"], color= "green", label= "Fitted Line (After Election)")
    plt.axvline(cutoff, color= "black", linestyle= "--", label= "Cutoff (Election Day)")
    plt.title(f"RDD Plot (Election Year: {year})")
    plt.xlabel("Months to Nearest Election")
    plt.ylabel("Average Presidental Candidate Mentions")
    plt.legend()
    plt.grid(alpha= 0.3)
    plt.show()

    # print regression summaries
    print("\n--- Before Cutoff Regression ---")
    print(model_before.summary())
    print("\n--- after Cutoff Regression ---")
    print(model_after.summary())


# to calculate months difference between two dates
def months_difference(date1, date2):
    return (date1.year - date2.year) * 12 + (date1.month - date2.month)


# to calculate the month difference to the nearest election
def month_to_nearest_election(row, election_dates):
    contribution_date = row['date']
    closest_election = None
    min_diff = float('inf')

    for year, election_date in election_dates.items():
        # only consider elections within 24 months
        months_diff = months_difference(contribution_date, election_date)
        
        if -24 <= months_diff <= 24:
            if abs(months_diff) < abs(min_diff):
                min_diff = months_diff
                closest_election = year

    return min_diff if closest_election is not None else np.nan


def get_nearest_sunday(date):
    # 0 = Monday, ..., 6 = Sunday
    weekday = date.weekday()
    days_to_nearest_sunday = (7 - weekday) % 7

    return date + pd.Timedelta(days=days_to_nearest_sunday)


def weeks_to_nearest_election(row, election_dates):
    contribution_date = row['date']
    closest_election = None
    min_diff = float('inf')

    for year, election_date in election_dates.items():
        nearest_sunday = get_nearest_sunday(election_date)
        weeks_diff = (contribution_date - nearest_sunday).days // 7

        if -4 <= weeks_diff <= 4:
            if abs(weeks_diff) < abs(min_diff):
                min_diff = weeks_diff
                closest_election = year

    return min_diff if closest_election is not None else np.nan


# to calculate days difference between two dates
def days_difference(date1, date2):
    return (date1 - date2).days


def days_to_nearest_election(row, election_dates):
    contribution_date = row['date']
    closest_election = None
    min_diff = float('inf')

    # find nearest sunday to election
    for year, election_date in election_dates.items():
        nearest_sunday = get_nearest_sunday(election_date)
        days_diff = days_difference(contribution_date, nearest_sunday)

        if -28 <= days_diff <= 28:
            if abs(days_diff) < abs(min_diff):
                min_diff = days_diff
                closest_election = year

    return min_diff if closest_election is not None else np.nan


def get_tuesday_between_nov2_and_nov8(year):
    # range of possible dates: November 2nd to 8th
    start_date = pd.to_datetime(f"{year}-11-02")
    end_date = pd.to_datetime(f"{year}-11-08")

    # loop over range to find the Tuesday
    for day in range((end_date - start_date).days + 1):
        current_date = start_date + pd.Timedelta(days=day)
        
        if current_date.weekday() == 1:  # 1 == Tuesday
            return current_date


def days_to_tuesday(row, election_years):
    if row['date'].year not in election_years:
        tuesday_nonelection = get_tuesday_between_nov2_and_nov8(row['date'].year)
        days_to_tuesday = (row['date'] - tuesday_nonelection).days

        return days_to_tuesday


def days_to_election(row, election_year= None):
    election_date = election_dates.get(election_year)

    if election_date is not None:
        days_to_elec = (row['date'] - election_date).days
        
        return days_to_elec
    
    return None


# create a global variable 'weeks_to_election{year}' based on 'days_to_election{year}'.
def create_weeks_to_election(data, election_dates):
    for year, election_date in election_dates.items():
        # compute 'days_to_election{year}' if not already in dataset
        days_col = f"days_to_election{year}"
        week_col = f"weeks_to_election{year}"

        if days_col not in data.columns:
            data[days_col] = (data['date'] - election_date).dt.days

        # convert days to weeks by integer division (floor method)
        data[week_col] = (data[days_col] // 7)

    return data


# get the RDD with 7-day binned averages
def get_rdd_7bin(data, outcome_var, running_var, cutoff= 0, days_window= 28, bin_size= 7):
    data_limited = data[(data[running_var] >= -days_window) & (data[running_var] <= days_window)].copy()
    averaged_data = data_limited.groupby(running_var, as_index= False)[outcome_var].mean()  # calculate mean per day
    averaged_data['week_bins'] = (averaged_data[running_var] // bin_size) * bin_size

    binned_data = averaged_data.groupby('week_bins', as_index= False)[outcome_var].mean()  # here we calculate mean per week
    binned_data_neq_cutoff = binned_data[binned_data['week_bins'] != cutoff]

    # split data into sets before and after cutoff
    binned_data_before_cutoff = binned_data_neq_cutoff[binned_data_neq_cutoff['week_bins'] < cutoff]
    binned_data_after_cutoff = binned_data_neq_cutoff[binned_data_neq_cutoff['week_bins'] > cutoff]

    # linear regression on both sets
    model_before = sm.OLS(binned_data_before_cutoff[outcome_var], sm.add_constant(binned_data_before_cutoff['week_bins'])).fit()
    model_after = sm.OLS(binned_data_after_cutoff[outcome_var], sm.add_constant(binned_data_after_cutoff['week_bins'])).fit()

    # predictions
    binned_data_before_cutoff["predictions"] = model_before.predict(sm.add_constant(binned_data_before_cutoff['week_bins']))
    binned_data_after_cutoff["predictions"] = model_after.predict(sm.add_constant(binned_data_after_cutoff['week_bins']))

    return binned_data_neq_cutoff, binned_data_before_cutoff, binned_data_after_cutoff


# plot the RDD with 7-day binned averages of 'president_mentions_all' against the running variable (in weeks)
def plot_rdd_7bin_presi(data, outcome_var, running_var, cutoff= 0, days_window= 28, bin_size= 7, year= None):
    neq_cutoff, before_cutoff, after_cutoff = get_rdd_7bin(data, outcome_var, running_var, cutoff, days_window, bin_size)

    plt.figure(figsize=(10, 6))
    plt.scatter(neq_cutoff['week_bins'] / 7, neq_cutoff[outcome_var], alpha= 0.7, label= "7-Day Bin Average", color= "blue")
    plt.plot(before_cutoff['week_bins'] / 7, before_cutoff['predictions'], color= "red", label= "Fitted Line (Before Election)")
    plt.plot(after_cutoff['week_bins'] / 7, after_cutoff['predictions'], color= "green", label= "Fitted Line (After Election)")
    plt.title(f"RDD Plot (Election Year: {year}) - Weekly")
    plt.xlabel(f"Weeks to Nearest Election")
    plt.ylabel("Average Presidential Candidate Mentions per 7-Day Bin")
    plt.axvline(cutoff / 7, color= "black", linestyle= "--", label= "Election Date")
    plt.grid(alpha= 0.3)
    plt.legend()
    plt.show()

# plot the RDD with 7-day binned averages of 'president_mentions_all' against the running variable (in weeks) for non-election years
def plot_rdd_7bin_presi_non(data, outcome_var, running_var, cutoff= 0, days_window= 28, bin_size= 7):
    neq_cutoff, before_cutoff, after_cutoff = get_rdd_7bin(data, outcome_var, running_var, cutoff, days_window, bin_size)

    plt.figure(figsize=(10, 6))
    plt.scatter(neq_cutoff['week_bins'] / 7, neq_cutoff[outcome_var], alpha= 0.7, label= "7-Day Bin Average", color= "blue")
    plt.plot(before_cutoff['week_bins'] / 7, before_cutoff['predictions'], color= "red", label= "Fitted Line (Before Tuesday)")
    plt.plot(after_cutoff['week_bins'] / 7, after_cutoff['predictions'], color= "green", label= "Fitted Line (After Tuesday)")
    plt.title(f"RDD Plot (Non-Election Years) - Weekly")
    plt.xlabel(f"Weeks to Nearest Tuesday between 2nd-8th Nov")
    plt.ylabel("Average Presidential Candidate Mentions per 7-Day Bin")
    plt.axvline(cutoff / 7, color= "black", linestyle= "--", label= "Tuesday between 2nd-8th Nov")
    plt.grid(alpha= 0.3)
    plt.legend()
    plt.show()


# plot the RDD with 7-day binned averages of election words against the running variable (in weeks)
def plot_rdd_7bin_elec(data, outcome_var, running_var, cutoff= 0, days_window= 28, bin_size= 7, year= None):
    neq_cutoff, before_cutoff, after_cutoff = get_rdd_7bin(data, outcome_var, running_var, cutoff, days_window, bin_size)

    plt.figure(figsize=(10, 6))
    plt.scatter(neq_cutoff['week_bins'] / 7, neq_cutoff[outcome_var], alpha= 0.7, label= "7-Day Bin Average", color= "blue")
    plt.plot(before_cutoff['week_bins'] / 7, before_cutoff['predictions'], color= "red", label= "Fitted Line (Before Election)")
    plt.plot(after_cutoff['week_bins'] / 7, after_cutoff['predictions'], color= "green", label= "Fitted Line (After Election)")
    plt.title(f"RDD Plot (Election Year: {year}) - Weekly")
    plt.xlabel("Weeks to Nearest Election")
    plt.ylabel("Average Election-Related Word Mentions per 7-Day Bin")
    plt.axvline(cutoff / 7, color= "black", linestyle= "--", label= "Election Date")
    plt.grid(alpha= 0.3)
    plt.legend()
    plt.show()


# plot the RDD with 7-day binned averages of election words against the running variable (in weeks) for non-election years
def plot_rdd_7bin_elec_non(data, outcome_var, running_var, cutoff=0, days_window=28, bin_size=7):
    neq_cutoff, before_cutoff, after_cutoff = get_rdd_7bin(data, outcome_var, running_var, cutoff, days_window, bin_size)

    plt.figure(figsize=(10, 6))
    plt.scatter(neq_cutoff['week_bins'] / 7, neq_cutoff[outcome_var], alpha= 0.7, label= "7-Day Bin Average", color= "blue")
    plt.plot(before_cutoff['week_bins'] / 7, before_cutoff['predictions'], color= "red", label= "Fitted Line (Before Tuesday)")
    plt.plot(after_cutoff['week_bins'] / 7, after_cutoff['predictions'], color= "green", label= "Fitted Line (After Tuesday)")
    plt.title(f"RDD Plot (Non-Election Years) - Weekly")
    plt.xlabel("Weeks to Nearest Tuesday between 2nd-8th Nov")
    plt.ylabel("Average Election-Related Word Mentions per 7-Day Bin")
    plt.axvline(cutoff / 7, color= "black", linestyle= "--", label= "Tuesday between 2nd-8th Nov")
    plt.grid(alpha= 0.3)
    plt.legend()
    plt.show()


# --- create time variables --- #

# calculate 'month_to_nearest_election'
df['month_to_nearest_election'] = df.apply(month_to_nearest_election, axis= 1, election_dates= election_dates)

# convert 'date' to datetime format
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# calculate 'weeks_to_nearest_election'
df['week_to_nearest_election'] = df.apply(weeks_to_nearest_election, axis= 1, election_dates= election_dates)

# calculate 'days_to_electionXX':
for year in election_years:
    # Add the weeks_to_electionXX variable for each election year
    df[f'days_to_election{year}'] = df.apply(days_to_election, axis= 1, election_year= year)

# calculate 'weeks_to_electionXX':
for year in election_dates.keys():
    days_col = f"days_to_election{year}"
    week_col = f"weeks_to_election{year}"

    # ensure column exists before applying transformation
    if days_col in df.columns:
        df[week_col] = df[days_col] // 7


# calculate 'days_to_nearest_election'
df['days_to_nearest_election'] = df.apply(days_to_nearest_election, axis= 1, election_dates= election_dates)

# days to tuesday between 2nd and 8th of nov
df['days_to_tuesday'] = df.apply(days_to_tuesday, axis= 1, election_years= election_years)


# --- create mention variables --- #

df["president_mentions_all"] = df["sermontext"].apply(lambda x: count_election_words(str(x), candidate_names))
df["election_word_count"] = df["sermontext"].apply(lambda x: count_election_words(str(x), election_words))


# --- whole average --- #

total_sume = df["election_word_count"].sum()
total_average_e = total_sume/166308
print(total_average_e)

total_sump = df["president_mentions_all"].sum()
total_average_p = total_sump/166308
print(total_average_p)


# --- export to stata --- #

# remove any leading/trailing spaces in column names
df.columns = df.columns.str.strip()

# clean string columns
df = df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
df.to_csv("output/cleaned_data.csv", encoding= 'utf-8', index= True, quoting= csv.QUOTE_ALL)


# --- election related words graphs --- #

# RDD style plots for election related words
plot_rdd_7bin_elec(
    data= df, outcome_var= "election_word_count", running_var= "days_to_election2004", 
    cutoff= 0, days_window= 28, bin_size= 7, year= 2004
)

plot_rdd_7bin_elec(
    data= df, outcome_var= "election_word_count", running_var= "days_to_election2008", 
    cutoff= 0, days_window= 28, bin_size= 7, year= 2008
)

plot_rdd_7bin_elec(
    data= df, outcome_var= "election_word_count", running_var= "days_to_election2012", 
    cutoff= 0, days_window= 28, bin_size= 7, year= 2012
)

plot_rdd_7bin_elec(
    data= df, outcome_var= "election_word_count", running_var= "days_to_election2016", 
    cutoff= 0, days_window= 28, bin_size= 7, year= 2016
)

plot_rdd_7bin_elec(
    data= df, outcome_var= "election_word_count", running_var= "days_to_election2020", 
    cutoff= 0, days_window= 28, bin_size= 7, year= 2020
)

# overlapping plots for election related words
# monthly analysis - election years
simple_rdd_plot(
    data= df, running_var= "month_to_nearest_election", outcome_var= "election_word_count", 
    cutoff= 0, year= "All"
)

# weekly analysis with 7 day bins - election years
plot_rdd_7bin_elec(
    data= df, outcome_var= "election_word_count", running_var= "days_to_nearest_election",
    cutoff= 0, days_window= 28, bin_size= 7, year= "All"
)

# daily analysis - non election years
plot_rdd_7bin_elec_non(
    data= df, outcome_var= "election_word_count", running_var= "days_to_tuesday", 
    cutoff= 0, days_window= 28, bin_size= 7
)

# election related word count plot
df["contribution_monthly"] = pd.to_datetime(df["contribution_monthly"])
# aggregate counts by monthly timestamp column
monthly_counts_elec = df.groupby("contribution_monthly")["election_word_count"].sum().reset_index()
# plot
plt.figure(figsize= (12, 6))
plt.plot(monthly_counts_elec["contribution_monthly"], monthly_counts_elec["election_word_count"], label= "Word Count", color= "blue")
# add vertical lines for specific months
election_months = pd.to_datetime(election_months)
for month in election_months:
    plt.axvline(month, color= "black", linestyle= "--", linewidth= 1)
plt.title("Election-Related Word Occurrences in Religious Sermons Over Time")
plt.xlabel("Month-Year")
plt.ylabel("Word Count")
plt.xticks(rotation= 45)
plt.grid(alpha= 0.3)
plt.legend()
plt.tight_layout()
plt.show()


# --- presidential candidate mentions ---

# RDD style plots for presidential candidate mentions
plot_rdd_7bin_presi(
    data= df, outcome_var= "president_mentions_all", running_var= "days_to_election2004", 
    cutoff= 0, days_window= 28, bin_size= 7, year= 2004
)

plot_rdd_7bin_presi(
    data= df, outcome_var= "president_mentions_all", running_var= "days_to_election2008", 
    cutoff= 0, days_window= 28, bin_size= 7, year= 2008
)

plot_rdd_7bin_presi(
    data= df, outcome_var= "president_mentions_all", running_var= "days_to_election2012", 
    cutoff= 0, days_window= 28, bin_size= 7, year= 2012
)

plot_rdd_7bin_presi(
    data= df, outcome_var= "president_mentions_all", running_var= "days_to_election2016", 
    cutoff= 0, days_window= 28, bin_size= 7, year= 2016
)

plot_rdd_7bin_presi(data= df, outcome_var= "president_mentions_all", running_var= "days_to_election2020", 
    cutoff= 0, days_window= 28, bin_size= 7, year= 2020
)

# overlapping plots for presidential candidate mentions
# monthly analysis - election years
simple_rdd_plot(
    data= df, running_var= "month_to_nearest_election", outcome_var= "president_mentions_all",
    cutoff= 0, year= None
)

# weekly analysis with 7 day bins - election years
plot_rdd_7bin_presi(
    data= df, outcome_var= "president_mentions_all", running_var= "days_to_nearest_election", 
    cutoff= 0, days_window= 28, bin_size= 7, year= "All"
)

# weekly analysis with 7 day bins - non election years
plot_rdd_7bin_presi_non(
    data= df, outcome_var= "president_mentions_all", running_var= "days_to_tuesday", 
    cutoff= 0, days_window= 28, bin_size= 7
)

# word count plot for presidential candidate mentions
monthly_counts_presi = df.groupby("contribution_monthly")["president_mentions_all"].sum().reset_index()
# plot
plt.figure(figsize= (12, 6))
plt.plot(monthly_counts_presi["contribution_monthly"], monthly_counts_presi["president_mentions_all"], label= "Word Count", color= "blue")
for month in election_months:
    plt.axvline(month, color= "black", linestyle= "--", linewidth= 1)
plt.title("Presidential Candidates Mentions in Religious Sermons Over Time")
plt.xlabel("Month-Year")
plt.ylabel("Word Count")
plt.xticks(rotation= 45)
plt.grid(alpha= 0.3)
plt.legend()
plt.tight_layout()
plt.show()
