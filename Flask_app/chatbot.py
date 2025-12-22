# from pymongo import MongoClient
# from datetime import datetime
#
# client = MongoClient("mongodb://localhost:27017/")
# db = client["ai_chatbot"]
# collection = db["chats"]
#
# user_id = "user_001"
#
# print("Chatbot started. Type 'exit' to stop.")
#
# while True:
#     user_msg = input("You: ")
#     if user_msg.lower() == "exit":
#         print("Chat ended.")
#         break
#
#     collection.insert_one({
#         "user_id": user_id,
#         "role": "user",
#         "message": user_msg,
#         "timestamp": datetime.now()
#     })
#
#     bot_msg = "You said: " + user_msg
#     print("Bot:", bot_msg)
#
#     collection.insert_one({
#         "user_id": user_id,
#         "role": "bot",
#         "message": bot_msg,
#         "timestamp": datetime.now()
#     })

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



