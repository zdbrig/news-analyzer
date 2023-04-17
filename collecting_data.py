import os
import glob
import json
import csv
from utils.config import read_config
import logging
import re
import pandas as pd
from pandas import json_normalize

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the configuration
config = read_config()

project_dir = config['project_dir']
requests = config['requests']


def collecting_data_excel(project_dir, req, data):
    # Write output to Excel file
    output_dir = os.path.join(project_dir, req['dist_dir'])
    output_extension = '.xlsx'
    output_file = os.path.join(output_dir, req['collecting_data_output'] + output_extension)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df = pd.concat([pd.DataFrame(json_normalize(sublist)) for sublist in data], ignore_index=True)
    df.to_excel(output_file, index=False)
    logging.info(f"Wrote {len(data)} rows of output data to file: {output_file}")


def collecting_data_csv(project_dir, req, data):
    # Write output to CSV file
    output_dir = os.path.join(project_dir, req['dist_dir'])
    output_extension = '.csv'
    output_file = os.path.join(output_dir, req['collecting_data_output'] + output_extension)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0][0].keys() if data and isinstance(data[0], list) else data[0].keys())
        writer.writeheader()
        for row in data:
            if isinstance(row, list):
                for r in row:
                    writer.writerow(r)
            else:
                writer.writerow(row)
    logging.info(f"Wrote {len(data)} rows of output data to file: {output_file}")


# Additional function to flatten nested dictionaries
def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Define function to extract JSON data from file content
def extract_json(file_content):
    # Search for all JSON objects within file content
    json_pattern = re.compile(r'{.*?}', re.DOTALL)
    json_matches = json_pattern.findall(file_content)

    if not json_matches:
        # JSON data not found or is invalid, return None
        return None
    else:
        # Parse each JSON object and return as list of objects
        json_objects = []
        for json_str in json_matches:
            try:
                json_obj = json.loads(json_str)
                flattened_obj = flatten_dict(json_obj)
                json_objects.append(flattened_obj)
            except json.JSONDecodeError:
                logging.warning(f"Invalid JSON object found in file: {json_str}")

        return json_objects


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
                # JSON data not found or is invalid
                logging.warning(f"JSON data not found or is invalid in file: {file}")
            else:
                # Add to data list
                data.append(json_obj)
                logging.info(f"Successfully analyzed JSON data in file: {file}")

    collecting_data_excel(project_dir, req, data)
    collecting_data_csv(project_dir, req, data)
