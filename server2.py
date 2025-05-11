from flask import Flask, request, jsonify
import hashlib
import os

app = Flask(__name__)

# Secret key for hashing (must match client)
SECRET = "super_secret_key"
player_balances = {}  # In-memory storage for player balances

@app.route("/", methods=["GET"])
def index():
    return "✅ Casino server is running."

@app.route("/get_hash", methods=["POST"])
def get_hash():
    try:
        data = request.get_json()
        balance = str(data.get("balance", "0"))
        player_id = data.get("player_id", "")

        hash_val = hashlib.sha256((player_id + balance + SECRET).encode()).hexdigest()
        return jsonify({"hash": hash_val})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/validate', methods=['POST'])
def validate():
    try:
        data = request.json
        balance = str(data.get("balance"))
        client_hash = data.get("client_hash")
        player_id = data.get("player_id", "")

        expected = hashlib.sha256((player_id + balance + SECRET).encode()).hexdigest()
        print(f"Player ID:      {player_id}")
        print(f"Balance:        {balance}")
        print(f"Expected hash:  {expected}")
        print(f"Client hash:    {client_hash}")

        if client_hash == expected:
            return jsonify({"valid": True})
        else:
            return jsonify({"valid": False, "client_hash": client_hash, "expected": expected, "balance": balance})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/give_money', methods=['POST'])
def give_money():
    try:
        data = request.get_json()
        player_id = data.get("player_id")
        amount = float(data.get("amount", 0))

        if player_id in player_balances:
            player_balances[player_id] += amount
            return jsonify({"message": f"Given ${amount} to player {player_id}. New balance: ${player_balances[player_id]}"})
        else:
            return jsonify({"error": "Player not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Render requires this to bind to the correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 locally
    app.run(host="0.0.0.0", port=port)
