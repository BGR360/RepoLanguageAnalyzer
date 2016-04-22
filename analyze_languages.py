"""
GitHub User Repository Language Analyzer
Created By: Ben Reeves
Date: January 8, 2015

Description:
This script uses the PyGithub library to access the Github API in order to perform some data analysis on a user's
repositories. Specifically, it will analyze all of the user's code and calculate the percentage of code written in
different programming languages.
"""

import operator
from getpass import getpass
from github import Github
from github import GithubException
from PyChart import PyChart

calculate_by_percentage = True
MIN_PERCENT = 1.0

def sort_by_value(dictionary):
    """
    Sorts a dictionary by its values (not its keys)
    :param dictionary: The dictionary we want to sort
    :return: A list of 2-tuples sorted by their second values
    """
    return sorted(dictionary.items(), key=operator.itemgetter(1))

def sum_values(dictionary):
    """
    Sums up all the values in a dictionary (not the keys)
    :param dictionary: The dictionary we want to sum up
    :return: The sum of all the values from the dictionary
    """
    return sum(dictionary.values())


print "Please login to your GitHub account."
login = raw_input("Username: ")
password = getpass("Password: ")

# Check to make sure they entered valid credentials
gh = Github(login, password)
try:
    gh.get_user().name
except GithubException:
    print "Error: Authentication failed. Exiting..."
    exit(1)

# User can enter a valid GitHub username or enter nothing (if they enter nothing, we will use their account)
username = raw_input("Enter a GitHub username you would like to invesigate: ")
if username == '':
    username = login

# Check if they entered a valid username
try:
    gh.get_user(username).name
except GithubException:
    print "Error: No such user exists. Exiting..."
    exit(1)

print
print "Crunching data for user %s..." % username
print

#----------------------------------
#      Perform the analysis
#----------------------------------

# The GitHub API returns how many bytes of code are written in each language.
percentages_per_repo = []
bytes_per_repo = []
primary_language_per_repo = []

# Go through all the user's public repositories
for repo in gh.get_user(username).get_repos():
    if not repo.private and not repo.fork:
        # If the repository has "None" as its primary language, don't include it
        if repo.language:
            print "Found repo: %s - %s" % (repo.name, repo.language)
            # Get the primary language for that repo
            primary_language_per_repo.append(repo.language)
            # Get the number of bytes used in each language
            languages = repo.get_languages()
            # Figure out what percent of the repo is each language
            percentages_in_this_repo = {}
            bytes_in_this_repo = {}
            total_num_bytes = sum_values(languages)
            for language in languages:
                num_bytes = languages[language]
                bytes_in_this_repo[language] = num_bytes
                percentage = float(num_bytes) / total_num_bytes
                percentages_in_this_repo[language] = percentage
            percentages_per_repo.append(percentages_in_this_repo)
            bytes_per_repo.append(bytes_in_this_repo)
    else:
        print "Skipped repo: %s - %s" % (repo.name, repo.language)

### print percentages_per_repo

pie_chart_data = {}

if calculate_by_percentage:
    # Add up all the percentages from each repo
    percentages_per_language = {}
    for repo_percentages in percentages_per_repo:
        for language in repo_percentages:
            language_percentage = repo_percentages[language]
            if language in percentages_per_language:
                percentages_per_language[language] += language_percentage
            else:
                percentages_per_language[language] = language_percentage
    ### print percentages_per_language

    pie_chart_data = percentages_per_language
else:
    # Calculate based on number of bytes of each language
    bytes_per_language = {}
    for repo_bytes in bytes_per_repo:
        for language in repo_bytes:
            language_bytes = repo_bytes[language]
            if language in bytes_per_language:
                bytes_per_language[language] += language_bytes
            else:
                bytes_per_language[language] = language_bytes

    pie_chart_data = bytes_per_language

### print pie_chart_data

# Normalize the values so they sum to 100
total = sum_values(pie_chart_data)
pie_copy = {}
for language in pie_chart_data:
    value = pie_chart_data[language]
    percentage = float(value) / total * 100
    # Remove data less than 1.0%
    if percentage >= MIN_PERCENT:
        pie_copy[language] = percentage

pie_chart_data = sort_by_value(pie_copy)
pie_chart_data.reverse()

# Print out the results
print
print "Data has been crunched. Here's what's up with %s's repositories:" % username
print
for language, percentage in pie_chart_data:
    print "%s: %.2f%%" % (language, percentage)

# Draw a pie chart for the data
pie_chart = PyChart(pie_chart_data)
pie_chart.draw()
