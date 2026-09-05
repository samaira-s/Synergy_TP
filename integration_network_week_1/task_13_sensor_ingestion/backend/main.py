import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

# ---------- Logging setup ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("sensor_backend")

app = FastAPI(title="AgroTech Soil Sensor Ingestion Backend")

# ---------- In-memory storage ----------
# List of accepted readings, most recent last. Fine for this task's scope
# (no persistence needed, no concurrent-write concerns at this data rate).
readings_store = []

# ---------- Physical plausibility bounds (meaning-level validation) ----------
MOISTURE_MIN, MOISTURE_MAX = 0.0, 100.0      # percent — physically cannot be outside this
TEMP_MIN, TEMP_MAX = -10.0, 60.0             # Celsius — realistic soil temperature range


class Readings(BaseModel):
    soil_moisture_pct: float
    soil_temperature_c: float


class SensorReading(BaseModel):
    device_id: str
    session_id: str
    timestamp: str
    readings: Readings
    status: str = "ok"

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp(cls, v):
        try:
            # Accept "Z" suffix by normalizing to +00:00 for fromisoformat
            datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError(f"timestamp '{v}' is not valid ISO 8601")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ("ok", "error"):
            raise ValueError(f"status must be 'ok' or 'error', got '{v}'")
        return v


@app.on_event("startup")
def on_startup():
    logger.info("Sensor ingestion backend starting up. Storage is in-memory and empty.")


@app.get("/health")
def health():
    logger.info("Health check requested.")
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@app.post("/readings")
def post_reading(reading: SensorReading):
    # Structural validation (types/required fields) is already handled by Pydantic
    # above, automatically, before this function body even runs. Below is
    # meaning-level validation: values that are the RIGHT TYPE but physically
    # impossible or implausible.
    errors = []
    if not (MOISTURE_MIN <= reading.readings.soil_moisture_pct <= MOISTURE_MAX):
        errors.append(
            f"soil_moisture_pct={reading.readings.soil_moisture_pct} is outside "
            f"plausible range [{MOISTURE_MIN}, {MOISTURE_MAX}]"
        )
    if not (TEMP_MIN <= reading.readings.soil_temperature_c <= TEMP_MAX):
        errors.append(
            f"soil_temperature_c={reading.readings.soil_temperature_c} is outside "
            f"plausible range [{TEMP_MIN}, {TEMP_MAX}]"
        )

    if errors:
        logger.warning(f"Rejected reading from {reading.device_id}: {errors}")
        raise HTTPException(status_code=422, detail={"errors": errors})

    readings_store.append(reading.model_dump())
    logger.info(
        f"Accepted reading from device={reading.device_id} "
        f"session={reading.session_id} "
        f"moisture={reading.readings.soil_moisture_pct}% "
        f"temp={reading.readings.soil_temperature_c}C"
    )
    return {"message": "Reading accepted", "stored_count": len(readings_store)}


@app.get("/readings/latest")
def get_latest_reading():
    if not readings_store:
        logger.info("Latest-reading requested but store is empty.")
        raise HTTPException(status_code=404, detail="No readings have been stored yet")
    return readings_store[-1]


@app.get("/devices")
def get_devices():
    device_ids = sorted(set(r["device_id"] for r in readings_store))
    logger.info(f"Devices list requested. {len(device_ids)} known device(s).")
    return {"devices": device_ids}


@app.get("/devices/{device_id}/latest")
def get_device_latest(device_id: str):
    device_readings = [r for r in readings_store if r["device_id"] == device_id]
    if not device_readings:
        logger.info(f"Latest-reading requested for unknown/empty device: {device_id}")
        raise HTTPException(status_code=404, detail=f"No readings found for device_id '{device_id}'")
    return device_readings[-1]
