import requests

username = input("Get a user: ")

def get_repositories(username):
    # Fetch repositories from GitHub
    page = 1
    all_repos = []

    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"

        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            print("User does not exist")
            return None
        elif response.status_code != 200:
            print(f"API ERROR: {response.status_code}")
            return None

        repos = response.json()

        if len(repos) == 0:
            break

        all_repos.extend(repos)
        page += 1

    return all_repos


def find_popular_repo(repos):
    # Find the repository with the most stars
    maxStars = -1
    popularRepo = None
    
    for repo in repos:
        stars = repo["stargazers_count"]
    
        if stars > maxStars:
            maxStars = stars
            popularRepo = repo["name"]
    
    if popularRepo is not None:
        print(f"\nMost popular repository: {popularRepo}")
        print(f"Stars: {maxStars}")
    else:
        print("No repositories found")
    

def rank_repositories(repos):
    # Sort repositories by stars
    sorted_repos = sorted(
            repos,
            key=lambda repo: repo["stargazers_count"],
            reverse=True
        )
    
    print("\nRepositories ranked by stars:")
    
    for index, repo in enumerate(sorted_repos, start=1):
        print(f"{index}. {repo['name']} - {repo['stargazers_count']} stars")

repos = get_repositories(username)
find_popular_repo(repos)
rank_repositories(repos)