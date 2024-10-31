import requests
import pandas as pd
import re
import csv

# GitHub API and headers
GITHUB_API_URL = "https://api.github.com"
TOKEN = "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"  # Replace with your GitHub PAT
HEADERS = {"Authorization": f"token {TOKEN}"}

# Search for Basel users with over 10 followers
def search_users(location="Basel", min_followers=10):
    url = f"{GITHUB_API_URL}/search/users"
    query = f"location:{location} followers:>{min_followers}"
    params = {"q": query, "per_page": 100}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json().get("items", [])

# Fetch detailed user data
def get_user_data(username):
    url = f"{GITHUB_API_URL}/users/{username}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

# Clean company names
def clean_company(company):
    if company:
        company = company.strip()
        company = re.sub(r'^@', '', company, count=1)  # Remove only the first '@'
        company = company.upper()
    return company

# Save user data to CSV
def save_users_to_csv(users):
    with open("users.csv", "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            "login", "name", "company", "location", "email", "hireable",
            "bio", "public_repos", "followers", "following", "created_at"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            cleaned_company = clean_company(user.get("company"))
            user["company"] = cleaned_company
            writer.writerow(user)

# Main function to gather user data
def main():
    users = search_users()
    detailed_users = []
    for user in users:
        user_data = get_user_data(user["login"])
        detailed_users.append({
            "login": user_data.get("login"),
            "name": user_data.get("name", ""),
            "company": user_data.get("company", ""),
            "location": user_data.get("location", ""),
            "email": user_data.get("email", ""),
            "hireable": user_data.get("hireable", ""),
            "bio": user_data.get("bio", ""),
            "public_repos": user_data.get("public_repos", 0),
            "followers": user_data.get("followers", 0),
            "following": user_data.get("following", 0),
            "created_at": user_data.get("created_at", "")
        })
    save_users_to_csv(detailed_users)

# if __name__ == "__main__":
#     main()

def get_user_repositories(username):
    url = f"{GITHUB_API_URL}/users/{username}/repos"
    params = {"sort": "pushed", "per_page": 100}
    repos = []
    page = 1
    while len(repos) < 500:
        response = requests.get(url, headers=HEADERS, params={**params, "page": page})
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos[:500]

def save_repositories_to_csv(repos):
    with open("repositories.csv", "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            "login", "full_name", "created_at", "stargazers_count",
            "watchers_count", "language", "has_projects", "has_wiki", "license_name"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repos:
            writer.writerow(repo)

def main_repositories():
    users = pd.read_csv("users.csv")["login"].tolist()
    all_repos = []
    for user in users:
        repos = get_user_repositories(user)
        for repo in repos:
            all_repos.append({
                "login": user,
                "full_name": repo.get("full_name", ""),
                "created_at": repo.get("created_at", ""),
                "stargazers_count": repo.get("stargazers_count", 0),
                "watchers_count": repo.get("watchers_count", 0),
                "language": repo.get("language", ""),
                "has_projects": repo.get("has_projects", False),
                "has_wiki": repo.get("has_wiki", False),
                "license_name": repo.get("license", {}).get("name", "") if repo.get("license") else ""

            })
    save_repositories_to_csv(all_repos)

if __name__ == "__main__":
    main_repositories()
