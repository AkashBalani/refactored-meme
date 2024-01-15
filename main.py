import os
import requests

def list_github_repos(username):
    github_token = os.environ.get('GITHUB_ACCESS_TOKEN')

    if github_token is None:
        print("Error: GitHub access token not found in environment variables.")
        return

    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            repositories = response.json()
            print(f"GitHub repositories for {username}:")
            for repo in repositories:
                print(repo['name'])
        else:
            print(f"Error: Unable to fetch repositories. Status code: {response.status_code}")

    except Exception as e:
        print("An error occurred:", e)

# Replace 'YOUR_GITHUB_USERNAME' with your GitHub username
github_username = 'AkashBalani'

list_github_repos(github_username)
