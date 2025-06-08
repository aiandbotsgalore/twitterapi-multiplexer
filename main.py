
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

@app.route("/twittersearch", methods=["POST"])
def search_twitter():
    data = request.json
    query = data.get("query")
    if not query:
        return jsonify({"error": "Query parameter missing"}), 400
    response = requests.get(f"{BASE_URL}/search", headers=HEADERS, params={"q": query})
    return jsonify(response.json())

@app.route("/getuserdetails", methods=["POST"])
def get_user_details():
    data = request.json
    username = data.get("username")
    if not username:
        return jsonify({"error": "Username parameter missing"}), 400
    response = requests.get(f"{BASE_URL}/getuserdetails", headers=HEADERS, params={"username": username})
    return jsonify(response.json())

@app.route("/gettweetdetails", methods=["POST"])
def get_tweet_details():
    data = request.json
    tweet_id = data.get("tweet_id")
    if not tweet_id:
        return jsonify({"error": "Tweet ID parameter missing"}), 400
    response = requests.get(f"{BASE_URL}/gettweetdetails", headers=HEADERS, params={"tweet_id": tweet_id})
    return jsonify(response.json())

@app.route("/getusertweets", methods=["POST"])
def get_user_tweets():
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID parameter missing"}), 400
    response = requests.get(f"{BASE_URL}/getusertweets", headers=HEADERS, params={"user_id": user_id})
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
