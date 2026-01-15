import serial
import time
import cv2
import numpy as np

# CONFIG
PORT = '/dev/ttyUSB0'
BAUD = 115200

print(f"--- CONNECTING TO {PORT} ---")
print("(If this fails, unplug USB, plug back in, and try again)")

try:
    # Open port with flags to prevent resetting the board
    ser = serial.Serial()
    ser.port = PORT
    ser.baudrate = BAUD
    ser.timeout = 0.1
    ser.setDTR(False) # Don't toggle DTR
    ser.setRTS(False) # Don't toggle RTS
    ser.open()
    print("SUCCESS: Port Open.")
except Exception as e:
    print(f"FAIL: {e}")
    exit()

buffer = b""
print("Waiting for data... (Press Ctrl+C to quit)")

last_data_time = time.time()

while True:
    try:
        # 1. Read Data
        if ser.in_waiting > 0:
            chunk = ser.read(ser.in_waiting)
            buffer += chunk
            last_data_time = time.time()
            
            # Print a dot for every 1000 bytes (Visual Progress)
            if len(chunk) > 0:
                print(".", end="", flush=True)

        # 2. Check for Silence (Is the board stuck?)
        if time.time() - last_data_time > 3.0 and len(buffer) == 0:
            print("\n[WARNING] No data received for 3 seconds.")
            print("ACTION: Press the RST button on the board NOW.")
            last_data_time = time.time()

        # 3. Process Image
        start = buffer.find(b'\xff\xd8')
        end = buffer.find(b'\xff\xd9')

        if start != -1 and end != -1:
            if start < end:
                print(f"\n[IMAGE FOUND] Size: {end-start} bytes")
                jpg_data = buffer[start : end + 2]
                
                try:
                    # Decode and Show
                    nparr = np.frombuffer(jpg_data, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    
                    if frame is not None:
                        cv2.imshow('ESP32 Stream', frame)
                        if cv2.waitKey(1) == ord('q'):
                            break
                    else:
                        print(" [Bad Frame]")
                except:
                    print(" [Decode Error]")
                
                # Clean buffer
                buffer = buffer[end + 2:]
            else:
                buffer = buffer[end + 2:]

    except KeyboardInterrupt:
        break

ser.close()