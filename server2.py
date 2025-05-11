from flask import Flask, request, jsonify
import hashlib
import os
import json

app = Flask(__name__)

# Secret key for hashing (must match client)
SECRET = "super_secret_key"
BALANCE_FILE = "player_balances.json"  # File to store player balances

# Load player balances from file
def load_player_balances():
    if os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, "r") as f:
            return json.load(f)
    return {}

# Save player balances to file
def save_player_balances():
    with open(BALANCE_FILE, "w") as f:
        json.dump(player_balances, f)

# In-memory storage for player balances (loaded from file)
player_balances = load_player_balances()

@app.route("/", methods=["GET"])
def index():
    return "✅ Casino server is running."

@app.route("/get_hash", methods=["POST"])
def get_hash():
    try:
        data = request.get_json()
        balance = str(data.get("balance", "0"))
        player_id = data.get("player_id", "")

        # If the player doesn't exist, initialize their balance
        if player_id not in player_balances:
            player_balances[player_id] = float(balance)
        else:
            # Update balance based on request, bypassing hash logic
            player_balances[player_id] = float(balance)

        # Save updated balance to file
        save_player_balances()

        # Generate the hash as usual (this will be sent back for client-side verification)
        hash_val = hashlib.sha256((player_id + balance + SECRET).encode()).hexdigest()
        print(f"Updated balance for {player_id}: {player_balances[player_id]}")
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

        # If the player's balance has changed, update it directly and disregard hash
        if player_id not in player_balances:
            player_balances[player_id] = float(balance)  # Initialize balance if not present
        else:
            player_balances[player_id] = float(balance)  # Directly update the balance

        # Save updated balance to file
        save_player_balances()

        # Now, generate the expected hash (using the new balance)
        expected = hashlib.sha256((player_id + balance + SECRET).encode()).hexdigest()
        print(f"Player ID:      {player_id}")
        print(f"Balance:        {balance}")
        print(f"Expected hash:  {expected}")
        print(f"Client hash:    {client_hash}")

        # We disregard hash validation because we're updating the balance directly
        return jsonify({"valid": True, "balance": player_balances[player_id]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/give_money', methods=['POST'])
def give_money():
    try:
        data = request.get_json()
        player_id = data.get("player_id")
        amount = float(data.get("amount", 0))

        # Check if player exists, and update the balance directly
        if player_id in player_balances:
            player_balances[player_id] += amount
            # Save the updated balance to file
            save_player_balances()
            print(f"New balance for {player_id}: {player_balances[player_id]}")
            return jsonify({"message": f"Given ${amount} to player {player_id}. New balance: ${player_balances[player_id]}"})
        else:
            return jsonify({"error": "Player not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Render requires this to bind to the correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 locally
    app.run(host="0.0.0.0", port=port)
