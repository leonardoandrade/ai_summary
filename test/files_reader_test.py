import os
from files_reader.files_reader import FileReader
import pytest

@pytest.fixture
def file_reader():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    mock_directory_path = os.path.join(current_dir, "mock_directory")
    filenames = [
        os.path.join(mock_directory_path, "index.js"),
        os.path.join(mock_directory_path, "package.json"),
        os.path.join(mock_directory_path, "README.md"),
        os.path.join(mock_directory_path, "src/client.js"),
        os.path.join(mock_directory_path, "src/server.js"),
        os.path.join(mock_directory_path, "test/test_server.js"),
        os.path.join(mock_directory_path, "v2.zip")
    ]
    return FileReader(filenames)

def test_read_files(file_reader):
    file_contents = file_reader.read_files()
    assert len(file_contents) == 7

    assert file_contents[0].filename == "test/mock_directory/index.js"
    assert file_contents[0].is_binary is False
    assert file_contents[0].content.startswith("console.log('Hello, world!');")

    assert file_contents[1].filename == "test/mock_directory/package.json"
    assert file_contents[1].is_binary is False
    assert file_contents[1].content.startswith("{")
    assert '"name": "mock-directory"' in file_contents[1].content

    assert file_contents[2].filename == "test/mock_directory/README.md"
    assert file_contents[2].is_binary is False
    assert file_contents[2].content.startswith("# Mock Directory")

    assert file_contents[3].filename == "test/mock_directory/src/client.js"
    assert file_contents[3].is_binary is False
    assert file_contents[3].content.startswith("function client() {")
    
    assert file_contents[4].filename == "test/mock_directory/src/server.js"
    assert file_contents[4].is_binary is False
    assert file_contents[4].content.startswith("function server() {")
    
    assert file_contents[5].filename == "test/mock_directory/test/test_server.js"
    assert file_contents[5].is_binary is False
    assert file_contents[5].content.startswith("function testServer() {")
    
    assert file_contents[6].filename == "test/mock_directory/v2.zip"
    assert file_contents[6].is_binary is True
    assert file_contents[6].content == ""

# Run the tests with pytest
# Ensure that your test file is in the same directory as your implementation files
# Run: pytest test_file_reader.py
