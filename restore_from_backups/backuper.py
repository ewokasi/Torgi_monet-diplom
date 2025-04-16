import os
import json
import hashlib
import datetime
import pymongo
import argparse
from pathlib import Path
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Define file for storing the last backup hash
LAST_BACKUP_HASH_FILE = "last_backup_hash.txt"

# Load last backup hash from file (if exists)
def load_last_backup_hash():
    if Path(LAST_BACKUP_HASH_FILE).exists():
        with open(LAST_BACKUP_HASH_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

# Save current backup hash to file
def save_current_backup_hash(current_hash):
    with open(LAST_BACKUP_HASH_FILE, "w", encoding="utf-8") as f:
        f.write(current_hash)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="MongoDB Backup Script")
parser.add_argument(
    "--mongo_uri", 
    type=str, 
    required=False, 
    help="MongoDB URI", 
    default=os.getenv("MONGO_URI", "mongodb://localhost:27017/")
)
parser.add_argument(
    "--db_name", 
    type=str, 
    required=False, 
    help="MongoDB Database Name", 
    default=os.getenv("DB_NAME", "your_database")
)
args = parser.parse_args()

# Connect to MongoDB
client = pymongo.MongoClient(args.mongo_uri)
db = client[args.db_name]

# Function to calculate hash of JSON data with datetime handling
def calculate_hash(data):
    # Define a custom serializer for datetime objects
    def default_serializer(obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()  # Convert datetime to ISO format string
        raise TypeError(f"Type {type(obj)} not serializable")

    data_str = json.dumps(data, sort_keys=True, default=default_serializer)
    return hashlib.sha256(data_str.encode()).hexdigest()

# Check for changes: calculate the hash of the entire database
def calculate_database_hash():
    db_hash = ""
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        documents = list(collection.find({}, {"_id": 0}))  # Extract data without _id

        if documents:
            # Calculate hash of the collection's current data
            collection_hash = calculate_hash(documents)
            db_hash += collection_hash
    return hashlib.sha256(db_hash.encode()).hexdigest()

# Perform backup if there are changes
def perform_backup():
    print("Checking for database changes...")

    # Load last backup hash and calculate the current hash
    last_backup_hash = load_last_backup_hash()
    current_hash = calculate_database_hash()

    if last_backup_hash != current_hash:
        # Create a backup if changes are detected
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backup_{args.db_name}_{timestamp}.json"
        
        all_data = []
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            documents = list(collection.find({}, {"_id": 0}))  # Extract data without _id
            if documents:
                all_data.append({"collection_name": collection_name, "documents": documents})

        data_str = json.dumps(all_data, ensure_ascii=False, default=str)

        # Save the backup to a file
        with open(backup_file, "w", encoding="utf-8") as f:
            f.write(data_str)

        print(f"Backup created for database {args.db_name}: {backup_file}")
        
        # Save the current hash to the file for future comparison
        save_current_backup_hash(current_hash)
    else:
        print("No changes detected, backup not needed.")

# Run the backup once a day
while True:
    perform_backup()
    print("Waiting for the next backup in 24 hours...")
    time.sleep(86400)  # Sleep for 24 hours (86400 seconds)
