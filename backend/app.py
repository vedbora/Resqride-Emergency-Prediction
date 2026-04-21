@app.route("/predict", methods=["POST"])
def predict():
    try:
        if model is None:
            return jsonify(
                {
                    "error": "Model is not loaded. Ensure backend/model.pkl exists and is valid."
                }
            ), 500

        # ✅ FIXED JSON HANDLING
        data = request.get_json()
        if data is None:
            data = request.json

        if not data:
            return jsonify({"error": "Request body must be valid JSON."}), 400

        if "lat" not in data or "lng" not in data:
            return jsonify({"error": "Both 'lat' and 'lng' are required."}), 400

        try:
            lat = float(data["lat"])
            lng = float(data["lng"])
        except (TypeError, ValueError):
            return jsonify({"error": "'lat' and 'lng' must be numeric values."}), 400

        prediction = model.predict([[lat, lng]])[0]

        label_map = {
            0: "EMS",
            1: "Fire",
            2: "Traffic"
        }
        predicted_reason = label_map.get(prediction, str(prediction))

        return jsonify(
            {
                "lat": lat,
                "lng": lng,
                "predicted_emergency_type": predicted_reason
            }
        ), 200

    except Exception as exc:
        return jsonify({"error": f"Server error: {str(exc)}"}), 500
