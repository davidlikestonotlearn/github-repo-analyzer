
"""Analyze a GitHub user's public repositories using the GitHub REST API."""

from collections import Counter
import requests

BASE_URL = "https://api.github.com"
PER_PAGE = 100


def get_repositories(username):
    """Return all public repositories, or None if a request fails."""
    all_repos = []
    page = 1

    with requests.Session() as session:
        session.headers.update({"Accept": "application/vnd.github+json"})

        while True:
            try:
                response = session.get(
                    f"{BASE_URL}/users/{username}/repos",
                    params={"per_page": PER_PAGE, "page": page},
                    timeout=10,
                )
            except requests.exceptions.RequestException as error:
                print(f"Request failed: {error}")
                return None

            if response.status_code == 404:
                print("User does not exist.")
                return None

            if response.status_code != 200:
                print(f"GitHub API error: {response.status_code}")
                return None

            try:
                repos = response.json()
            except ValueError:
                print("GitHub returned invalid JSON.")
                return None

            if not isinstance(repos, list):
                print("Unexpected response from GitHub.")
                return None

            if not repos:
                break

            all_repos.extend(repos)

            if len(repos) < PER_PAGE:
                break

            page += 1

    return all_repos


def find_popular_repo(repos):
    """Return the repository with the most stars."""
    return max(
        repos,
        key=lambda repo: repo["stargazers_count"],
        default=None
    )


def rank_repositories(repos):
    """Sort repositories from most stars to least stars."""
    return sorted(
        repos,
        key=lambda repo: repo["stargazers_count"],
        reverse=True
    )


def count_languages(repos):
    """Count repositories by their primary programming language."""
    return Counter(
        repo["language"]
        for repo in repos
        if repo.get("language")
    )


def main():
    username = input("Enter GitHub username: ").strip()

    if not username:
        print("Please enter a username.")
        return

    repos = get_repositories(username)

    if repos is None:
        return

    print(f"\nTotal public repositories fetched: {len(repos)}")

    if not repos:
        print("No public repositories found.")
        return

    most_popular = find_popular_repo(repos)

    print(f"\nMost starred repository: {most_popular['name']}")
    print(f"Stars: {most_popular['stargazers_count']}")

    print("\nRepositories ranked by stars:")

    for index, repo in enumerate(rank_repositories(repos), start=1):
        language = repo.get("language") or "Unknown"
        print(
            f"{index}. {repo['name']} — "
            f"{repo['stargazers_count']} stars ({language})"
        )

    languages = count_languages(repos)

    print("\nPrimary languages by repository count:")

    if not languages:
        print("No primary languages detected.")
    else:
        for language, count in languages.most_common():
            print(f"{language}: {count} repositories")

        print(f"\nMost common language: {languages.most_common(1)[0][0]}")


if __name__ == "__main__":
    main()
