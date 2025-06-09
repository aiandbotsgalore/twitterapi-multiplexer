from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
BASE_URL = "https://twitter241.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "twitter241.p.rapidapi.com"
}

@app.route("/twitter", methods=["POST"])
def twitter_api_proxy():
    data = request.json
    action = data.get("action")
    params = data.get("params", {})

    if not action:
        return jsonify({"error": "Missing 'action' field"}), 400

    endpoint_map = {
        "search_twitter": "/search-v2",  # updated from /search to /search-v2 per your recent usage
        "get_tweet_details": "/gettweetdetails",
        "get_user_by_username": "/getuserdetails",
        "get_user_tweets": "/getusertweets"
    }

    endpoint = endpoint_map.get(action)
    if not endpoint:
        return jsonify({"error": f"Unsupported action: {action}"}), 400

    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, params=params)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
