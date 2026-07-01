import paho.mqtt.client as mqtt
import psutil
import time
import json
from app import logger

broker = "localhost"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(broker, 1883, 60)

def get_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return float(f.read()) / 1000.0
    except:
        return 0

def publish_monitoring_data():
    cpu = int(round(psutil.cpu_percent()))
    ram = int(round(psutil.virtual_memory().percent))
    disk = psutil.disk_usage("/").percent
    temp = get_temp()

    client.publish("pi/mem", ram)
    client.publish("pi/temp", temp)
    client.publish("pi/cpu", cpu)
    client.publish("pi/disk", disk)

    logger.info(f"CPU: {cpu}%, Memory: {ram}%, Disk: {disk}%, Temperature: {temp}°C")
