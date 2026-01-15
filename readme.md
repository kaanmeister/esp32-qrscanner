# ESP32 QR Streamer (USB Serial)

This project turns an ESP32 into a QR code scanner that streams video/data over USB Serial to a Python script on your computer.

## Requirements:

1.  **Hardware:**
    * ESP32 Board (with Camera).
    * USB Data Cable.
2.  **Software:**
    * **VS Code** with **PlatformIO** extension installed.
    * **Python 3** installed on your computer.

## How to Run:

### Step 1: Open the Project
1.  Clone this repository.
2.  Open VS Code.
3.  Go to **File > Open Folder** and select the `esp32-qrscanner` folder.
4.  **Wait** for PlatformIO to initialize. It will automatically download the necessary libraries and toolchains defined in `platformio.ini`.

### Step 2: Upload Code to ESP32
1.  Connect your ESP32 to the computer via USB.
2.  Click the **PlatformIO Alien Icon** on the left sidebar.
3.  Under **Project Tasks**, click **Upload**.

### Step 3: Verify Raw Data 
Before running the Python script, verify the ESP32 is working:
1.  Click the **Plug Icon** (Serial Monitor) at the bottom of VS Code.
2.  If you see a stream of "random symbols" or garbage text scrolling by, It means the ESP32 is successfully sending raw image data.

### Step 4: Run the Viewer
You must CLOSE the Serial Monitor before proceeding. The Python script cannot access the USB port if the Serial Monitor is using it.

1.  Open a new terminal in VS Code.
2.  Install necessary Python libraries (if you haven't yet):
    ```bash
    pip install opencv-python pyserial numpy
    ```
    *(Note: Adjust the libraries above based on what your qr.py actually uses)*
3.  Run the script:
    ```bash
    python qr.py
    ```

### Step 5: Success
A window with the video stream should pop up. You can now point the camera at a QR code to scan it.

---

## Troubleshooting

**Error: "Access is denied" or "Port Busy"**
* You likely left the VS Code Serial Monitor open. Close the terminal panel or click the trash can icon to free up the port, then try running `python qr.py` again.

**Python says "Module not found"**
* Make sure you installed the libraries used in `qr.py` (usually `opencv-python` and `pyserial`).