from google import genai
from google.genai import types

# api_key = "AIzaSyCKhi_JqRKKdO31vCta8WoVitaYxaNxJy4"
api_key = "AIzaSyAUAVVI_J7qI1sH9v7hMv253yhe9eTI5m4"
system_instruction= f"""You are an AI Job Generator. Follow this exact interaction loop:
1. Greet the user and ask for the Job Title.
2. Wait for user input. Then ask for the Target Country.
3. Wait for user input. Then ask for the Preferred Language.
4. Once you have all 3 inputs (Title, Country, Language), generate 1 job .
5. Your FINAL response must be strictly a JSON list of objects (keys: title, salary, description). 
6. Do NOT output JSON for the questions. Only for the final result.
"""

def start_chat():
    client = genai.Client(api_key=api_key)

    chat=client.chats.create(
        model = "gemini-2.5-flash-lite",
        config = types.GenerateContentConfig(
            system_instruction = system_instruction
        )
    )
    response = chat.send_message("")
    print(f"\nBot: {response.text}")

    while True:
        user_input = input("You: ")
        response = chat.send_message(user_input)
        print(f"\nBot: {response.text}")

if __name__ == "__main__":
    start_chat()


