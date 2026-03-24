from flask import Flask,request,jsonify,render_template
from groq import Groq

app=Flask(__name__)

GROQ_API_KEY="YOUR_API_KEY_HERE"

client=Groq(api_key=GROQ_API_KEY)

with open("knowledge.txt","r",encoding="utf-8") as file:
    knowledge=file.read()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat",methods={'POST'})
def chat():
    user_message=request.json.get("message")

    if user_message.lower() in ["hi","hello","hey"]:
        return jsonify({"reply":"Hello! How can i help you with Emerging Trends in Cloud Computing ?"})
    
    completion=client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful AI assistant. You must answer the user's questions based ONLY on the following knowledge text.\n\nKnowledge:\n{knowledge}\n\nIf the answer to the user's question cannot be found in the knowledge text, you MUST reply EXACTLY with: 'Sorry! I can't help you in this.' Do not include any other text, apologies, or explanations."
            },
            {
                "role": "user",
                "content": user_message
            },
        ]
    )

    bot_reply=completion.choices[0].message.content

    return jsonify({"reply":bot_reply})

if __name__=="__main__":
    app.run(debug=True)