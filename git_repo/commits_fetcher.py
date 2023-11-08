from git import Repo

class GitCommitFetcher:
    def __init__(self, directory: str):
        self.directory = directory
        self.repo = Repo(directory)

    def fetch_last_n_commit_messages(self, n: int) -> list:
        commit_messages = []
        for commit in self.repo.iter_commits(max_count=n):
            commit_messages.append(commit.message.strip())  # Remove leading/trailing whitespaces
        return commit_messages