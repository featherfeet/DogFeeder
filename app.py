#!/usr/bin/env python3

# Library for controlling the GPIO pins.
from flask import Flask, render_template, make_response, request
import RPi.GPIO as GPIO
import time

# Pin numbers (BCM numbering scheme) that connect to the IN1 and IN2 inputs of the L298N motor controller. Make sure that the jumper to short ENA to 5V is installed. Also make sure that the jumper above the battery screw terminals is installed (this supplies the L298N chip with 5V regulated from the battery input).
H_BRIDGE_PIN_IN1 = 4
H_BRIDGE_PIN_IN2 = 17

# Maximum time the motor should be allowed to turn for.
MAX_MOTOR_TURN_TIME_SECONDS = 2.5

# Use BCM pin numbering scheme.
GPIO.setmode(GPIO.BCM)

# Set up output pins.
GPIO.setup(H_BRIDGE_PIN_IN1, GPIO.OUT)
GPIO.setup(H_BRIDGE_PIN_IN2, GPIO.OUT)

# Function to turn the motor for a specific number of seconds.
def turn_motor(time_seconds):
    GPIO.output(H_BRIDGE_PIN_IN1, GPIO.HIGH)
    GPIO.output(H_BRIDGE_PIN_IN2, GPIO.LOW)
    time.sleep(time_seconds)
    GPIO.output(H_BRIDGE_PIN_IN1, GPIO.LOW)
    GPIO.output(H_BRIDGE_PIN_IN2, GPIO.LOW)

# Set up Flask web server (remember to not use the development server in production or Internet-facing environments).
app = Flask(__name__)

# Set up form for activating the dog feeder.
@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        try:
            motor_turn_time = float(request.form["motor_turn_time"])
        except KeyError:
            return make_response("Error: You must submit the motor_turn_time form parameter.", 400)
        except ValueError:
            return make_response("Error: motor_turn_time must be a number.", 400)
        if motor_turn_time < 0.0 or motor_turn_time > MAX_MOTOR_TURN_TIME_SECONDS:
            return make_response("Error: motor_turn_time must be between 0.0 and {} seconds.".format(MAX_MOTOR_TURN_TIME_SECONDS), 400)
        turn_motor(motor_turn_time)
        return render_template("completion.html", motor_turn_time = motor_turn_time)

# Run Flask web server.
if __name__ == "__main__":
    try:
        app.run(host = "0.0.0.0", port = 80)
    except KeyboardInterrupt:
        print("Exiting...")
        GPIO.cleanup()
