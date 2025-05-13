import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()

# Open SPI bus 0, device 0 (corresponding to /dev/spidev0.0)
spi.open(0, 1)  # Bus 0, Device 0

# Set SPI speed and mode
spi.max_speed_hz = 10000  # 50 kHz speed (adjust as necessary)
spi.mode = 0b00  # SPI Mode 0 (CPOL=0, CPHA=0)

# Function to test SPI communication
def test_spi():
    # Send a test byte and receive the response
    test_data = [0x55]  # Example byte to send (0x55)
    response = spi.xfer(test_data)

    # Print sent and received data
    print(f"Sent: {test_data}")
    print(f"Received: {response}")

# Run the test
try:
    print("Testing SPI communication...")
    test_spi()
finally:
    # Close SPI connection
    spi.close()