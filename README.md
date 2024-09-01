
---

# Face Recognition System

This project implements a simple face recognition system using a client-server architecture. The client runs on a Raspberry Pi and captures images, while the server processes these images to perform face recognition.

## Video Demo 
TODO


## Project Structure

- `face_rec_simple.py`: Contains the main logic for face recognition.
- `rpi_client.py`: Code for the Raspberry Pi client that captures images and sends them to the server.
- `server.py`: Server-side code that receives images from the client and performs face recognition.

## Requirements

- Python 3.x
- OpenCV
- Flask
- Requests
- Picamera (for Raspberry Pi)
- Face Recognition library (`face_recognition`)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/face-recognition-system.git
    cd face-recognition-system
    ```

2. **Install the required libraries:**

    ```bash
    pip install -r requirements.txt
    ```

3. **For Raspberry Pi:**

    ```bash
    sudo apt-get install python3-picamera
    ```

## Usage

### Server

1. **Start the server:**

    ```bash
    python server.py
    ```

    The server will start and listen for incoming connections from the Raspberry Pi client.

### Client (Raspberry Pi)

1. **Run the client:**

    ```bash
    python rpi_client.py
    ```

    The client will capture images using the Raspberry Pi camera and send them to the server for processing.

## Configuration

- **Server Configuration:**

    - The server listens on `0.0.0.0` and port `5000` by default. You can change these settings in the `server.py` file.

- **Client Configuration:**

    - The client is configured to connect to the server at `http://<server-ip>:5000`. Update the server IP address in the `rpi_client.py` file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---
