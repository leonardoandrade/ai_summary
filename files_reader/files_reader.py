from typing import List
import os
import magic

class FileContent:
    def __init__(self, filename: str, content: str, is_binary: bool) -> None:
        self.filename: str = filename
        self.content: str = content
        self.is_binary: bool = is_binary

class FileReader:
    def __init__(self, filenames: List[str]) -> None:
        self.filenames: List[str] = filenames

    def read_files(self) -> List[FileContent]:
        file_contents: List[FileContent] = []
        mime = magic.Magic()
        for filename in self.filenames:
            try:
                with open(filename, 'rb') as file:
                    file_content: bytes = file.read()
                    is_binary: bool = b'\x00' in file_content  # Check if the file contains null bytes (indicating binary)
                    content: str = file_content.decode('utf-8') if not is_binary else ''
                    relative_filename = os.path.relpath(filename)  # Get the relative filename
                    file_contents.append(FileContent(relative_filename, content, is_binary))
            except FileNotFoundError:
                print(f"File '{filename}' not found.")
            except PermissionError:
                print(f"Permission denied for '{filename}'.")
            except Exception as e:
                print(f"Error reading '{filename}': {e}")
        return file_contents