import os
import glob
import json
import csv
from utils.config import read_config
import logging
import re
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the configuration
config = read_config()

project_dir = config['project_dir']
authorization = config['authorization']
openai_model = config['openai-model']
requests = config['requests']


def collecting_data_excel(project_dir, req, data):
    # Write output to Excel file
    output_dir = os.path.join(project_dir, req['dist_dir'])
    output_extension = '.xlsx'
    output_file = os.path.join(output_dir, req['collecting_data_output'] + output_extension)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)
    logging.info(f"Wrote {len(data)} rows of output data to file: {output_file}")


def collecting_data_csv(project_dir, req, data):

    # Write output to CSV file
    output_dir = os.path.join(project_dir, req['dist_dir'])
    output_extension = '.csv'
    output_file = os.path.join(output_dir, req['collecting_data_output'] + output_extension)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    logging.info(f"Wrote {len(data)} rows of output data to file: {output_file}")


# Define function to extract JSON data from file content
def extract_json(file_content):
    # Search for JSON data within file content
    json_pattern = re.compile(r'{.*?}', re.DOTALL)
    json_match = json_pattern.search(file_content)
    if not json_match:
        # JSON data not found or is invalid, return None
        return None
    else:
        # Parse JSON data and return as object
        return json.loads(json_match.group())


# Loop through each request in the config
for req in requests:
    # Get files to be analyzed
    input_dir = os.path.join(project_dir, req['dist_dir'])
    files = glob.glob(os.path.join(input_dir, '**', '*' + req['output_extension']), recursive=True)
    logging.info(f"Found {len(files)} files to analyze in {input_dir}")

    # Loop through each file and analyze data
    data = []
    for file in files:
        with open(file) as f:
            logging.info(f"Analyzing data in file: {file}")
            file_content = f.read()

            # Extract JSON data from file content
            json_obj = extract_json(file_content)
            if json_obj is None:
                # JSON data not found or is invalid, add error to data list
                data.append({
                    'file': file,
                    'error': 'JSON data not found or is invalid'
                })
                logging.warning(f"JSON data not found or is invalid in file: {file}")
            else:
                # Add to data list
                data.append(json_obj)
                logging.info(f"Successfully analyzed JSON data in file: {file}")

    collecting_data_excel(project_dir, req, data)
    collecting_data_csv(project_dir, req, data)
