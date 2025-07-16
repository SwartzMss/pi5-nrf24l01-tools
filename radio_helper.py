import spidev
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24

PIPES = [b"1Node", b"2Node"]


def init_radio() -> NRF24:
    """Initialize and return an NRF24L01 radio instance."""
    GPIO.setmode(GPIO.BCM)
    radio = NRF24(GPIO, spidev.SpiDev())
    radio.begin(0, 22)  # CE on GPIO22, CSN uses CE0
    radio.setPayloadSize(32)
    radio.setChannel(0x76)
    radio.setDataRate(NRF24.BR_1MBPS)
    radio.setPALevel(NRF24.PA_MIN)

    radio.openWritingPipe(list(PIPES[0]))
    radio.openReadingPipe(1, list(PIPES[1]))
    radio.startListening()
    return radio


def send_message(radio: NRF24, text: str) -> None:
    """Send a UTF-8 string as a fixed-size payload."""
    radio.stopListening()
    payload = list(text.encode("utf-8"))
    while len(payload) < 32:
        payload.append(0)
    radio.write(payload)
    radio.startListening()


def check_receive(radio: NRF24) -> str | None:
    """Check for a received message and return it if available."""
    if radio.available():
        received = []
        radio.read(received, radio.getDynamicPayloadSize())
        return bytes(x for x in received if x != 0).decode("utf-8", errors="ignore")
    return None
