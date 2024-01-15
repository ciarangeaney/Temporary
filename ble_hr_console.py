from bluepy.btle import Scanner, DefaultDelegate, Peripheral
import struct

# Define the UUIDs for the Heart Rate Service and the Heart Rate Measurement Characteristic
HR_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HR_MEASUREMENT_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# Create a BLE delegate class to handle notifications
class HRNotificationDelegate(DefaultDelegate):
    def handleNotification(self, cHandle, data):
        # Parse the heart rate measurement data
        bpm = struct.unpack('B', data[1])[0]
        print("Heart Rate:", bpm)

def main():
    try:
        # Scan for the heart rate monitor device
        scanner = Scanner().withDelegate(DefaultDelegate())
        devices = scanner.scan(5)  # Scan for 5 seconds (adjust as needed)
        
        for device in devices:
            if device.addr == 'YOUR_HEART_RATE_MONITOR_MAC_ADDRESS':
                print("Found Heart Rate Monitor")
                peripheral = Peripheral(device)
                
                # Enable notifications for the Heart Rate Measurement Characteristic
                peripheral.setDelegate(HRNotificationDelegate())
                hr_service = peripheral.getServiceByUUID(HR_SERVICE_UUID)
                hr_measurement_char = hr_service.getCharacteristics(uuid=HR_MEASUREMENT_UUID)[0]
                peripheral.writeCharacteristic(hr_measurement_char.valHandle + 1, b"\x01\x00", withResponse=True)
                
                # Keep the script running to receive notifications
                while True:
                    if peripheral.waitForNotifications(1.0):
                        continue
    
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
