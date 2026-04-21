const API_URL = "https://resqride-emergency-prediction.onrender.com/predict";

function App() {
  const [lat, setLat] = React.useState("");
  const [lng, setLng] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [result, setResult] = React.useState("");
  const [error, setError] = React.useState("");

  const handlePredict = async () => {
    setResult("");
    setError("");

    if (!lat.trim() || !lng.trim()) {
      setError("Please enter both latitude and longitude.");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          latitude: Number(lat),
          longitude: Number(lng)
        })
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Prediction failed. Please try again.");
        return;
      }

      setResult(`Predicted Emergency Type: ${data.predicted_emergency_type}`);
    } catch (err) {
      setError("Could not connect to backend server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="app-container">
      <section className="card">
        <h1>ResQride Emergency Prediction System</h1>
        <p className="subtitle">
          Predict emergency type (EMS, Fire, Traffic) using latitude and longitude.
        </p>

        <div className="input-group">
          <label>Latitude</label>
          <input
            type="number"
            step="any"
            placeholder="e.g. 40.2732"
            value={lat}
            onChange={(e) => setLat(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>Longitude</label>
          <input
            type="number"
            step="any"
            placeholder="e.g. -75.2481"
            value={lng}
            onChange={(e) => setLng(e.target.value)}
          />
        </div>

        <button onClick={handlePredict} disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </button>

        {result && <div className="result">{result}</div>}
        {error && <div className="error">{error}</div>}
      </section>
    </main>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
