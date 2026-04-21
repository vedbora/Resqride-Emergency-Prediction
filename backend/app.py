from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib


app = Flask(__name__)
# Allow frontend apps (different port/origin) to call this API.
CORS(app)


def load_model():
    """
    Load the pre-trained model from disk.
    Kept in a function so startup/load logic is easy to understand and extend.
    """
    model_path = Path(__file__).resolve().parent / "model.pkl"
    if not model_path.exists():
        raise FileNotFoundError(
            "model.pkl not found in backend folder. Please place the trained model there."
        )
    return joblib.load(model_path)


try:
    model = load_model()
except Exception:
    model = None


@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict emergency type from latitude and longitude.
    Expected JSON input: { "lat": number, "lng": number }
    """
    try:
        if model is None:
            return jsonify(
                {
                    "error": "Model is not loaded. Ensure backend/model.pkl exists and is valid."
                }
            ), 500

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Request body must be valid JSON."}), 400

        if "lat" not in data or "lng" not in data:
            return jsonify({"error": "Both 'lat' and 'lng' are required."}), 400

        try:
            lat = float(data["lat"])
            lng = float(data["lng"])
        except (TypeError, ValueError):
            return jsonify({"error": "'lat' and 'lng' must be numeric values."}), 400

        # Predict class label directly using the trained model.
        prediction = model.predict([[lat, lng]])[0]

        # If model outputs numeric classes, map them to readable labels.
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
        # Generic safety net for unexpected issues.
        return jsonify({"error": f"Server error: {str(exc)}"}), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {
            "message": "ResQride Emergency Prediction API is running.",
            "endpoint": "POST /predict"
        }
    )


if __name__ == "__main__":
    # Debug True for development convenience.
    app.run(host="0.0.0.0", port=5000, debug=True)
