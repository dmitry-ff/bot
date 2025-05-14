import logging
logging.basicConfig(level=logging.INFO)

def delete_message(event, db):
    try:
        print(event)
    except Exception as e:
        logging.error(f"Error while deleting: {e}")