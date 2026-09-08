# Task 13 — Sensor Data Ingestion Backend (AgroTech)

## Scenario
Simulated soil sensors (moisture % and temperature °C) send periodic readings
to a FastAPI backend over the local network.

## JSON Contract
See `examples/sample_reading.json`. Fields:
- `device_id` (string) — identifies which sensor sent the reading
- `session_id` (string) — groups readings from one continuous deployment/run
- `timestamp` (ISO 8601 string, UTC) — when the reading was taken
- `readings.soil_moisture_pct` (float, 0-100) — soil moisture percentage
- `readings.soil_temperature_c` (float, -10 to 60) — soil temperature in Celsius
- `status` ("ok" or "error") — sensor self-reported health

## Setup
```bash
pip install fastapi uvicorn requests
```

## Running the backend
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```
`--host 0.0.0.0` is required (not `127.0.0.1`) so the OTHER laptop can reach
this machine over the LAN — binding to 127.0.0.1 only accepts connections
from the same machine.

## Running the simulator (from the other laptop, or same machine to test)
```bash
cd simulator
python simulate.py --url http://<BACKEND_LAPTOP_LAN_IP>:8000 \
    --device-id soil-sensor-01 --session-id session-demo \
    --interval 2 --count 10 --bad-at 5
```
Find `<BACKEND_LAPTOP_LAN_IP>` via `ipconfig` (Windows) on the backend
laptop — use the IPv4 address, not `localhost`.

## Routes
- `GET /health` — liveness check
- `POST /readings` — submit a reading (validates structure via Pydantic,
  then validates physical plausibility of moisture/temperature ranges)
- `GET /readings/latest` — most recent reading across all devices
- `GET /devices` — list of known device IDs
- `GET /devices/{device_id}/latest` — most recent reading for one device

## Validated end-to-end (see chat/report for full test log)
- Valid readings from a single device: accepted, count increments correctly
- Multiple devices tracked independently
- Deliberately invalid reading (moisture=250%) correctly rejected with HTTP 422
  and a clear error message, does not crash the backend
- Missing field and wrong-type payloads rejected by Pydantic automatically
- `/devices` and `/devices/{id}/latest` correctly scoped per device
- Unknown device_id returns HTTP 404, not a crash
- Simulator handles backend-down (connection refused) gracefully — logs and
  continues to the next reading instead of crashing
## Known Issue: Cross-Device Connectivity
Attempted cross-device test between two laptops on the same campus Wi-Fi.
A basic `ping` between them failed completely (100% packet loss) despite
both sharing an identical Default Gateway (same subnet). Likely cause:
client isolation (AP isolation), a common institutional Wi-Fi setting that
blocks direct device-to-device traffic while still allowing internet access.
Workaround attempted: switching both devices to a personal mobile hotspot.
See the full report for the detailed diagnosis.

