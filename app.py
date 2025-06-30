import os
import requests
from flask import Flask, request, jsonify


app = Flask(__name__)


# 🔑 API-Key सुरक्षित तरीक़े से OS Environment से लो
LANGSEARCH_API_KEY = os.getenv("LANGSEARCH_API_KEY")

# 🌐 LangSearch endpoint
LANGSEARCH_URL = "https://api.langsearch.com/v1/web-search"

@app.route('/')
def home():
    return "🚀 LangSearch Flask API चल रही है!"

@app.route('/search', methods=['POST'])
def search():
    body = request.get_json(silent=True) or {}
    query = body.get("query", "").strip()
    count = int(body.get("count", 5))

    if not LANGSEARCH_API_KEY:
        return jsonify({"error": "Server में LANGSEARCH_API_KEY नहीं मिली"}), 500
    if not query:
        return jsonify({"error": "query चाहिए"}), 400

    headers = {
        "Authorization": f"Bearer {LANGSEARCH_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "freshness": "oneMonth",
        "summary": True,
        "count": count
    }

    res = requests.post(LANGSEARCH_URL, json=payload, headers=headers)
    if res.status_code == 200:
        return jsonify(res.json())
    return jsonify({"error": "LangSearch API fail", "status": res.status_code, "msg": res.text}), res.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
