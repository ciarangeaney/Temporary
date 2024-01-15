from bluepy.btle import Scanner, DefaultDelegate, Peripheral
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_RGBMatrix
import struct

# Define the UUIDs for the Heart Rate Service and the Heart Rate Measurement Characteristic
HR_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HR_MEASUREMENT_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# Create a BLE delegate class to handle notifications
class HRNotificationDelegate(DefaultDelegate):
    def __init__(self, matrix):
        DefaultDelegate.__init__(self)
        self.matrix = matrix

    def handleNotification(self, cHandle, data):
        # Parse the heart rate measurement data
        bpm = struct.unpack('B', data[1])[0]
        self.display_heart_rate(bpm)

    def display_heart_rate(self, bpm):
        # Initialize the RGB matrix
        matrix = self.matrix
        matrix.begin()
        canvas = matrix.CreateFrameCanvas()
        
        # Define font and color
        font = Adafruit_RGBMatrix.Font()
        font.load('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
        textColor = (255, 255, 255)
        
        # Display heart rate on the matrix panel
        matrix.Clear()
        matrix.Fill(0, 0, 0)
        matrix.brightness = 50
        matrix.text(2, 15, textColor, str(bpm), font)
        matrix.swapOnVSync(canvas)

def main():
    # Initialize the RGB matrix
    options = {
        'led-rows': 32,
        'led-cols': 64,
        'led-gpio-mapping': 'adafruit-hat-pwm',
    }
    matrix = Adafruit_RGBMatrix.RGBMatrix(**options)
    
    try:
        # Scan for the heart rate monitor device
        scanner = Scanner().withDelegate(DefaultDelegate())
        devices = scanner.scan(5)  # Scan for 5 seconds (adjust as needed)
        
        for device in devices:
            if device.addr == 'YOUR_HEART_RATE_MONITOR_MAC_ADDRESS':
                print("Found Heart Rate Monitor")
                peripheral = Peripheral(device)
                
                # Enable notifications for the Heart Rate Measurement Characteristic
                peripheral.setDelegate(HRNotificationDelegate(matrix))
                hr_service = peripheral.getServiceByUUID(HR_SERVICE_UUID)
                hr_measurement_char = hr_service.getCharacteristics(uuid=HR_MEASUREMENT_UUID)[0]
                peripheral.writeCharacteristic(hr_measurement_char.valHandle + 1, b"\x01\x00", withResponse=True)
                
                # Keep the script running to receive notifications
                while True:
                    if peripheral.waitForNotifications(1.0):
                        continue
    
    except KeyboardInterrupt:
        pass
    finally:
        matrix.Clear()

if __name__ == "__main__":
    main()
