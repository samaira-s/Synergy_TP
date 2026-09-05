import time
import random
import argparse
from datetime import datetime, timezone

import requests

def make_reading(device_id, session_id, force_bad=False):
    """Builds one reading payload. If force_bad, deliberately produces an
    out-of-range value to test the backend's validation."""
    if force_bad:
        moisture = 250.0   # impossible — over 100%, on purpose
    else:
        moisture = round(random.uniform(20.0, 60.0), 1)  # normal soil moisture range

    temperature = round(random.uniform(18.0, 30.0), 1)  # normal ambient soil temp range

    return {
        "device_id": device_id,
        "session_id": session_id,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "readings": {
            "soil_moisture_pct": moisture,
            "soil_temperature_c": temperature,
        },
        "status": "ok",
    }


def run_simulator(backend_url, device_id, session_id, interval_seconds, num_readings, bad_reading_index):
    print(f"Starting simulator for device '{device_id}' -> {backend_url}")
    print(f"Sending {num_readings} readings, every {interval_seconds}s "
          f"(reading #{bad_reading_index} will be deliberately invalid)")

    for i in range(1, num_readings + 1):
        force_bad = (i == bad_reading_index)
        payload = make_reading(device_id, session_id, force_bad=force_bad)

        try:
            response = requests.post(f"{backend_url}/readings", json=payload, timeout=5)
            print(f"[{i}/{num_readings}] Sent moisture={payload['readings']['soil_moisture_pct']}% "
                  f"temp={payload['readings']['soil_temperature_c']}C "
                  f"-> HTTP {response.status_code}: {response.json()}")
        except requests.exceptions.ConnectionError:
            # This is the "backend is down" case the task requires handling
            # gracefully — the simulator must NOT crash here.
            print(f"[{i}/{num_readings}] Could not reach backend at {backend_url} "
                  f"(connection refused). Skipping this reading and continuing.")
        except requests.exceptions.Timeout:
            print(f"[{i}/{num_readings}] Request to backend timed out. Skipping this reading.")

        if i < num_readings:
            time.sleep(interval_seconds)

    print("Simulator finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AgroTech soil sensor simulator")
    parser.add_argument("--url", default="http://127.0.0.1:8000", help="Backend base URL")
    parser.add_argument("--device-id", default="soil-sensor-01")
    parser.add_argument("--session-id", default="session-demo")
    parser.add_argument("--interval", type=float, default=2.0, help="Seconds between readings")
    parser.add_argument("--count", type=int, default=10, help="Number of readings to send")
    parser.add_argument("--bad-at", type=int, default=5, help="Which reading number is deliberately invalid")
    args = parser.parse_args()

    run_simulator(args.url, args.device_id, args.session_id, args.interval, args.count, args.bad_at)
