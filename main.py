import argparse
import os
from typing import Optional, List
from files_reader.files_reader import FileReader, FileContent
from files_reader.directory_scanner import DirectoryScanner
from open_ai_client.open_ai_client import OpenAIClient

OPEN_AI_KEY = "OPEN_AI_KEY"

PROMPT_PREFIX = """
Please generate a README file in markdown for a code project. The file names and content are given as follows (separated by line with "======="): 

"""

PROMPT_SUFFIX = """

**LLM-generated by [AI summarizer](https://github.com/leonardoandrade/ai_summary)**
"""


def get_openai_key() -> str:
    openai_key = os.getenv(OPEN_AI_KEY)
    if not openai_key:
        raise EnvironmentError("OPEN_AI_KEY environment variable is not set.")
    return openai_key


# TODO: add support for target README size
def make_prompt(file_contents: List[FileContent]):
    prompt = PROMPT_PREFIX

    for content in file_contents:
        prompt += f"\n\nFile path: {content.filename}\n"
        if not content.is_binary:
            prompt += f"File content: {content.content}\n"
        else:
            prompt += "File is binary, content now shown\n"
        prompt += "=======\n"

    prompt += f"""

        END OF FILES, following instructions are important:
    
        For the readme, the following guidelines should apply:
        1. Only the content, in markdown, nothing else
        2. Enumerate and describe each directory, but not individual files
        3. Do NOT describe the dependencies
        4. Have a section summarizing the TODOS
        5. Add a single Emoji at the end of each section title (line starting with ##, for example "## TODOS"), with meaning related to the section. If no meaningful emoji can be found, use the a random emoji,

        """
    return prompt + PROMPT_SUFFIX


def save_prompt(prompt):
    with open("/tmp/.last_prompt", "w", encoding="utf-8") as output_file:
        output_file.write(prompt)
    output_file.close()



def generate_readme(content: str, target_file: str) -> None:
    with open(target_file, "w", encoding="utf-8") as output_file:
        output_file.write(content)
    output_file.close()



def main(
    directory: str, target_file: str, generate_changelog: Optional[bool] = True
) -> None:
    files = DirectoryScanner(directory).scan()
    file_contents = FileReader(files).read_files()

    llm_client = OpenAIClient(get_openai_key(), temperature=0.7)

    prompt = make_prompt(file_contents)

    readme_content = llm_client.generate_chat_completion(prompt=prompt)

    save_prompt(prompt)

    # Generate README.md file
    generate_readme(readme_content, target_file)

    # Generate changelog if specified
    if generate_changelog:
        print("TODO: generate changelog")

    print(f"README.md file generated successfully at: {target_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="AI Summary: Generate a README.md file using Large Language Model (LLM)"
    )
    parser.add_argument(
        "directory", type=str, help="The directory containing the files to process."
    )
    parser.add_argument(
        "target_file", type=str, help="The target README.md file to generate."
    )
    parser.add_argument(
        "--generate-changelog",
        action="store_true",
        default=True,
        help="Generate changelog (default: True)",
    )

    args = parser.parse_args()
    main(args.directory, args.target_file, args.generate_changelog)