"""
This script processes all .txt and .md files in the current directory,
correcting their grammar and spelling using LanguageTool.
"""

import os
import sys
import language_tool_python

# Initialize the tool
tool = language_tool_python.LanguageTool("en-CA")


def clean_text_file(file_path):
    """Cleans text files by correcting grammar and spelling errors using LanguageTool."""
    # Iterate over all .txt files
    for file in os.listdir(file_path):
        if (
            (file.endswith(".txt") or file.endswith(".md"))
            and not file.endswith("_corrected.txt")
            and not file.endswith("_corrected.md")
        ):
            full_path = os.path.join(file_path, file)
            print(f"Processing {full_path}...")

            try:
                # Read the content of the file
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check for errors
                matches = tool.check(content)
                if matches:
                    print(f"Correcting {len(matches)} issues in {file}...")

                    # Correct the content
                    corrected_content = tool.correct(content)

                    # Write the corrected content back to the file
                    corrected_path = full_path.replace(
                        ".txt", "_corrected.txt"
                    ).replace(".md", "_corrected.md")
                    with open(corrected_path, "w", encoding="utf-8") as f:
                        f.write(corrected_content)
                    print(f"Corrected {file} and saved changes.\n")
                else:
                    print(f"No issues found in {file}.\n")
            except (
                FileNotFoundError,
                PermissionError,
                UnicodeDecodeError,
                OSError,
            ) as e:
                print(f"Error processing {file}: {e}")
                print(f"Skipping {file} and continuing to next file.\n")
                continue
            except Exception as e:
                print(f"Unexpected error processing {file}: {e}")
                print(f"Skipping {file} and continuing to next file.\n")
                continue


if __name__ == "__main__":
    clean_text_file(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
