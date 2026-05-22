# NatalFreqAPI

Generates a Pythagorean planetary frequency matrix from a natal chart.

## Theory

- **Pythagoras**: 12 zodiac signs = 12 chromatic semitones.
- **Hans Cousto (1978)**: planetary base frequencies derived from orbital periods via octave transposition.
- **Formula**: `freq = base × 2^(semitone/12) × 2^(degree/29/12)`
- **Tuning**: 432 Hz

## Endpoints

### `POST /generate`

**Request:**
```json
{
  "year": 1990,
  "month": 3,
  "day": 15,
  "hour": 14,
  "minute": 30,
  "city": "Kyiv"
}
```

`hour` and `minute` are optional (default: `12:00`).

**Response:**
```json
{
  "birthdate": "15.03.1990",
  "city": "Kyiv",
  "tuning": "432 Hz",
  "theory": "Pythagorean • Cousto 1978",
  "planets": {
    "Sun":  { "freq": 245.70, "bpm": 3.94,  "sign": "Pis", "deg": 24.5, "color": [255, 200, 50] },
    "Moon": { "freq": 315.45, "bpm": 52.71, "sign": "Sco", "deg": 7.2,  "color": [200, 210, 255] }
  }
}
```

### `GET /health`

Returns `{"status": "ok"}`.

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

## Deploy on Railway

```
uvicorn app:app --host 0.0.0.0 --port $PORT
```

## Stack

| Library | Purpose |
|---|---|
| FastAPI | API framework |
| kerykeion | Swiss Ephemeris natal chart |
| geopy + timezonefinder | City geocoding with local cache |
| certifi | SSL certificates |

## Planet Base Frequencies (Cousto, 432 Hz tuning)

| Planet  | Base Hz |
|---------|---------|
| Sun     | 126.22  |
| Moon    | 210.42  |
| Mercury | 141.27  |
| Venus   | 221.23  |
| Mars    | 144.72  |
| Jupiter | 183.58  |
| Saturn  | 147.85  |
| Uranus  | 207.36  |
| Neptune | 211.44  |
| Pluto   | 140.25  |
