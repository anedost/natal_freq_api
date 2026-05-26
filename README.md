# NatalFreqAPI

Generates a Pythagorean planetary frequency matrix from a natal chart.

## Theory

- **Pythagoras**: 12 zodiac signs = 12 chromatic semitones.
- **Hans Cousto (1978)**: planetary base frequencies derived from orbital periods via octave transposition.
- **Formula**: `freq = base × 2^(semitone/12) × 2^(degree/29/12) × (432/440)`
- **Tuning**: 432 Hz (via `432/440` coefficient)

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
  "lat": 50.4501,
  "lng": 30.5234,
  "city": "Kyiv",
  "state": "Kyiv City",
  "country": "Ukraine"
}
```

`hour` and `minute` are optional (default: `12:00`).

**Response:**
```json
{
  "birthdate": "15.03.1990",
  "lat": 50.4501,
  "lng": 30.5234,
  "city": "Kyiv",
  "state": "Kyiv City",
  "country": "Ukraine",
  "planets": {
    "Sun":  { "freq": 245.70, "bpm": 3.94,  "sign": "Pisces", "deg": 24.5, "color": [255, 200, 50] },
    "Moon": { "freq": 315.45, "bpm": 52.71, "sign": "Scorpio", "deg": 7.2,  "color": [200, 210, 255] }
  }
}
```

**Error Responses:**

`400 Bad Request` (invalid calendar date)
```json
{
  "detail": "Invalid date: day is out of range for month"
}
```

`404 Not Found` (chart/timezone resolution issue)
```json
{
  "detail": "Could not determine timezone for coordinates (0.0, 0.0)."
}
```

`500 Internal Server Error` (unexpected chart processing error)
```json
{
  "detail": "Chart error: <error message>"
}
```

### `GET /health`

Returns `{"status": "ok"}`.

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
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
| timezonefinder | Coordinates -> local IANA timezone |
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
