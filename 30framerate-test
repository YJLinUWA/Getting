import RPi.GPIO as GPIO
import time
import picamera

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)  # Red LED
GPIO.setup(15, GPIO.OUT)  # Infrared LED

# Set up PWM signals for red and infrared LEDs
red_pwm = GPIO.PWM(14, 50)  # Frequency of 50Hz
ir_pwm = GPIO.PWM(15, 50)  # Frequency of 50Hz
red_pwm.start(0)  # Initial duty cycle of 0%
ir_pwm.start(100)  # Initial duty cycle of 100%
duty_cycle = 50  # Set duty cycle to 50%

# Set up camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)  # Set resolution to 640x480 pixels
camera.framerate = 30  # Set framerate to 30fps

# Run for 10 seconds
duration = 10  # in seconds
start_time = time.time()
frame_num = 0

while (time.time() - start_time) < duration:
    # Switch LEDs
    red_pwm.ChangeDutyCycle(duty_cycle)
    ir_pwm.ChangeDutyCycle(100 - duty_cycle)
    time.sleep(0.5)  # Wait for LEDs to settle

    # Capture frame
    filename = 'frame_{:03d}.jpg'.format(frame_num)
    camera.capture(filename)
    frame_num += 1

# Clean up
red_pwm.stop()
ir_pwm.stop()
GPIO.cleanup()
