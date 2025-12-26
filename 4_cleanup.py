"""
This script processes all .txt and .md files in the current directory,
correcting their grammar and spelling using LanguageTool.
"""

import os
import sys
import language_tool_python

# Log file name
LOG_FILENAME = "cleaned.log"

# Initialize the tool
tool = language_tool_python.LanguageTool("en-CA")


def clean_text_file(file_path):
    """Cleans text files by correcting grammar and spelling errors using LanguageTool."""
    # Path to log file
    log_path = os.path.join(file_path, LOG_FILENAME)
    cleaned_files = set()

    # Load already cleaned files from log
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as log_file:
            cleaned_files = set(line.strip() for line in log_file if line.strip())

    # Loop through all .txt and .md files in the directory
    for file in os.listdir(file_path):
        if (
            (file.endswith(".txt") or file.endswith(".md"))
            and not file.endswith("_corrected.txt")
            and not file.endswith("_corrected.md")
            and file not in cleaned_files
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
                    corrected_path = full_path.replace(".txt", "_corrected.txt").replace(".md", "_corrected.md")
                    with open(corrected_path, "w", encoding="utf-8") as f:
                        f.write(corrected_content)
                    print(f"Corrected {file} and saved changes.\n")
                else:
                    print(f"No issues found in {file}.\n")
                # Mark as cleaned
                with open(log_path, "a", encoding="utf-8") as log_file:
                    log_file.write(file + "\n")
                    log_file.flush()
          
            # Handle specific file read/write errors
            except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as e:
                print(f"Error processing {file}: {e}")
                print(f"Skipping {file} and continuing to next file.\n")
                continue

            # Handle any other unexpected errors
            except Exception as e:
                print(f"Unexpected error processing {file}: {e}")
                print(f"Skipping {file} and continuing to next file.\n")
                continue

if __name__ == "__main__":
    clean_text_file(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
