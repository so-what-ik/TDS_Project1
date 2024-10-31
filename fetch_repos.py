import requests
import pandas as pd
import time

# Your GitHub personal access token
GITHUB_TOKEN = 'THETOKEN'  # Replace with your GitHub token
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}
BASE_URL = "https://api.github.com"

def get_user_repositories(username):
    """Fetch up to 500 most recent public repositories for a user."""
    repos = []
    url = f"{BASE_URL}/users/{username}/repos?sort=pushed&per_page=100"
    
    while url and len(repos) < 500:
        response = requests.get(url, headers=HEADERS)
        
        # Error handling for API issues
        if response.status_code != 200:
            print(f"Error fetching repos for {username}: {response.status_code}")
            break
        
        data = response.json()

        for repo in data:
            repos.append({
                'login': username,
                'full_name': repo['full_name'],
                'created_at': repo['created_at'],
                'stargazers_count': repo['stargazers_count'],
                'watchers_count': repo['watchers_count'],
                'language': repo['language'],
                'has_projects': repo['has_projects'],
                'has_wiki': repo['has_wiki'],
                'license_name': repo['license']['name'] if repo['license'] else ''
            })

        # Check if there is a next page for repositories
        if 'next' in response.links:
            url = response.links['next']['url']
            time.sleep(1)  # Optional delay to avoid hitting rate limits
        else:
            url = None  # No more pages
    
    return repos

def main():
    # Load usernames from users.csv
    users_df = pd.read_csv("users.csv")
    usernames = users_df['login'].tolist()
    
    # List to hold repository data
    repo_data = []

    # Fetch repositories for each user
    for username in usernames:
        user_repos = get_user_repositories(username)
        repo_data.extend(user_repos)
        print(f"Fetched {len(user_repos)} repos for user: {username}")

    # Convert to DataFrame and save to repositories.csv
    repos_df = pd.DataFrame(repo_data)
    repos_df.to_csv("repositories.csv", index=False)
    print("Data saved to repositories.csv")

# Run the main function
if __name__ == "__main__":
    main()
