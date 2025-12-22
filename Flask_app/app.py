from flask import Flask,render_template,request,session
from pymongo import MongoClient
from datetime import datetime
import uuid
from config import JOBS
from google import genai

import json
from google.genai import types
app = Flask(__name__)

# api_key="AIzaSyCKhi_JqRKKdO31vCta8WoVitaYxaNxJy4"
api_key="AIzaSyDshsPBzbqbFobchC_gPvdVOkuWxAvwVpA"

@app.route('/')
def home():
    return render_template("index.html", name="John")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/profile/<username>')
def profile(username):
    return render_template("profile.html", name=username)

@app.route('/jobs',methods=["POST"])
def jobs():
    data=request.json
    print(data)

    company_name = data.get("Company")
    job_title = data.get("title")
    Loc = data.get("location")

    jobs = [job for job in JOBS
            # if job['company'] == company_name
            if job['title'] == job_title
            # if job['location'] == Loc
            ]
    return jobs

@app.route('/submit/job',methods=["POST"])
def submit_job():
    data=request.json
    print(data)
    return {"message":"Success"},200

@app.route('/jobs/create')
def create_job():
    return render_template("forms.html")

@app.route('/ai/prompt/')
def ai_prompt():
    return render_template("index2.html")

@app.route('/api/ai/prompt',methods=["POST"])
def api_ai_prompt():
    try:
        data=request.json
        print(data)
        if not data or "prompt" not in data:
            return {"message":"Key is missing"},400

        client = genai.Client(api_key=api_key)
        prompt=data["prompt"]
        print(prompt)
        response=client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        return {"message":response.text},200

    except Exception as e:
        print(e)
        return {"message":"Error"},500

# @app.route('/ai/chatbot',methods=["GET","POST"])
# def ai_chatbot():
#     if request.method == "POST":
#         try:
#             data=request.json
#             print(data)
#             prompt=data.get("prompt")
#
#             client = genai.Client(api_key=api_key)
#             response = client.models.generate_content(
#                 model="gemini-2.5-flash-lite",
#                 contents=prompt
#             )
#             return {"message":response.text},200
#         except Exception as e:
#             print(e)
#             return {"message":"Error"},500
#
#     return render_template("chat.html")

# ai_chatbot with sessions ..

app.secret_key = "flask_app_v2"     #Authentication (Security)
client = MongoClient("mongodb://localhost:27017/")
database = client["ai_chatbot"]
collection = database["chats"]

@app.route('/ai/chatbot',methods = ["GET","POST"])
def ai_chatbot():
    if 'session_id' not in session:
        session['session_id'] =  str(uuid.uuid4())

    if request.method == "POST":
        try:
            data = request.json
            prompt = data.get("prompt")

            session_id = session['session_id']

            if 'chat_history' not in session:
                session['chat_history'] = []

            session['chat_history'].append({
                "role": "user",
                "parts": [{"text": prompt}]
            })

            print(session['chat_history'])

            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=session["chat_history"]
            )
            bot_response = response.text

            collection.insert_many([
                {
                    "session_id": session_id,
                    "role" :"user",
                    "message" :prompt,
                    "timestamp" : datetime.utcnow()
                },
                {
                    "session_id" : session_id,
                    "role" : "bot",
                    "message" : bot_response,
                    "status" : "success",
                    "timestamp" : datetime.utcnow(),
                }
            ])
            session['chat_history'].append({
                "role": "bot",
                "parts": [{"text": bot_response}]
            })
            session.modified = True
            return {"message":bot_response},200

        except Exception as e:
            print(e)

            session_id = session.get("session_id","unknown")
            collection.insert_many([
                {
                    "session_id": session_id,
                    "role": "user",
                    "message": prompt,
                    "timestamp": datetime.utcnow()
                },
                {
                    "session_id": session_id,
                    "role": "bot",
                    "message": f"An internal error occurred.\n {e}",
                    "status": "error",
                    "timestamp": datetime.utcnow()
                }
            ])
            return {"message":"Error"},500
    return render_template("chat.html")

@app.route('/get_history')
def get_history():
    return {"history":session.get('chat_history',[])}

@app.route('/clear_history',methods=["POST"])
def clear_history():
    session.pop('chat_history',None)

    session.pop('session_id',None)

    # session['session_id'] = str(uuid.uuid4())

    session.modified = True
    return {"message":"History cleared"},200

@app.route('/chats/stats')
def chats_stats():
    #Total Sessions
    total_sessions = len(collection.distinct('session_id'))

    #Total Messages
    total_messages = collection.count_documents({})

    #User messages
    user_messages = collection.count_documents({"role":"user"})

    #Bot responses
    bot_messages = collection.count_documents({"role":"bot"})

    #Total Errors
    total_errors = collection.count_documents({"status":"error"})

    return render_template("stats.html",
                           sessions = total_sessions,
                           messages = total_messages,
                           errors = total_errors,
                           user_count = user_messages,
                           bot_count = bot_messages,
                           )

@app.route('/session/details')
def session_details():
    pipeline = [
        {"$group": {"_id": "$session_id", "message_count": {"$sum": 1}}}
    ]
    sessions_data = list(collection.aggregate(pipeline))
    return render_template("session_details.html",sessions = sessions_data)

@app.route('/error/details')
def error_details():
    errors_data = list(collection.find({"status":"error"}).sort("timestamp",-1))
    return render_template("error_details.html",errors = errors_data)

@app.route('/session/view/<session_id>')
def view_chats(session_id):
    chat_history = list(collection.find({"session_id":session_id}).sort("timestamp",-1))
    return render_template("chat_history.html",session_id = session_id,chat = chat_history)

# ai_job_generator_CHATBOT
client = genai.Client(api_key=api_key)
system_instruction = f"""You are an AI Job Generator. Follow this exact interaction loop:
                 1. the user will give you the Job Title.
                 2. Then ask for the Target Country.
                 3. Wait for user input. Then ask for the Preferred Language.
                 4. Once you have all 3 inputs (Title, Country, Language), generate 1 job .
                 5. Your FINAL response must be strictly a JSON list of objects (keys: title, salary, description).
                 6. Do NOT output JSON for the questions. Only for the final result.
                 """
chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            # response_mime_type="application/json"
        )
    )
# response789 = chat.send_message("")

@app.route('/ai/job/generator', methods=["GET", "POST"])
def ai_job_generator():

    if request.method == "POST":
        try:
            data=request.json
            print(data)
            user_input=data.get("prompt")

            response = chat.send_message(user_input)
            print(f"\nBot: {response.text}")
            return {"message": response.text}, 200

        except Exception as e :
             print(f"Error: {e}")
             return {"message": "Error generating jobs.", "status": "error"}, 500

    return render_template("ai_job_generator.html")

if __name__ == '__main__':
    app.run(debug=True)






































