import { useState } from "react";
import "./App.css";

function App() {
  const [pm25, setPm25] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [email, setEmail] = useState("");
  const [subMessage, setSubMessage] = useState("");
  console.log("Rendering... pm25 =", pm25);
  // Call api to check the current pm 2.5 based on user's location
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
      (err) => {
        console.log("Location error:", err);
        setError("Location access denied");
        setLoading(false);
      };
    });
  }
  //check the level of air quality based on pm 2.5
  function getLevel(value) {
    if (value < 0) {
      return "Unknown value";
    } else if (value <= 12) {
      return "Good";
    } else if (value <= 35.4) {
      return "Moderate";
    } else if (value <= 55.4) {
      return "Unhealthy for Sensitive Groups";
    } else if (value <= 150.4) {
      return "Unhealthy";
    } else {
      return "Very Unhealthy";
    }
  }
  //get the class name for different level to display different color in css
  function getLevelClass(value) {
    if (value < 0) {
      return "level-unknown";
    } else if (value <= 12) {
      return "level-good";
    } else if (value <= 35.4) {
      return "level-moderate";
    } else if (value <= 55.4) {
      return "level-unhealthy-sensitive";
    } else if (value <= 150.4) {
      return "level-unhealthy";
    } else {
      return "level-very-unhealthy";
    }
  }

  function handleSubscribe() {
    if (!email) {
      setSubMessage("Please enter your email!");
      return;
    }
    //ask for user location
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        fetch("http://127.0.0.1:5000/api/subscribe", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: email, lat: lat, lon: lon }),
        })
          .then((response) => response.json())
          .then((data) => setSubMessage(data.message));
      },
      (err) => {
        setSubMessage("Locaton access denied");
      },
    );
  }
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
          <p className="pm25-label">{pm25} µg/m³</p>
          <p className={getLevelClass(pm25)}>
            Air Quality Level: {getLevel(pm25)}
          </p>
        </div>
      )}
      <div className="subscribe-card">
        <h2 className="get-email"> Do you want to get PM2.5 alert?</h2>
        <input
          className="user-input"
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        ></input>
        <button
          className="subscribe-btn"
          type="button"
          onClick={handleSubscribe}
        >
          Subscribe
        </button>
        {subMessage && <p className="sub-message">{subMessage}</p>}
      </div>
    </div>
  );
}

export default App;
