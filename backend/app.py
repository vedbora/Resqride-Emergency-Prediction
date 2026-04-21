from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib

# ✅ FIRST create app
app = Flask(__name__)
CORS(app)

# Load model
def load_model():
    model_path = Path(__file__).resolve().parent / "model.pkl"
    if not model_path.exists():
        raise FileNotFoundError("model.pkl not found in backend folder.")
    return joblib.load(model_path)

try:
    model = load_model()
except Exception:
    model = None

# ✅ HOME ROUTE
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "ResQride Emergency Prediction API is running.",
        "endpoint": "POST /predict"
    })

# ✅ PREDICT ROUTE
@app.route("/predict", methods=["POST"])
def predict():
    try:
        if model is None:
            return jsonify({
                "error": "Model is not loaded. Ensure model.pkl exists."
            }), 500

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
        except:
            return jsonify({"error": "'lat' and 'lng' must be numeric."}), 400

        prediction = model.predict([[lat, lng]])[0]

        label_map = {
            0: "EMS",
            1: "Fire",
            2: "Traffic"
        }

        return jsonify({
            "lat": lat,
            "lng": lng,
            "predicted_emergency_type": label_map.get(prediction, str(prediction))
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ LOCAL RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
