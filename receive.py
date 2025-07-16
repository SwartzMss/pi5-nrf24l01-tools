#!/usr/bin/env python3
"""Simple NRF24L01 receiver example for Raspberry Pi 5."""
import time
import spidev
import lgpio as GPIO
from lib_nrf24 import NRF24


def main():
    pipes = [b"1Node", b"2Node"]
    GPIO.setmode(GPIO.BCM)

    radio = NRF24(GPIO, spidev.SpiDev())
    radio.begin(0, 22)  # ce=22, csn=0 -> CE0
    radio.setPayloadSize(32)
    radio.setChannel(0x76)
    radio.setDataRate(NRF24.BR_1MBPS)
    radio.setPALevel(NRF24.PA_MIN)

    radio.openWritingPipe(list(pipes[1]))
    radio.openReadingPipe(1, list(pipes[0]))
    radio.startListening()

    while True:
        if radio.available():
            received = []
            radio.read(received, radio.getDynamicPayloadSize())
            msg = ''.join(chr(x) for x in received if x != 0)
            print("Received:", msg)
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()
