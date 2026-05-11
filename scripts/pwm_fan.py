from gpiozero import PWMOutputDevice
from time import sleep

FAN_PIN = 18

# Tạo PWM fan
fan = PWMOutputDevice(FAN_PIN)

# Ngưỡng nhiệt độ (có thể chỉnh)
TEMP_MIN = 45   # bắt đầu quay
TEMP_MEDIUM = 52
TEMP_MAX = 55   # max speed

# PWM giá trị tương ứng với nhiệt độ
LOW=0.4
MEDIUM=0.6
HIGH=1.0
OFF=0.0

def get_temp():
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        return int(f.read()) / 1000

def temp_to_pwm(temp):
    if temp >= TEMP_MAX:
        return HIGH
    elif temp >= TEMP_MEDIUM:
        return MEDIUM
    elif temp >= TEMP_MIN:
        return LOW
    else:
        return OFF

try:
    while True:
        
        temp = get_temp()
        speed = temp_to_pwm(temp)

        fan.value = speed

        print(f"Temp: {temp:.1f}°C | Fan speed: {speed*100:.0f}%")

        if speed > 0:
         sleep(30)
        else:
         sleep(10)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    fan.off()
