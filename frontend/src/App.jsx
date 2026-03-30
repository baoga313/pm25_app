import { useState } from "react";
import "./App.css";

function App() {
  const [pm25, setPm25] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  console.log("Rendering... pm25 =", pm25);

  function checkAirQuality() {
    setLoading(true);
    setError(null);

    navigator.geolocation.getCurrentPosition((position) => {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;
      console.log("Step 1 - Got location:", lat, lon);
      fetch(`http://127.0.0.1:5000/api/pm25?lat=${lat}&lon=${lon}`)
        .then((response) => {
          console.log("Step 2 - Got response:", response.status);
          return response.json();
        })
        .then((data) => {
          console.log("Step 3 - Got data:", data);
          setPm25(data.pm2_5);
          setLoading(false);
        });
    });
  }
  (err) => {
    console.log("Location error:", err);
    setError("Location access denied");
    setLoading(false);
  };
  return (
    <div className="container">
      <div className="header">
        <img className="logo" src="src/assets/breath.png" alt="Logo"></img>
        <h1 className="title"> PM2.5 Air Quality Monitor</h1>
      </div>
      <button className="btn" type="button" onClick={checkAirQuality}>
        Check Current Air Quality
      </button>
      {loading && <p className="loading">Fetching data</p>}
      {error && <p className="error">{error}</p>}

      {/* Only show if pm25 is not null */}
      {pm25 && (
        <div className="result-card">
          <p className="pm25-value">{pm25}</p>
          <p className="pm25-label">PM2.5: {pm25} µg/m³</p>
        </div>
      )}
    </div>
  );
}

export default App;
