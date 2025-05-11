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

        return jsonify({"valid": client_hash == expected})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
