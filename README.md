# RGB Control App

This repository contains the source code for an RGB control application developed in Python using the customtkinter, colorpicker, serial_connection, and microphone libraries. The application allows users to control the color of RGB LEDs connected to an Arduino board, either through a graphical color picker or by voice commands.

## Features

- **Arduino Connection:** Automatically detects available USB ports and allows connection to the Arduino board for sending color change commands.
- **Color Picker:** Includes an intuitive color picker that lets users select the desired LED color while displaying the result in real-time.
- **Voice Commands:** The application supports voice commands in Portuguese and English to change LED colors. Colors like "red," "green," "blue," and others are recognized.
- **Color Display and RGB Code:** Displays the selected color and its RGB code, with an option to copy the RGB code to the clipboard.
- **Connection Alerts:** Shows visual alerts if there is any issue connecting to the Arduino board.

## Requirements

- Python 3.x
- Python Libraries: customtkinter, colorpicker, serial_connection, microphone, and other dependencies as needed.
- Arduino board with connected RGB LEDs.
- KY-037 module.

## How to Run

Clone this repository.
Install the required dependencies.

## Run the main file to start the application

```
python rgb_control_app.py
```
- Connect your Arduino board, select the correct port in the application interface, and start controlling the RGB LEDs.

![image](https://github.com/user-attachments/assets/e1d103e8-9b31-4b01-97e3-2198ad8d360e)

## Contributions
Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

This description provides a clear overview of the project, its features, and how to use it, making it ideal for the main page of your GitHub repository.
