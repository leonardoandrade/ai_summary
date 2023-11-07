import os
from typing import List
import fnmatch

class DirectoryScanner:
    def __init__(self, directory_path: str) -> None:
        self._directory_path: str = directory_path
        self._ignore_list: List[str] = self._load_gitignore()

    def _load_gitignore(self) -> List[str]:
        gitignore_path: str = os.path.join(self._directory_path, ".gitignore")
        ignore_list: List[str] = []
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as file:
                ignore_list = file.read().splitlines()
        return ignore_list

    def _should_ignore(self, path: str) -> bool:
        for pattern in self._ignore_list:
            if pattern and pattern[0] != '#':  # Ignore comments in .gitignore
                if pattern.endswith("/"):  # Directory pattern
                    if path.startswith(pattern[:-1]):
                        return True
                else:  # File pattern
                    if fnmatch.fnmatch(os.path.basename(path), pattern):
                        return True
        return False

    def scan(self) -> List[str]:
        file_list: List[str] = []
        for root, dirs, files in os.walk(self._directory_path):
            dirs[:] = [d for d in dirs if not self._should_ignore(os.path.join(root, d))]
            files[:] = [f for f in files if not self._should_ignore(os.path.join(root, f))]
            for file in files:
                relative_path = os.path.relpath(os.path.join(root, file), self._directory_path)
                file_list.append(relative_path)
        return file_list

