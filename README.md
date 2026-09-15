# PM2.5 Air Quality Monitor

A full-stack web app that shows real-time PM2.5 air quality readings and next-hour predictions based on user location,
with optional email alerts when predicted air quality crosses a user-set threshold.
**Live demo:** https://pm2-5-air-quality.onrender.com
Built as a companion project to my ENVISION-AI capstone, adapting a trained LSTM model for real-world, location-based use.

## Known Limitations

**Prediction accuracy for non-Romanian locations.**
The LSTM model was trained exclusively on sensor data from Ploiești, Romania.
Predictions for U.S. locations are rough estimates, not accurate forecasts,
because the model learned its weather and pollutant ranges from a different climate and sensor setup.
The app's UI and alert emails disclose this directly.

**No email verification.** Subscriptions only validate email format, not deliverability — anyone can enter any address.

**Third-party API rate limits.** Weather and air quality data come from Open-Meteo's free tier, which has daily request caps. Heavy testing or high subscriber volume can exhaust these.

## Features

- Current PM2.5 reading based on the user's browser location, with reverse geocoding to show a city name
- Next-hour PM2.5 prediction from an LSTM model
- Email subscription with a configurable alert threshold
- Hourly background check that emails subscribers if the predicted PM2.5 exceeds their threshold, with a 12-hour cooldown between alerts
- Welcome email on subscription, confirming the threshold and location

## Tech Stack

**Frontend:** React (Vite), plain CSS
**Backend:** Flask, APScheduler for the hourly job
**Database:** PostgreSQL (Supabase)
**ML:** TensorFlow/Keras LSTM, trained on Ploiești, Romania air quality sensor data as part of my ENVISION-AI capstone
**Data sources:** [Open-Meteo](https://open-meteo.com/) for weather and air quality (CC BY 4.0)
**Email:** Gmail SMTP
**Hosting:** Render

## Setup

### Prerequisites

- Python 3.9 (TensorFlow 2.20 does not yet support newer versions)
- Node.js
- A Supabase (or other Postgres) database
- A Gmail account with an [App Password](https://myaccount.google.com/apppasswords)

### Backend

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root:
DATABASE_URL=postgresql://...
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password

Run the database schema in `schema.sql` against your Postgres instance, then:

```bash
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

For production, `npm run build` outputs to `frontend/dist`, which Flask serves directly.

## Architecture

```
React (Vite) → Flask API → Supabase (Postgres) =>
Open-Meteo API (weather + air quality) =>
LSTM model (TensorFlow) → prediction =>
APScheduler (hourly) → email alerts

```

The LSTM was trained on four features — temperature, pressure, humidity, and PM10 — using a 24-hour lookback window. At inference time, the app fetches the last 24 hours of those four values from Open-Meteo, scales them with the same `StandardScaler` fit during training, and feeds them through the model to predict the next hour's PM2.5.
