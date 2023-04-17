import os
import logging
from utils.config import read_config
from utils.file_handling import get_file_list
from utils.filter import filter
from utils.process_filtered_file import process_filtered_file
from logger_config import configure_logger 

# Configure the logger
configure_logger()

# Load the configuration
config = read_config()

# Set the directory to analyze from the configuration
directory_to_analyze = config["project_dir"]

# Loop through all requests in the config
for request in config["requests"]:
    # Set the output directory for the analyzed files
    output_dir = os.path.join(directory_to_analyze, request["dist_dir"])

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Log the output directory
    logging.info(f"Analyzing directory: {directory_to_analyze}")
    logging.info(f"Output directory: {output_dir}")

    # Loop through all files in the directory to analyze, including subdirectories
    for root, dirs, files in get_file_list(directory_to_analyze , request):
        if not files:
            logging.warning(f"No files found in directory: {root}")
        else:
            for name in files:
                escaped_content, file_path = filter(name, root, request)
                if escaped_content:
                    try:
                        process_filtered_file(escaped_content, file_path, output_dir, directory_to_analyze, request)
                    except Exception as e:
                        logging.error(f"An error occurred while processing {file_path}: {e}")  # Log the error

    if not os.listdir(output_dir):
        logging.warning(f"No files were analyzed for request: {request['request']}")