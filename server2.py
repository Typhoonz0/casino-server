from flask import Flask, request, jsonify
import hashlib
import os

app = Flask(__name__)

# Secret key for hashing (must match client)
SECRET = "super_secret_key"

@app.route("/", methods=["GET"])
def index():
    return "✅ Casino server is running."

@app.route("/get_hash", methods=["POST"])
def get_hash():
    try:
        data = request.get_json()
        balance = str(data.get("balance", "0"))
        hash_val = hashlib.sha256((balance + SECRET).encode()).hexdigest()
        return jsonify({"hash": hash_val})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/validate", methods=["POST"])
def validate():
    try:
        data = request.get_json()
        balance = str(data.get("balance", "0"))
        provided_hash = data.get("hash")
        actual_hash = hashlib.sha256((balance + SECRET).encode()).hexdigest()
        return jsonify({"valid": provided_hash == actual_hash})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Render requires this to bind to the correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 locally
    app.run(host="0.0.0.0", port=port)
