import cv2
import serial
import numpy as np
import time

#CONFIGURATION
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200  

print(f"--- CONNECTING TO {SERIAL_PORT} ---")

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print("SUCCESS! Waiting for video stream...")
except Exception as e:
    print(f"ERROR: {e}")
    print("TIP: Is the VS Code Serial Monitor still open? CLOSE IT!")
    exit()

data_buffer = b""

while True:
    try:
        if ser.in_waiting > 0:
            data_buffer += ser.read(ser.in_waiting)
        
        # JPEG Start (0xFFD8) and End (0xFFD9)
        start = data_buffer.find(b'\xff\xd8')
        end = data_buffer.find(b'\xff\xd9')

        if start != -1 and end != -1:
            if start < end:
                jpg_data = data_buffer[start : end + 2]
                try:
                    nparr = np.frombuffer(jpg_data, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    if frame is not None:
                        cv2.imshow('ESP32 Stream', frame)
                except:
                    pass
                data_buffer = data_buffer[end + 2:]
            else:
                data_buffer = data_buffer[end + 2:]

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except KeyboardInterrupt:
        break

ser.close()
cv2.destroyAllWindows()