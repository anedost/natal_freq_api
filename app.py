import ssl, certifi, os, sys
os.environ['SSL_CERT_FILE']      = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent))
import chart as m

app = FastAPI(
    title="NatalFreqAPI",
    description="Pythagorean planetary matrix generator • Cousto 1978 • 432 Hz",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    year:   int = Field(..., ge=1900, le=2100, example=1990)
    month:  int = Field(..., ge=1,    le=12,   example=3)
    day:    int = Field(..., ge=1,    le=31,   example=15)
    hour:   int   = Field(12,  ge=0,    le=23,    example=14)
    minute: int   = Field(0,   ge=0,    le=59,    example=30)
    lat:     float = Field(..., ge=-90,  le=90,    example=50.4501)
    lng:     float = Field(..., ge=-180, le=180,   example=30.5234)
    city:    str = Field(..., example="Donetsk")
    state:   str = Field(..., example="Donetsk Oblast")
    country: str = Field(..., example="Ukraine")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate")
def generate(req: GenerateRequest):
    try:
        birthdate = date(req.year, req.month, req.day)
    except ValueError as e:
        raise HTTPException(400, f"Invalid date: {e}")
    try:
        planets = m.build_chart(req.year, req.month, req.day,
                                req.hour, req.minute, req.lat, req.lng)
    except ValueError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, f"Chart error: {e}")

    return {
        "birthdate": birthdate.strftime("%d.%m.%Y"),
        "lat":       req.lat,
        "lng":       req.lng,
        "city":      req.city,
        "state":     req.state,
        "country":   req.country,
        "tuning":    "432 Hz",
        "theory":    "Pythagorean • Cousto 1978",
        "planets": {
            name: {
                "freq":  d["freq"],
                "bpm":   round(d["bpm"], 4),
                "sign":  d["sign"],
                "deg":   round(d["deg"], 2),
                "color": list(d["color"]),
            }
            for name, d in planets.items()
        }
    }
