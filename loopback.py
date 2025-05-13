import spidev

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000  # 1 MHz
spi.mode = 0

test_data = [0x55]
response = spi.xfer(test_data)

print(f"Sent: {test_data}")
print(f"Received: {response}")

spi.close()
