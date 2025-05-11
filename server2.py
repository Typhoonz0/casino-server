from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)
SECRET = "a-secret-salt"

def hash_balance(balance):
    return hashlib.sha256(f"{balance}{SECRET}".encode()).hexdigest()

@app.route("/get_hash", methods=["POST"])
def get_hash():
    data = request.get_json()
    balance = data.get("balance")
    return jsonify({"hash": hash_balance(balance)})

@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json()
    balance = data.get("balance")
    client_hash = data.get("hash")
    valid = (hash_balance(balance) == client_hash)
    return jsonify({"valid": valid})

if __name__ == "__main__":
    app.run()
