import os
import shutil
import re
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found. Make sure to set OPENAI_API_KEY in your .env file.")

client = OpenAI(api_key=api_key)

def scan_folder(directory):
    print(f"Scanning directory: {directory}")
    media_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.startswith("._"):
                continue  # Skip macOS hidden files
            if file.endswith(('.mp4', '.mkv', '.avi', '.srt')):
                file_path = os.path.join(root, file)
                media_type = "TV" if re.search(r'[Ss]\d{2}[Ee]\d{2}', file) else "Movie"
                media_files.append({"path": file_path, "type": media_type})
    return media_files

def get_standardized_name(file_name, media_type):
    if media_type == "TV":
        prompt = f"""
        Rename the following TV show file for Plex Media Server:
        '{file_name}'
        Provide:
        - New file name: <New Name>
        - Folder structure: <Folder Path>
        Use the format: TV Shows/<Show Name>/Season xx/<Show Name> - SxxEyy - <Episode Title>.ext
        """
    else:
        prompt = f"""
        Rename the following movie file for Plex Media Server:
        '{file_name}'
        Provide:
        - New file name: <New Name>
        - Folder structure: Movies/<Movie Title> (<Year>)
        """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that organizes media files for Plex."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def rename_and_organize(file_path, ai_response, destination_root):
    try:
        lines = ai_response.splitlines()
        new_file_name = None
        folder_structure = None
        for line in lines:
            line = line.strip().lstrip('-').strip()
            if line.lower().startswith("new file name:"):
                new_file_name = line.split(": ", 1)[1].strip()
            elif line.lower().startswith("folder structure:"):
                folder_structure = line.split(": ", 1)[1].strip()

        if not new_file_name or not folder_structure:
            print(f"Failed to process AI response for {file_path}")
            return

        movie_folder = os.path.join(destination_root, folder_structure)
        os.makedirs(movie_folder, exist_ok=True)
        new_file_path = os.path.join(movie_folder, new_file_name)
        shutil.move(file_path, new_file_path)
        print(f"Moved: {file_path} -> {new_file_path}")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

def process_media_files(source_directories, destination_root):
    for directory in source_directories:
        print(f"Scanning root directory: {directory}")
        media_files = scan_folder(directory)
        print(f"Found {len(media_files)} media files to process in {directory}.")
        for media in media_files:
            file_path = media["path"]
            media_type = media["type"]
            file_name = os.path.basename(file_path)
            print(f"Processing: {file_name} ({media_type})")
            try:
                ai_response = get_standardized_name(file_name, media_type)
                print(f"AI Response:\n{ai_response}")
                rename_and_organize(file_path, ai_response, destination_root)
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

if __name__ == "__main__":
    source_directories = ["path/to/source1", "path/to/source2"]
    destination_root = "path/to/destination"
    process_media_files(source_directories, destination_root)
