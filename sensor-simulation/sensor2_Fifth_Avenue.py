import time
import random
from azure.iot.device import IoTHubDeviceClient, Message
import json

CONNECTION_STRING = "HostName=assignment2hub.azure-devices.net;DeviceId=sensor2_Fifth_Avenue;SharedAccessKey=KlpCnyF2vG4MIc18X909uKv/R7LVXvNj1A2ZhWPKdAg="

def get_telemetry():
    return {
        "location": "Fifth Avenue",
        "iceThickness": round(random.uniform(15.0, 35.0), 2),
        "surfaceTemperature": round(random.uniform(-10.0, 2.0), 2),
        "snowAccumulation": round(random.uniform(0.0, 20.0), 2),
        "externalTemperature": round(random.uniform(-15.0, 5.0), 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

def main():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    print("Sending telemetry from Fifth Avenue sensor to IoT Hub...")
    try:
        while True:
            telemetry = get_telemetry()
            message = Message(json.dumps(telemetry))
            client.send_message(message)
            print(f"Sent message: {message}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Simulation stopped.")
    finally:
        client.disconnect()
        print("Disconnected from IoT Hub.")

if __name__ == "__main__":
    main()
