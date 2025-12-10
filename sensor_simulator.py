import os
import json
import time
import random
from datetime import datetime, timezone
from dotenv import load_dotenv
from azure.iot.device import IoTHubDeviceClient, Message

load_dotenv()

DEVICE_CONN_DOWS = os.getenv("DEVICE_CONN_DOWS")
DEVICE_CONN_FIFTH = os.getenv("DEVICE_CONN_FIFTH")
DEVICE_CONN_NAC = os.getenv("DEVICE_CONN_NAC")

LOCATIONS = ["Dow's Lake", "Fifth Avenue", "NAC"]
CONNECTION_STRINGS = [DEVICE_CONN_DOWS, DEVICE_CONN_FIFTH, DEVICE_CONN_NAC]

# Validate .env configuration
for i, conn in enumerate(CONNECTION_STRINGS):
    if not conn:
        raise Exception(
            f"MISSING CONNECTION STRING FOR {LOCATIONS[i]}.\n"
            f"Add to .env: DEVICE_CONN_DOWS / DEVICE_CONN_FIFTH / DEVICE_CONN_NAC"
        )

clients = [
    IoTHubDeviceClient.create_from_connection_string(conn)
    for conn in CONNECTION_STRINGS
]

print("Starting Python IoT Sensor Simulation")
print("Sending telemetry to Azure IoT Hub every 10 seconds\n")


def generate_sensor_data(location: str):
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),

        "location": location,

        "iceThickness": round(random.uniform(10, 60), 2),
        "surfaceTemperature": round(random.uniform(-25, 0), 2),
        "snowAccumulation": round(random.uniform(0, 40), 2),
        "externalTemp": round(random.uniform(-30, 5), 2),
    }

try:
    while True:
        for client, location in zip(clients, LOCATIONS):
            data = generate_sensor_data(location)
            message = Message(json.dumps(data))
            message.content_type = "application/json"
            message.content_encoding = "utf-8"

            client.send_message(message)
            print(f"Sent from {location}: {data}")

        time.sleep(10)

except KeyboardInterrupt:
    print("\n Sensor simulation stopped.")
except Exception as e:
    print(f"ERROR: {e}")
