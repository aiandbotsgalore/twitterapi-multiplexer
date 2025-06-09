from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
BASE_URL = "https://twitter241.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "twitter241.p.rapidapi.com"
}

def search_twitter(params):
    query = params.get("query")
    type_ = params.get("type", "Top")
    count = params.get("count", "10")

    if not query:
        return jsonify({"error": "Missing 'query' in params"}), 400

    response = requests.get(f"{BASE_URL}/search", headers=HEADERS, params={
        "query": query,
        "type": type_,
        "count": count
    })
    return jsonify(response.json())

def get_user_by_username(params):
    username = params.get("username")
    if not username:
        return jsonify({"error": "Missing 'username' in params"}), 400

    response = requests.get(f"{BASE_URL}/user", headers=HEADERS, params={
        "username": username
    })
    return jsonify(response.json())

def get_tweet_details(params):
    tweet_id = params.get("tweet_id")
    if not tweet_id:
        return jsonify({"error": "Missing 'tweet_id' in params"}), 400

    response = requests.get(f"{BASE_URL}/tweet", headers=HEADERS, params={
        "tweet_id": tweet_id
    })
    return jsonify(response.json())

def get_user_tweets(params):
    user_id = params.get("user_id")
    count = params.get("count", "10")
    if not user_id:
        return jsonify({"error": "Missing 'user_id' in params"}), 400

    response = requests.get(f"{BASE_URL}/user-tweets", headers=HEADERS, params={
        "user": user_id,
        "count": count
    })
    return jsonify(response.json())

@app.route("/twitter", methods=["POST"])
def twitter_router():
    data = request.get_json()
    if not data or "action" not in data or "params" not in data:
        return jsonify({"error": "Request must contain 'action' and 'params'"}), 400

    action = data["action"]
    params = data["params"]

    if action == "search_twitter":
        return search_twitter(params)
    elif action == "get_user_by_username":
        return get_user_by_username(params)
    elif action == "get_tweet_details":
        return get_tweet_details(params)
    elif action == "get_user_tweets":
        return get_user_tweets(params)
    else:
        return jsonify({"error": f"Unsupported action '{action}'"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
