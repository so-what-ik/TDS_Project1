# Basel GitHub Users and Repositories Analysis

## Summary
- Data Collection: Leveraging the GitHub API, this project collects detailed profiles and repositories for all GitHub users in Basel with over 10 followers.
- Key Insight: Basel developers with longer bios tend to have more followers, hinting that a well-articulated profile boosts visibility.
- Recommendation: Developers aiming to attract followers or recruiters should consider sharing more detailed bios and enabling project features to foster engagement.

## Project Description
This project involves scraping user profiles and repositories from GitHub for developers based in Basel with over 10 followers. The code is split into two parts:
- fetch_users.py: Collects user profiles with detailed information such as their name, company, bio, follower count, and more.
- fetch_repos.py: Gathers information about each user’s repositories, including stargazer counts, programming languages, and licenses.
  
The output includes two CSV files:
- users.csv: Contains GitHub users’ details with cleaned-up company names (trimming whitespace, removing leading "@" symbols, and converting to uppercase).
- repositories.csv: Details each user’s public repositories, including their creation date, star count, language, license type, and settings for project and wiki features.
  
Both scripts are coded in Python and are designed to handle up to 500 repositories per user, as allowed by GitHub’s API rate limits.

## Project Setup
To reproduce the data collection, ensure you have a valid GitHub API token with the necessary permissions. Set up the environment by installing Python libraries required for API requests, data handling, and CSV manipulation.
  Run fetch_users.py to gather user data, followed by fetch_repos.py to fetch repositories data.

## Files in this Repository
- users.csv: GitHub user profiles in Basel with over 10 followers.
- repositories.csv: Repositories data linked to each user in users.csv.
- fetch_users.py: Script for fetching user profiles.
- fetch_repos.py: Script for fetching repository details.
- README.md: Documentation for the project and analysis findings.

# <p align="center">THANK YOU</p>
