import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
DATA_FILE = "codes.json"

def load_codes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try: return json.load(f)
            except: return []
    return []

@app.route('/check', methods=['GET'])
def check_code():
    code = request.args.get('code')
    codes = load_codes()
    if code in codes:
        return jsonify({"valid": True})
    return jsonify({"valid": False})

if __name__ == "__main__":
    # Render сам выдает порт через переменную окружения
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
