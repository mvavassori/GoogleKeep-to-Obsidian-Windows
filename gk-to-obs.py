#Script to convert Google Keep JSON to Obsidian Markdown Notes on Windows maintaining created at and updated at timestamps

import pywintypes, win32file, win32con
import json
import os
import re
import string

#! Change this!
# The folder containing all your json google keep notes
input_folder = r"C:\Users\username\Desktop\GoogleKeep-json-Notes"
# The folder where you want to save your Obsidian Markdown notes
output_folder = r"C:\Users\useername\Desktop\Output-md-Notes"

def sanitize_filename(filename):
    # Remove or replace invalid characters in the filename
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized_filename = "".join(c if c in valid_chars else " " for c in filename)
    sanitized_filename = re.sub(r"\s+", " ", sanitized_filename) # Replace consecutive whitespace with single space
    sanitized_filename = sanitized_filename.strip() # Remove leading/trailing spaces
    return sanitized_filename

def set_file_time(fname, creation_time, modified_time):
    creation_time = pywintypes.Time(creation_time/1000000)
    modified_time = pywintypes.Time(modified_time/1000000)
    winfile = win32file.CreateFile(
        fname, win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None, win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL, None)
    win32file.SetFileTime(winfile, creation_time, None, modified_time)
    winfile.close()

def convert_keep_to_markdown(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    title = data.get("title", "")
    text_content = data.get("textContent", "")
    created_timestamp = data.get("createdTimestampUsec", 0)
    updated_timestamp = data.get("userEditedTimestampUsec", 0)

    # Check if "labels" field exists and is a list
    if "labels" in data and isinstance(data["labels"], list):
        labels = data["labels"]
        tags = " ".join(["#" + label["name"] for label in labels])
    else:
        labels = []
        tags = ""

    # Prepare the Markdown content
    markdown_content = text_content
    if tags:
        markdown_content += f"\n\n{tags}"

    # Generate a unique filename if the title is empty or too long
    if not title.strip() or len(title) > 260:
        base_filename = text_content[:10]
    else:
        base_filename = title

    # Sanitize the base filename
    sanitized_base_filename = sanitize_filename(base_filename)

    # Generate a unique filename by adding a numeric suffix
    suffix = 1
    filename = f"{sanitized_base_filename}.md"
    while os.path.exists(os.path.join(output_folder, filename)):
        filename = f"{sanitized_base_filename}_{suffix}.md"
        suffix += 1

    output_filepath = os.path.join(output_folder, filename)

    with open(output_filepath, "w", encoding="utf-8") as output_file:
        output_file.write(markdown_content)

    # Set the file creation and modification timestamps
    set_file_time(output_filepath, created_timestamp, updated_timestamp)

# Process all JSON files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        json_file = os.path.join(input_folder, filename)
        convert_keep_to_markdown(json_file)
