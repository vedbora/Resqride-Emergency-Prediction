# ResQride Emergency Prediction System

ResQride is a full-stack machine learning project that predicts emergency type (`EMS`, `Fire`, `Traffic`) from location coordinates (`lat`, `lng`).

It uses:
- **Backend**: Flask API
- **Frontend**: React (CDN-based) + modern CSS UI
- **Model**: Pre-trained Decision Tree model saved as `model.pkl`

## Project Structure

```text
ResQride Emergency Prediction System/
├── backend/
│   ├── app.py
│   ├── train_model.py
│   ├── 911.csv            # place dataset here (for training script)
│   ├── model.pkl          # place your trained model here
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
└── README.md
```

## Dataset and ML Logic

- Dataset: 911 Calls dataset
- Features: `lat`, `lng`
- Target: `reason` extracted from `title` by splitting at `":"`
- Model: `DecisionTreeClassifier`
- Saved model: `backend/model.pkl`

> Example reason extraction logic used during training:
> `df["reason"] = df["title"].apply(lambda x: x.split(":")[0])`

## Backend Setup (Flask API)

1. Open terminal in project root:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Generate trained model (recommended if you don't already have `model.pkl`):
   - Place dataset at: `backend/911.csv`
   - Run:
     ```bash
     python train_model.py
     ```
   - This creates: `backend/model.pkl`

4. Run backend:
   ```bash
   python app.py
   ```

5. API runs at:
   - `http://127.0.0.1:5000`

### API Endpoint

- **POST** `/predict`
- Request JSON:
  ```json
  {
    "lat": 40.2732,
    "lng": -75.2481
  }
  ```
- Success response:
  ```json
  {
    "lat": 40.2732,
    "lng": -75.2481,
    "predicted_emergency_type": "EMS"
  }
  ```
- Error response example:
  ```json
  {
    "error": "Both 'lat' and 'lng' are required."
  }
  ```

## Frontend Setup

1. Open another terminal:
   ```bash
   cd frontend
   ```

2. Start a local static server (recommended):
   ```bash
   python -m http.server 5500
   ```

3. Open browser:
   - `http://127.0.0.1:5500`

4. Enter latitude and longitude, then click **Predict**.

## Test API Quickly (Optional)

Use curl:

```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "{\"lat\":40.2732,\"lng\":-75.2481}"
```

## Notes

- CORS is enabled so frontend can call backend from a different origin/port.
- Backend returns readable labels (`EMS`, `Fire`, `Traffic`), not numeric codes.
- The UI handles loading, validation, and API error messages.
- If you already have a trained model, you can skip `train_model.py` and place it directly at `backend/model.pkl`.
