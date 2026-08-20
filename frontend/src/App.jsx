import { useState } from "react";
import "./App.css";
import {
  Wind,
  Bell,
  Info,
  MapPin,
  Clock,
  Shield,
  Mail,
  ArrowRight,
} from "lucide-react";

function App() {
  const [pm25, setPm25] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [email, setEmail] = useState("");
  const [subMessage, setSubMessage] = useState("");
  const [location, setLocation] = useState("Unknown");
  const [lastUpdated, setLastUpdated] = useState(null);
  const [threshold, setThreshold] = useState(35);
  console.log("Rendering... pm25 =", pm25);

  // Call api to check the current pm 2.5 based on user's location
  function checkAirQuality() {
    setLoading(true);
    setError(null);

    navigator.geolocation.getCurrentPosition((position) => {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;
      fetch(`http://127.0.0.1:5000/api/pm25?lat=${lat}&lon=${lon}`)
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          setPm25(data.pm2_5);
          setLocation(data.city);
          setLastUpdated(new Date().toLocaleTimeString());
          setLoading(false);
        });
      (err) => {
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
  function getRange(value) {
    if (value == null) return { label: "No data", max: null };
    if (value <= 12) return { label: "Good range: 0-12 µg/m³", max: 12 };
    if (value <= 35.4)
      return { label: "Moderate range: 12.1-35.4 µg/m³", max: 35.4 };
    if (value <= 55.4)
      return { label: "Sensitive range: 35.5-55.4 µg/m³", max: 55.4 };
    if (value <= 150.4)
      return { label: "Unhealthy range: 55.5-150.4 µg/m³", max: 150.4 };
    return { label: "Very unhealthy: 150.5+ µg/m³", max: 250 };
  }
  return (
    <div className="page">
      {/* navbar and icons */}
      <nav className="navbar">
        <div className="brand">
          <div className="brand-mark">
            <Wind size={18} color="#ffffff" />
          </div>
          <div className="brand-text">
            <span className="brand-name"> Air Quality Monitor</span>
            <span className="brand-sub"> PM2.5 tracking and alert</span>
          </div>
        </div>
        <div className="nav-links">
          <a className="nav-link active" href="#">
            Dashboard
          </a>
          <a className="nav-link" href="#">
            PM2.5 Guide
          </a>
          <a className="nav-link" href="#">
            Alerts
          </a>
          <a className="nav-link" href="#">
            About
          </a>
        </div>
        <div className="nav-actions">
          <button className="btn-signup">
            {" "}
            <Bell size={18} color="#ffffff" />
            Get alerts
          </button>
        </div>
      </nav>
      {/* show current pm2.5 */}
      <section className="hero">
        <div className="hero-content">
          <div className="eyebrow">
            <span className="eyebrow-dot"></span>
            <span className="eyebrow-text">Live data • Update every hour</span>
          </div>
          <h1 className="hero-title">
            Monitor Air Quality,
            <br />
            Protect your heath
          </h1>
          <p className="hero-subtitle">
            Real time PM2.5 tracking with AI powered predictions. Get instant
            alerts when air quality affect your heath.
          </p>
          <div className="hero-ctas">
            <button className="cta-primary" onClick={checkAirQuality}>
              <Bell size={18} color="#ffffff" />
              Set up spike alerts
            </button>
            <button className="cta-secondary">
              {" "}
              <Info size={18} color="#0f172a" />
              Learn about PM2.5
            </button>
          </div>
          <div className="hero-meta">
            <div className="meta-item">
              <MapPin size={16} color="#94a3b8" />
              <span>Location: {location}</span>
            </div>
            <div className="meta-item">
              <Clock size={16} color="#94a3b8" />
              <span>
                {lastUpdated
                  ? `Last updated: ${lastUpdated}`
                  : "Not updated yet"}
              </span>
            </div>
          </div>
        </div>
        <div className="gauge-card">
          <div className="gauge-header">
            <div className="gauge-title">
              <span className="gauge-label">Current PM2.5</span>
              <span className="gauge-value">
                {" "}
                {pm25 ? `${pm25}µg/m³` : "-- µg/m³"}
              </span>
            </div>
            <div className={`quality-pill ${pm25 ? getLevelClass(pm25) : ""}`}>
              <span className="pill-dot"></span>
              <span className="pill-text">
                {pm25 ? getLevel(pm25) : "No data"}
              </span>
            </div>
          </div>
          <div className="gauge-wrap">
            <div className={`gauge-center ${pm25 ? getLevelClass(pm25) : ""}`}>
              <span className="gauge-center-label">PM2.5</span>
              <span className="gauge-center-value">
                {pm25 ? Math.round(pm25) : "--"}
              </span>
              <span className="gauge-center-unit">µg/m³</span>
            </div>
          </div>
          <div className="gauge-footer">
            <span className="gauge-range">{getRange(pm25).label}</span>
            <span className="gauge-ratio">
              {pm25 ? `${Math.round(pm25)} / ${getRange(pm25).max}` : "-- / 12"}
            </span>
          </div>
        </div>
      </section>
      {/* explain what is pm2.5 and how it it affect user's health */}
      <section className="explaination-section">
        <div className="section-header">
          <span className="section-eyebrow">What it means</span>
          <h2 className="section-title">Understanding PM2.5</h2>
          <p className="section-desc">
            PM2.5 is the most common metric for measuring fine particulate
            matter. It's a critical health indicator because these particles are
            small enough to bypass your body's natural filters.
          </p>
        </div>
        <div className="explanation-row">
          <div className="explanation-icon">
            <Info size={24} color="#0ea5e9" />
          </div>
          <div className="explanation-text">
            <h3 className="explanation-heading">
              PM2.5 refers to microscopic fine particulate matter under 2.5
              micrometers in size.
            </h3>
            <p className="explanation-body">
              These tiny particles bypass your body's natural filters and enter
              deep into your lungs and bloodstream, making it a critical health
              indicator.
            </p>
          </div>
        </div>
        <div className="facts">
          <div className="fact-card">
            <div className="fact-top">
              <div className=" fact-icon fact-icon-green">
                <Shield size={18} color="#10b981" />
              </div>
              <span className="fact-title">Heath impact</span>
            </div>
            <p className="fact-body">
              Even short-term exposure can trigger respiratory symptoms and
              reduce lung function.
            </p>
          </div>
          <div className="fact-card">
            <div className="fact-top">
              <div className="fact-icon fact-icon-blue">
                <Wind size={18} color="#0ea5e9" />
              </div>
              <span className="fact-title">Sources</span>
            </div>
            <p className="fact-body">
              Common sources include traffic, wildfires, industrial activity,
              and household combustion.
            </p>
          </div>
          <div className="fact-card">
            <div className="fact-top">
              <div className="fact-icon fact-icon-white">
                <Mail size={18} color="#0f172a" />
              </div>
              <span className="fact-title">Alerts</span>
            </div>
            <p className="fact-body">
              Set up email notifications for spikes and plan your day with
              cleaner air in mind.
            </p>
          </div>
        </div>
      </section>
      {/* get the user's email and ask for the threshold */}
      <section className="subscription-section">
        <div className="section-header">
          <span className="section-eyebrow"> Stay informed</span>
          <h2 className="section-title">Get notified when PM2.5 spikes</h2>
          <p className="section-desc">
            Receive instant email warnings when the air quality index drops
            below standard healthy levels in your area.
          </p>
        </div>
        <div className="signup-card">
          <div className="signup-header">
            <h3 className="signup-title">Subscribe for the spike alerts</h3>
            <p className="signup-desc">
              We'll send you a simple, actionable email when PM2.5 crosses your
              chosen threshold
            </p>
          </div>
          <div className="signup-form">
            <div className="email-input">
              <Mail size={18} color="#94a3b8" />
              <input
                type="email"
                placeholder="Enter your email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="threshold-row">
              <div className="threshold-label">
                <span className="threshold-text">
                  Notify when PM2.5 exceeds
                </span>
                <div className="threshold-input-wrap">
                  <input
                    type="number"
                    className="threshold-input"
                    value={threshold}
                    onChange={(e) => setThreshold(e.target.value)}
                  />
                  <span className="threshold-unit">µg/m³</span>
                </div>
              </div>
              <button className="subscribe-button" onClick={handleSubscribe}>
                Notify me
                <ArrowRight size={18} color="#ffffff" />
              </button>
            </div>
          </div>
          <p className="signup-note">
            No spam. Unsubscribe anytime. We only send alerts when PM2.5 crosses
            your threshold.
          </p>
          {subMessage && <p className="sub-message">{subMessage}</p>}
        </div>
      </section>
    </div>
  );
}

export default App;
