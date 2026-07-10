from asyncio import subprocess
import re
from gpiozero import PWMOutputDevice
from time import sleep

FAN_PIN = 19

# Tạo PWM fan
fan = PWMOutputDevice(FAN_PIN)

# Ngưỡng nhiệt độ (có thể chỉnh)
TEMP_MEDIUM = 45
TEMP_MAX = 50

# PWM giá trị tương ứng với nhiệt độ
LOW=0.3
MEDIUM=0.6
HIGH=1.0

HDD_DEVICE = '/dev/sdc'

# sudo smartctl -n standby -A -d sat /dev/sdc

def get_hdd_temp():
    """
    Return HDD temperature in °C.
    Return None if drive is sleeping or SMART unavailable.
    """

    try:
        result = subprocess.run(
            [
                "smartctl",
                "-n", "standby",
                "-A",
                "-d", "sat",
                HDD_DEVICE
            ],
            capture_output=True,
            text=True
        )

        # Drive sleeping
        if "STANDBY" in result.stdout.upper():
            return None

        for line in result.stdout.splitlines():
            if "Temperature_Celsius" in line:
                m = re.search(r"(\d+)\s*\(", line)
                if m:
                    return int(m.group(1))
        return None

    except Exception as e:
        print(e)
        return None

def temp_to_pwm(temp):
    if temp == None:
        return 0.0
    elif temp >= TEMP_MAX:
        return HIGH
    elif temp >= TEMP_MEDIUM:
        return MEDIUM
    else:
        return LOW

try:
    while True:
        temp = get_hdd_temp()
        speed = temp_to_pwm(temp)

        fan.value = speed

        print(f"Hdd Temp: {temp:.1f}°C | Fan speed: {speed*100:.0f}%", flush=True)

        #Sleep 5 minutes if fan is running, otherwise sleep 10 seconds
        sleep(300)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    fan.off()
