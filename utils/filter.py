
import fnmatch
import os
import logging  # Import the logging module
from utils.file_handling import read_file_content
from utils.request_handling import escape_content


def read_request_file(request_file_name):
    with open(request_file_name, "r") as file:
        content = file.read()
    return content

def filter(name, root,  request):
    files_to_be_excluded = request["files_to_be_excluded"]
    file_exclude_patterns = [f_pattern.strip() for f_pattern in files_to_be_excluded.split(",")]
    
    if not any(fnmatch.fnmatch(name, pattern) for pattern in file_exclude_patterns) and not os.path.basename(name) in file_exclude_patterns:
        file_path = os.path.join(root, name)
        if os.path.isfile(file_path):
            content = read_file_content(file_path)
            request_content = read_request_file(request["request"])
            content = request_content + " {}".format(content)
            escaped_content = escape_content(content)
            logging.debug(f"Filtered file: {file_path}")  # Log the filtered file
            return escaped_content, file_path
    else:
        logging.debug(f"Excluded file: {os.path.join(root, name)}")  # Log the excluded file
    return None, None