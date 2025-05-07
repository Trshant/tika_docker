from tika import parser
from extract_time import extract_dates


def extract_text_and_dates(file_path):
    """
    Extracts text and metadata (including dates) from a file using Apache Tika.

    Args:
        file_path (str): The path to the input file.

    Returns:
        tuple: A tuple containing the extracted text (str) and
               the extracted metadata (dict). Returns (None, None)
               if extraction fails.
    """
    try:
        parsed = parser.from_file(file_path)
        text = parsed["content"]
        metadata = parsed["metadata"]
        dates_extracted = extract_dates(text)
        metadata["dates_extracted"] = dates_extracted
        return text, metadata
    except Exception as e:
        print(f"Error extracting data from {file_path}: {e}")
        return None, None


if __name__ == "__main__":
    # Example usage:
    # Replace 'your_file_path_here.pdf' with the actual path to your file
    file_to_process = (
        "/home/trshantbhat/Documents/tika/src/files/sample.eml"  # Or .docx, .txt, etc.
    )

    extracted_text, extracted_metadata = extract_text_and_dates(file_to_process)

    if extracted_text is not None:
        print("--- Extracted Text ---")
        print(extracted_text)

        print("\n--- Extracted Metadata ---")
        import json

        print(json.dumps(extracted_metadata, indent=2))

        # You can access potential date fields from the metadata dictionary
        # Common date fields include 'Creation-Date', 'Last-Modified', etc.
        print("\n--- Potential Dates in Metadata ---")
        for key, value in extracted_metadata.items():
            if "date" in key.lower():
                print(f"{key}: {value}")
