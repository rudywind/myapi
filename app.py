from flask import Flask, jsonify, request
import cloudscraper
import os

app = Flask(__name__)
scraper = cloudscraper.create_scraper()
API_KEY = "6e820ce645f4988dc5ec802984bba446dc1668c7"
API_BASE = "https://api.mydramalist.com/v1"

AVAILABLE_ENDPOINTS = {
    "/titles/<mdl_id>": "Get main info for title",
    "/titles/<mdl_id>/credits": "Get cast/crew info for title",
    "/titles/<mdl_id>/related": "Get related titles",
    "/people/<mdl_id>": "Get info about a person",
    "/people/<mdl_id>/credits": "Get filmography for a person"
}

@app.route("/")
def index():
    return jsonify({
        "message": "Welcome to MyDramaList Proxy API via Cloudscraper",
        "usage": "Append one of the available endpoints to the base URL",
        "available_endpoints": AVAILABLE_ENDPOINTS,
        "example": request.host_url + "titles/12345"
    })

@app.route("/titles/<mdl_id>")
def get_title(mdl_id):
    return fetch_api(f"/titles/{mdl_id}")

@app.route("/titles/<mdl_id>/credits")
def get_title_credits(mdl_id):
    return fetch_api(f"/titles/{mdl_id}/credits")

@app.route("/titles/<mdl_id>/related")
def get_title_related(mdl_id):
    return fetch_api(f"/titles/{mdl_id}/related")

@app.route("/people/<mdl_id>")
def get_person(mdl_id):
    return fetch_api(f"/people/{mdl_id}")

@app.route("/people/<mdl_id>/credits")
def get_person_credits(mdl_id):
    return fetch_api(f"/people/{mdl_id}/credits")

def fetch_api(path):
    try:
        url = API_BASE + path
        headers = {
            "Content-Type": "application/json",
            "mdl-api-key": API_KEY
        }
        r = scraper.get(url, headers=headers)
        r.raise_for_status()
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e), "path": path}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
