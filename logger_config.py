import logging

def configure_logger():
    logging.basicConfig(
        level=logging.INFO,  # Set the logging level to INFO
        format="%(asctime)s - %(levelname)s - %(message)s",  # Set the logging format
        handlers=[
            logging.FileHandler("chatgpt_analysis.log"),  # Save logs to a file named chatgpt_analysis.log
            logging.StreamHandler()  # Print logs to the console
        ],
    )
