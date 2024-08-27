import os
import shutil
import subprocess
import mimetypes

# File type handling dictionary
file_types = {
    'pdf': 'application/pdf',
    'video': ['video/mp4', 'video/avi', 'video/mkv'],
    'audio': ['audio/mp3', 'audio/wav', 'audio/ogg'],
    'executable': ['application/exe', 'application/msi']
}

def split_file(file_path, location1, location2):
    # Split file into chunks
    chunk_size = 1024 * 1024 * int(input("Enter Chunk-size in MB:"))  # Calculates Chunk-size in MB
    file_size = os.path.getsize(file_path)
    num_chunks = (file_size // chunk_size) + (1 if file_size % chunk_size else 0)

    with open(file_path, 'rb') as file:
        for i in range(num_chunks):
            chunk = file.read(chunk_size)
            chunk_path = os.path.join(location1 if i % 2 == 0 else location2, f'chunk{i}')
            with open(chunk_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
    return num_chunks

def create_loader_script(file_path, location1, location2, num_chunks):
    loader_script = f"""
import os
import mimetypes
import subprocess

file_path = r'{file_path}'
location1 = r'{location1}'
location2 = r'{location2}'
num_chunks = {num_chunks}

reassembled_path = file_path

# Combine chunks
with open(reassembled_path, 'wb') as f:
    for i in range(num_chunks):
        chunk_path = os.path.join(location1 if i % 2 == 0 else location2, f'chunk{{i}}')
        with open(chunk_path, 'rb') as c:
            f.write(c.read())

# Run original file
file_type, _ = mimetypes.guess_type(reassembled_path)
if file_type == 'application/pdf':
    os.startfile(reassembled_path)
elif file_type and file_type.startswith('video/'):
    os.startfile(reassembled_path)
elif file_type and file_type.startswith('audio/'):
    os.startfile(reassembled_path)
else:
    subprocess.run([reassembled_path])
"""
    loader_script_path = os.path.splitext(file_path)[0] + '_loader.py'
    with open(loader_script_path, 'w') as f:
        f.write(loader_script)
    print(f"Loader script created at: {loader_script_path}")

def create_library(file_path, location1, location2):
    library_entry = {
        'file_path': file_path,
        'location1': location1,
        'location2': location2
    }
    with open('library.txt', 'a') as f:
        f.write(str(library_entry) + '\n')

def install_wizard_split(file_path, location1, location2):
    num_chunks = split_file(file_path, location1, location2)
    create_loader_script(file_path, location1, location2, num_chunks)
    create_library(file_path, location1, location2)

def main():
    print("File Splitter and Installer")
    print("1. Split file")
    print("2. Install and split")
    choice = input("Enter choice: ")

    if choice == '1':
        file_type = input("Enter file type (pdf, video, audio, executable): ")
        file_path = input("Enter file path: ")
        location1 = input("Enter location 1: ")
        location2 = input("Enter location 2: ")

        if file_type in file_types:
            num_chunks = split_file(file_path, location1, location2)
            create_loader_script(file_path, location1, location2, num_chunks)
            create_library(file_path, location1, location2)
        else:
            print("Unsupported file type")

    elif choice == '2':
        file_path = input("Enter file path: ")
        location1 = input("Enter location 1: ")
        location2 = input("Enter location 2: ")
        install_wizard_split(file_path, location1, location2)

if __name__ == '__main__':
    main()
