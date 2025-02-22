
from flask import Flask, request, jsonify
import subprocess
import json
import re

app = Flask(__name__)

def get_instagram_data(instagram_url):
    try:
        result = subprocess.run(
            ["yt-dlp", "-j", instagram_url],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout.strip())
            download_url = data.get("url")
            thumbnail = data.get("thumbnail")
            description = data.get("description")
            return {
                "download_url": download_url,
                "thumbnail": thumbnail,
                "description": description
            }
        else:
            return None
    except Exception as e:
        print("Error:", str(e))
        return None

@app.route('/')
def d():
     return "api running"
def download():
    instagram_url = request.args.get('url')
    if not instagram_url:
        return jsonify({"error": "No URL provided"}), 400

    if not re.match(r'^https:\/\/(www\.)?instagram\.com\/', instagram_url):
        return jsonify({"error": "Invalid Instagram URL"}), 400

    data = get_instagram_data(instagram_url)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
