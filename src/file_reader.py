import os
from datetime import datetime
import magic
from celeryconfig import app

def extract_metadata(file_path):
    # Extract file metadata using python-magic
    mime_type = magic.from_file(file_path, mime=True)
    size = os.path.getsize(file_path)
    return {
        'filename': os.path.basename(file_path),
        'mime_type': mime_type,
        'size': size,
        'timestamp': datetime.now().isoformat()
    }

def read_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            metadata = extract_metadata(file_path)
            app.send_task('process_file', args=[file_path], kwargs={'metadata': metadata})

if __name__ == '__main__':
    directory = './files'  # Update with your directory path
    read_directory(directory)