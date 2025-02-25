import requests
import pandas as pd
import time

# Your GitHub personal access token
GITHUB_TOKEN = 'THETOKEN'  # Replace with your GitHub token
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}

# Base URL for GitHub API
BASE_URL = "https://api.github.com"

import time

def fetch_users_in_basel():
    """Fetch users in Basel with 10 or more followers and handle pagination thoroughly."""
    users = []
    url = f"{BASE_URL}/search/users?q=location:Basel+followers:>=10&per_page=100"
    
    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            break
        
        data = response.json()
        
        # Check for the expected key in response data
        if 'items' not in data:
            print("Unexpected data format:", data)
            break
        
        # Append each user's login to the list
        for user in data['items']:
            users.append(user['login'])
        
        # Check if there is a next page; GitHub includes pagination links in the headers
        if 'next' in response.links:
            url = response.links['next']['url']
            time.sleep(1)  # Optional: Pause to avoid hitting rate limits
        else:
            url = None  # No more pages

    print(f"Total users fetched: {len(users)}")
    return users


def clean_company(company):
    """Clean and standardize the company name."""
    if company:
        company = company.lstrip('@').strip().upper()
    return company or ''  # Empty string if None

def clean_location(location):
    """Ensure location mentions Basel if available."""
    if location and 'basel' in location.lower():
        return 'Basel'
    return location or ''  # Empty string if None

def get_user_details(username):
    """Fetch detailed information for a single user with cleaning."""
    url = f"{BASE_URL}/users/{username}"
    response = requests.get(url, headers=HEADERS)
    user_data = response.json()
    
    # Clean and prepare data fields
    company = clean_company(user_data.get('company', ''))
    location = clean_location(user_data.get('location', ''))

    return {
        'login': user_data['login'],
        'name': user_data.get('name', '') or '',
        'company': company,
        'location': location,
        'email': user_data.get('email', '') or '',
        'hireable': user_data.get('hireable', ''),
        'bio': user_data.get('bio', '') or '',
        'public_repos': user_data.get('public_repos', 0),
        'followers': user_data.get('followers', 0),
        'following': user_data.get('following', 0),
        'created_at': user_data.get('created_at', '') or ''
    }

def main():
    # Fetch users in Basel
    usernames = fetch_users_in_basel()
    user_data = []

    # Get details for each user
    for username in usernames:
        details = get_user_details(username)
        user_data.append(details)
    
    # Save to users.csv
    users_df = pd.DataFrame(user_data)
    users_df.to_csv("users.csv", index=False)
    print("Data saved to users.csv")

# Run the main function
if __name__ == "__main__":
    main()
