import os
from files_reader import directory_scanner 

import pytest

@pytest.fixture
def scanner():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mock_directory_path = os.path.join(current_dir, "./mock_directory")
    return directory_scanner.DirectoryScanner(mock_directory_path)

def test_list_files(scanner):
    expected_files = [
        ".gitignore",
        "index.js",
        "package.json",
        "README.md",
        "src/client.js",
        "src/server.js",
        "test/test_server.js"
    ]

    files = scanner.list_files()
    assert sorted(files) == sorted(expected_files)
