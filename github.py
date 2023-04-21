"""Download README.md files of a github repositories using Github API."""
import os
import sys
import requests
import base64
from dotenv import load_dotenv

class GitHubRepoDownloader:
    def __init__(self, user, token):
        self.user = user
        self.token = token

    def download_repository_file(self, repo_owner, repo_name, file_path):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        json_response = response.json()
        if "content" in json_response:
            content = json_response["content"]
            decoded_content = base64.b64decode(content).decode("utf-8")
            print(f"{repo_owner}/{repo_name} - {file_path} Found!")
            return decoded_content
        else:
            print("Error: " + json_response.get("message", "Unknown error"))
            return ""

    def get_repository_file_url(self, repo_owner, repo_name, file_path):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        json_response = response.json()
        if "download_url" in json_response:
            url = json_response["download_url"]
            print(f"{repo_owner}/{repo_name} - {file_path} Found!")
            return url
        else:
            print("Error: " + json_response.get("message", "Unknown error"))
            return ""

    def list_starred_repositories(self):
        url = f"https://api.github.com/users/{self.user}/starred"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        starred_repos = response.json()
        return [repo["full_name"] for repo in starred_repos]
    
    def get_all_starred_repo_markdown_files(self):
        repos = self.list_starred_repositories()
        collection = []
        for repo in repos:
            splitted_name = repo.split('/')
            owner = splitted_name[0]
            name = splitted_name[1]
            file = 'README.md'
            data = self.download_repository_file(owner, name, file)
            collection.append(data)
        return collection

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user = sys.argv[1]
        load_dotenv()
        downloader = GitHubRepoDownloader(user, os.environ.get("GITHUB_API_KEY"))
        print(downloader.get_all_starred_repo_markdown_files())
    else:
        print("Usage: github.py github-username")
