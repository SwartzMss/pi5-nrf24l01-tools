#!/usr/bin/env python3
"""Combined example using NRF24L01 on Raspberry Pi 5."""
import time
import RPi.GPIO as GPIO
from radio_helper import init_radio, send_message, check_receive


def main() -> None:
    radio = init_radio()
    count = 0
    try:
        while True:
            text = f"Ping {count}"
            send_message(radio, text)
            print("Sent:", text)
            time.sleep(0.5)
            reply = check_receive(radio)
            if reply:
                print("Received:", reply)
            time.sleep(1)
            count += 1
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
