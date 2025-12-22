import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_CONN_STR = os.getenv("DATABASE_CONN_STR")

def migrate_chats():
    try:
        source_client = MongoClient(DATABASE_URL)
        dest_client = MongoClient(DATABASE_CONN_STR)

        source_database = source_client["ai_chatbot"]
        dest_database = dest_client["ai_chatbot"]

        source_collection = source_database["chats"]
        dest_collection = dest_database["chats"]

        chats = source_collection.find()
        all_chats = list(chats)

        if not all_chats:
            print("No data found in source collection.")
            return

        for chat in all_chats:
            chat.pop("_id")

        print(all_chats)

        #Insert into the new database
        dest_collection.insert_many(all_chats)

    except Exception as e:
        print(f"Error:{e}")

if __name__ == "__main__":
    migrate_chats()




