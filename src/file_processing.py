
from datetime import datetime

from celeryconfig import app
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup

@app.task(name='process_file')
def process_file(file_path, metadata):
    print(f"Task started at {datetime.now()}")
    print(f"File path: {file_path}")
    print("Metadata:")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    # Implement file processing logic here
    pass  # Replace with actual processing code

    print(f"Task completed at {datetime.now()}")
