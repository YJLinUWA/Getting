import RPi.GPIO as GPIO
import time
import picamera

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.OUT)  # Red LED
GPIO.setup(15, GPIO.OUT)  # Infrared LED

# Set up PWM signals for red and infrared LEDs
red_pwm = GPIO.PWM(14, 10000)  # Frequency of 10kHz
ir_pwm = GPIO.PWM(15, 10000)  # Frequency of 10kHz
red_pwm.start(100)  # Initial duty cycle of 0%
ir_pwm.start(0)  # Initial duty cycle of 100%
duty_cycle = 100  # Set duty cycle to 100%

# Set up camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)  # Set resolution to 640x480 pixels
camera.framerate = 90  # Set framerate to 90fps

# Run for 10 seconds
duration = 10  # in seconds
start_time = time.time()
frame_num = 0

while (time.time() - start_time) < duration:
    # Switch LEDs
    if duty_cycle == 100:
        red_pwm.ChangeDutyCycle(0)
        ir_pwm.ChangeDutyCycle(100)
        duty_cycle = 0
    else:
        red_pwm.ChangeDutyCycle(100)
        ir_pwm.ChangeDutyCycle(0)
        duty_cycle = 100
    time.sleep(0.5)  # Wait for LEDs to settle

    # Capture frame
    filename = 'frame_{:03d}.jpg'.format(frame_num)
    camera.capture(filename)
    frame_num += 1

# Clean up
red_pwm.stop()
ir_pwm.stop()
GPIO.cleanup()
