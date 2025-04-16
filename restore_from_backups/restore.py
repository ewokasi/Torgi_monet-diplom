from dotenv import load_dotenv
import pymongo
import argparse
import os
import json 

load_dotenv()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="MongoDB Backup Script")
parser.add_argument(
    "--mongo_uri", 
    type=str, 
    required=False, 
    help="MongoDB URI", 
    default=os.getenv("MONGO_URI")
)
parser.add_argument(
    "--db_name", 
    type=str, 
    required=False, 
    help="MongoDB Database Name", 
    default=os.getenv("DB_NAME")
)

parser.add_argument(
    "--file_path", 
    type=str, 
    required=False, 
    help="relative path to json", 
    default= "backup_Torgi_Monet_20250212_151905.json"
)



args = parser.parse_args()

client = pymongo.MongoClient(args.mongo_uri)
db = client[args.db_name]

def restore():
    
    with open(args.file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    
    for collection in data:
        db[collection["collection_name"]].insert_many(collection["documents"])
        print(collection["collection_name"])
        
if __name__=="__main__":
    restore()