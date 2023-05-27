# Google Keep to Obsidian Markdown Converter for Windows

This script is for Windows users who want to convert their Google Keep notes (exported in JSON format) into Markdown (.md) files, suitable for use in Obsidian. Importantly, the script preserves the original timestamps from Google Keep notes.

Please note that this script only converts text content and labels from Google Keep notes. Attachments such as images and audio files are not converted.

## How the Script Works

### Handling of Labels

In Google Keep, notes can have labels associated with them. This script converts these labels into hashtags at the end of the Markdown file.

For example, if a Google Keep note has labels "work" and "meeting", these would appear at the end of the Markdown note like this:

#work #programming

### Handling of Text Content

The main text content of the Google Keep note is preserved as the main body of the Markdown file.

### Handling of Titles

If a Google Keep note has a title, the script uses this title (with any invalid filename characters removed) as the filename for the Markdown file. If the title is absent or too long, the script uses the first few characters of the note's content as the filename.

## How to use this script

### Step 1: Export Google Keep data using Google Takeout

First, you need to download your Google Keep data:

1. Visit Google Takeout: https://takeout.google.com/.
2. Deselect all data types and then select only "Google Keep".
3. Choose the file type (`.zip`) and delivery method according to your preference, and click "Create export".
4. Once the export is ready, download the zip file and extract it.

### Step 2: Separate JSON files

Your Google Keep export will contain both JSON and HTML files. You need to extract only the JSON files:

1. Navigate to the extracted folder containing your Google Keep export.
2. Use the search functionality in Windows and search for `.json`.
3. Select all the `.json` files that appear and move them to a new folder. This is your JSON input folder.

### Step 3: Install Python dependencies

You need Python 3 and the `pywin32` module installed. To install `pywin32`, you can use the following command:

```sh
pip install pywin32
```

### Step 4: Configure the script

In the script, you need to set the following variables:

input_folder: The path to the folder containing your .json files.
output_folder: The path to the folder where you want to send the converted Markdown files.

### Step 5: Run the script
Now, you can run the script. Open PowerShell or Command Prompt, navigate to the directory containing the script, and run:

```sh
python gk-to-obs.py
```

Your Markdown files will be created in the output directory you specified, each with a filename based on the note's title or content, and with preserved creation and modification timestamps.
