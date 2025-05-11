from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)
SECRET_KEY = "server_secret_key_123"  # Keep this secret and same as client

def hash_balance(balance):
    return hashlib.sha256(f"{balance}{SECRET_KEY}".encode()).hexdigest()

@app.route("/verify", methods=["POST"])
def verify():
    data = request.json
    balance = data.get("balance")
    client_hash = data.get("hash")

    if balance is None or client_hash is None:
        return jsonify({"valid": False, "error": "Missing data"}), 400

    server_hash = hash_balance(str(balance))
    valid = (client_hash == server_hash)
    return jsonify({"valid": valid})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
