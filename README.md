# PlexSorter

**PlexSorter** is a Python script that organizes messy media folders into a Plex-compatible folder structure. It can automatically identify movies and TV shows, rename files, and place them in structured folders, making it easy to integrate with Plex Media Server.

---

## Features

- Detects and organizes TV shows and movies based on file names.
- Creates Plex-compatible folder structures:
  - **Movies**: `Movies/<Movie Title> (<Year>)`
  - **TV Shows**: `TV Shows/<Show Name>/Season xx/<Show Name> - SxxEyy - <Episode Title>.ext`
- Uses OpenAI to intelligently suggest file names and structures.

---

## Installation

### 1. Clone the Repository

 `git clone https://github.com/robzilla1738/plexsorter.git`
  `cd plexsorter`

### 2. Install Dependencies

  `pip install -r requirements.txt`

### 3. Set Up Your API Key

Create a .env file in the project directory and add your OpenAI API key:

  `echo "OPENAI_API_KEY=your_openai_api_key_here" > .env`

## Usage

1. Open the plexsorter.py file.
2. Update the source_directories and destination_root variables with the paths to your source and destination folders:

  `source_directories = ["path/to/source1", "path/to/source2"]`
  `destination_root = "path/to/destination"`

3. Run the script:

  `python3 plexsorter.py`

The script will scan your source directories, identify media files, and organize them into the destination directory.

## Example: Before and After

### Before Organization
<img width="767" alt="Screenshot 2024-12-13 at 11 41 47 AM" src="https://github.com/user-attachments/assets/190703b1-2d04-4143-8e3b-03ab6dfae061" />


### After Organization
<img width="768" alt="Screenshot 2024-12-13 at 11 42 17 AM" src="https://github.com/user-attachments/assets/6ae220fd-6824-403c-8ac7-8b83bc635510" />



## Requirements

Python 3.7 or higher
OpenAI API Key

## Dependencies

python-dotenv: For managing environment variables.
openai: To interact with OpenAI's GPT API.

## Contribution
Contributions are welcome! Feel free to fork this repository, create a feature branch, and submit a pull request.
