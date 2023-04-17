from utils.file_handling import write_file_content
from utils.request_handling import make_request, extract_content
import logging  # Import the logging module
import os

def process_filtered_file(escaped_content, file_path, output_dir, directory_to_analyze , request):
    response = make_request(escaped_content ,  request)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful
    extracted_content = extract_content(response)

    # Determine the relative path of the input file
    relative_path = os.path.relpath(file_path, directory_to_analyze)

    # Create the output subdirectory path
    output_subdir = os.path.join(output_dir, os.path.dirname(relative_path))

    # Create the output subdirectory if it doesn't exist
    if not os.path.exists(output_subdir):
        os.makedirs(output_subdir)

    # Save the analyzed file to the output subdirectory
    output_file_path = os.path.join(output_subdir, os.path.basename(file_path))
    write_file_content(output_file_path, extracted_content , request)

    logging.info(f"Processed file: {file_path}")  # Log the processed file
