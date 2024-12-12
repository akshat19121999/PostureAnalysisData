import asyncio
from bleak import BleakScanner, BleakClient

async def scan_and_read():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()

    if not devices:
        print("No devices found. Make sure your BLE device is discoverable.")
        return

    print("\nDevices found:")
    for i, device in enumerate(devices):
        print(f"{i + 1}. {device.name} ({device.address})")

    for device in devices:
        if device.name:
            print(f"\nAttempting to connect to: {device.name} ({device.address})")
            try:
                async with BleakClient(device.address) as client:
                    if client.is_connected:
                        print(f"Connected to {device.name}")
                        
                        print("Discovering services...")
                        for service in client.services:
                            print(f"[Service] {service.uuid}: {service.description}")
                            for char in service.characteristics:
                                print(f"  [Characteristic] {char.uuid}: {char.properties}")
                                
                                if "read" in char.properties:
                                    try:
                                        value = await client.read_gatt_char(char)
                                        print(f"    Data from {char.uuid}: {value}")
                                    except Exception as e:
                                        print(f"    Failed to read {char.uuid}: {e}")

                                if "notify" in char.properties:
                                    try:
                                        def notification_handler(sender, data):
                                            print(f"    Notification from {sender}: {data}")
                                        
                                        await client.start_notify(char, notification_handler)
                                        await asyncio.sleep(5)  # Wait for notifications
                                        await client.stop_notify(char)
                                    except Exception as e:
                                        print(f"    Failed to set notifications for {char.uuid}: {e}")
            except Exception as e:
                print(f"Failed to connect to {device.name} ({device.address}): {e}")

    print("\nScanning and reading complete.")

asyncio.run(scan_and_read())
