
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["ai_chatbot"]
collection = db["texts"]

print("Type something. Type 'exit' to stop.")

while True:
    text = input("Enter text: ")

    if text.lower() == "exit":
        print("Stopped.")
        break

    collection.insert_one({
        "message": text,
        "timestamp": datetime.now()
    })

    print("Saved to database.")



