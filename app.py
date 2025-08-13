from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OPENAI_API_KEY = "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"

def generate_ai_response(prompt: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.7,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        res_json = response.json()
        return res_json["choices"][0]["message"]["content"].strip()
    else:
        return "❌ عذرًا، حدث خطأ في التواصل مع خدمة الذكاء الاصطناعي."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    if question.strip() == "":
        return jsonify({"answer": "يرجى إدخال سؤال."})
    answer = generate_ai_response(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)