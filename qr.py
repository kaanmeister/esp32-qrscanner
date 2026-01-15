import serial
import time
import cv2
import numpy as np
from pyzbar.pyzbar import decode

# --- CONFIGURATION ---
PORT = '/dev/ttyUSB0'
BAUD = 115200

print(f"--- CONNECTING TO {PORT} ---")
print("Focus the camera on a QR code!")

try:
    # 1. Open connection safely (Disable DTR/RTS to prevent reset)
    ser = serial.Serial()
    ser.port = PORT
    ser.baudrate = BAUD
    ser.timeout = 0.1
    ser.setDTR(False) 
    ser.setRTS(False)
    ser.open()
    print("SUCCESS: Connected. Waiting for video...")
except Exception as e:
    print(f"FAIL: {e}")
    exit()

buffer = b""

while True:
    try:
        # 2. Read Data
        if ser.in_waiting > 0:
            buffer += ser.read(ser.in_waiting)
        
        # 3. Find JPEG Frame
        start = buffer.find(b'\xff\xd8')
        end = buffer.find(b'\xff\xd9')

        if start != -1 and end != -1:
            if start < end:
                jpg_data = buffer[start : end + 2]
                
                try:
                    # Decode Image
                    nparr = np.frombuffer(jpg_data, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    
                    if frame is not None:
                        # --- QR SCANNING LOGIC ---
                        decoded_objects = decode(frame)
                        
                        for obj in decoded_objects:
                            # A. Extract Data
                            qr_data = obj.data.decode("utf-8")
                            print(f" >> QR FOUND: {qr_data}")
                            
                            # B. Draw Green Box
                            pts = np.array(obj.polygon, dtype=np.int32)
                            cv2.polylines(frame, [pts], True, (0, 255, 0), 3)
                            
                            # C. Draw Text on Screen
                            cv2.putText(frame, qr_data, (pts[0][0], pts[0][1] - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
                        # Show Video
                        cv2.imshow('QR Scanner', frame)
                except:
                    pass
                
                # Clear processed data
                buffer = buffer[end + 2:]
            else:
                buffer = buffer[end + 2:]

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except KeyboardInterrupt:
        break

ser.close()
cv2.destroyAllWindows()