# IoT Ice Statistics Sensor Simulator

## 1. Overview

### What the simulatore does

- This sensor_simulater is used to generate the timestamp and location of the IoT device and then create random numbers for the Ice Thickness, Surface Temperature, Snow Accumulation and the External Temperature of the ice.

### Technologies Used

- Python 3.13
- Azure IoT SDK

## 2. Prerequisites

Python 3.13 +

All requirements within the virtual environment:

- azure-iot-device==2.14.0
- certifi==2025.11.12
- charset-normalizer==3.4.4
- deprecation==2.1.0
- dotenv==0.9.9
- idna==3.11
- janus==2.0.0
- packaging==25.0
- paho-mqtt==1.6.1
- PySocks==1.7.1
- python-dotenv==1.2.1
- requests==2.32.5
- requests-unixsocket2==1.0.1
- typing_extensions==4.15.0
- urllib3==2.6.1

## 3. Installation & Configuration

- Git clone the repo
  - `git clone https://github.com/demurphyh/rideau-canal-sensor-simulation`

- Create a python virtual environment (Instructions and commands for MacOS)
  - `python -m venv venv`
- Activate Virtual Environment
  - `source venv/bin/activate`
- [Instructions for Windows/ Linux](https://www.w3schools.com/python/python_virtualenv.asp)

- `pip install azure-iot-device`
- Add the three device connection string to the .env file

## 4. Usage

- Run the script
  - `python sensor_simulator.py`

## 5. Code Structure

### Main Components and Key Functions

```Python
DEVICE_CONN_DOWS = os.getenv("DEVICE_CONN_DOWS")
DEVICE_CONN_FIFTH = os.getenv("DEVICE_CONN_FIFTH")
DEVICE_CONN_NAC = os.getenv("DEVICE_CONN_NAC")
```

- This loads all of our IoT device connection strings into variable for the different sensors to be used later.

```Python
clients = [
    IoTHubDeviceClient.create_from_connection_string(conn)
    for conn in CONNECTION_STRINGS
]
```

- This uses the IoT device SDK to create clients from the stored connection strings.

```Python
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
```

- This is the main part of the code responsible for generating the data, it returns data for the current timestamp, and location of the device then generates random data for the ice thickness, surface temperature, snow accumulation and external temp. it then it converts the message to JSON format and sends it to the azure hub. This process will occur every 10 seconds unless interupted. It includes a print statement to state where it was sent from to visually confirm where the data was sent from at a glance.

## 6. Sensor Data Format

### JSON Schema

```JSON
{
 'timestamp':,
 'location':,
 'iceThickness':,
 'surfaceTemperature':,
 'snowAccumulation':,
 'externalTemp':
 }
 ```

### Example Output

- `Sent from Dow's Lake: {'timestamp': '2025-12-10T18:54:38.354235+00:00', 'location': "Dow's Lake", 'iceThickness': 10.01, 'surfaceTemperature': -22.97, 'snowAccumulation': 33.62, 'externalTemp': -19.42}`

- `Sent from Fifth Avenue: {'timestamp': '2025-12-10T18:54:38.559802+00:00', 'location': 'Fifth Avenue', 'iceThickness': 12.24, 'surfaceTemperature': -1.66, 'snowAccumulation': 33.0, 'externalTemp': -27.57}`

- `Sent from NAC: {'timestamp': '2025-12-10T18:54:38.718581+00:00', 'location': 'NAC', 'iceThickness': 38.7, 'surfaceTemperature': -10.18, 'snowAccumulation': 36.06, 'externalTemp': -15.74}`

## 7. Troubleshooting

- If the application is not running make sure the virtual environment is created and activated and then that all requirements are installed.
- If application runs but doesn't send data ensure all three connection strings are added to the .env file and are correct
