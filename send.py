#!/usr/bin/env python3
"""Simple NRF24L01 transmitter example for Raspberry Pi 5."""
import time
import spidev
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24


def main():
    # Pipes for communication (5 bytes each)
    pipes = [b"1Node", b"2Node"]

    GPIO.setmode(GPIO.BCM)

    # CE on GPIO22, CSN on SPI0_CE0 (BCM8)
    radio = NRF24(GPIO, spidev.SpiDev())
    radio.begin(0, 22)  # ce=22, csn=0 -> CE0
    radio.setPayloadSize(32)
    radio.setChannel(0x76)
    radio.setDataRate(NRF24.BR_1MBPS)
    radio.setPALevel(NRF24.PA_MIN)

    radio.openWritingPipe(list(pipes[0]))
    radio.openReadingPipe(1, list(pipes[1]))
    radio.stopListening()

    while True:
        message = list("Hello from Pi5")
        # Pad message to 32 bytes
        while len(message) < 32:
            message.append(0)

        radio.write(message)
        print("Sent:", ''.join(chr(x) for x in message if x != 0))
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()
