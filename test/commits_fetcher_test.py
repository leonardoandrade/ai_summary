from unittest.mock import patch
from git_repo.commits_fetcher import GitCommitFetcher

@patch('git_repo.commits_fetcher.Repo')
def test_fetch_last_n_commit_messages(mock_repo):
    # Mock the last 3 commits
    mock_commits = [
        'Commit message 3',
        'Commit message 2',
        'Commit message 1'
    ]
    mock_repo.return_value.iter_commits.return_value = [MockCommit(message) for message in mock_commits]
    
    directory_path = '/path/to/mock/git/repo'  
    n_commits = 3
    
    git_commit_fetcher = GitCommitFetcher(directory_path)
    last_n_commit_messages = git_commit_fetcher.fetch_last_n_commit_messages(n_commits)
    
    assert last_n_commit_messages == mock_commits

class MockCommit:
    def __init__(self, message):
        self.message = message




