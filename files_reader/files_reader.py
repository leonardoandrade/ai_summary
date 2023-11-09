from typing import List, Optional
import os
class FileContent:
    def __init__(self, filename: str, content: str, is_binary: bool) -> None:
        self.filename: str = filename
        self.content: str = content
        self.is_binary: bool = is_binary

class FileReader:
    def __init__(self, filenames: List[str], num_lines: Optional[int] = 200) -> None:
        self.filenames: List[str] = filenames
        self.num_lines: int = num_lines

    def read_files(self) -> List[FileContent]:
        file_contents: List[FileContent] = []

        for filename in self.filenames:
            try:
                with open(filename, 'rb') as file:
                    is_binary = b'\x00' in file.read(1024)  # Check if the file contains null bytes within the first 1024 bytes
                    relative_filename = os.path.relpath(filename)  # Get the relative filename

                    if not is_binary:
                        with open(filename, 'r', encoding='utf-8') as text_file:
                            lines = text_file.readlines()[:self.num_lines]  # Read only the first self.num_lines lines
                            content = ''.join(lines)
                            file_contents.append(FileContent(relative_filename, content, is_binary))
                    else:
                        file_contents.append(FileContent(relative_filename, '', is_binary))
            except FileNotFoundError:
                print(f"File '{filename}' not found.")
            except PermissionError:
                print(f"Permission denied for '{filename}'.")
            except Exception as e:
                print(f"Error reading '{filename}': {e}")
        return file_contents