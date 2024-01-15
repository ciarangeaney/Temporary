import time
import pygatt

# Define the UUIDs for the Heart Rate Service and the Heart Rate Measurement Characteristic
HR_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HR_MEASUREMENT_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

def handle_notification(handle, value_bytes):
    # Parse the heart rate measurement data
    bpm = value_bytes[1]
    print("Heart Rate:", bpm)

def main():
    adapter = pygatt.GATTToolBackend()

    try:
        adapter.start()
        
        # Scan for the heart rate monitor device
        devices = adapter.scan(run_as_root=True, timeout=5)  # Scan for 5 seconds (adjust as needed)
        
        for device in devices:
            if device['address'] == 'YOUR_HEART_RATE_MONITOR_MAC_ADDRESS':
                print("Found Heart Rate Monitor")
                device_address = device['address']
                
                # Connect to the heart rate monitor
                device = adapter.connect(device_address)
                
                # Enable notifications for the Heart Rate Measurement Characteristic
                device.subscribe(HR_MEASUREMENT_UUID, callback=handle_notification)
                
                # Keep the script running to receive notifications
                while True:
                    time.sleep(1)
    
    except KeyboardInterrupt:
        pass
    finally:
        adapter.stop()

if __name__ == "__main__":
    main()
