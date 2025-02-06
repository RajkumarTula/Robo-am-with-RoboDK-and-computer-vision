# Gesture-Based Robotic Arm Control using Computer Vision and RoboDK

## Overview
This project utilizes **computer vision** and **robotic simulation** to control two ABB robotic arms based on **hand gestures** detected via a webcam. The system integrates **MediaPipe for hand tracking**, **OpenCV for image processing**, and **RoboDK for robotic simulation and movement execution**. The goal is to create an intuitive and contactless control system for industrial robots using simple hand gestures.

## Technologies Used
- **OpenCV** – For video capture and image processing
- **MediaPipe** – For real-time hand tracking and landmark detection
- **RoboDK** – For simulating and controlling ABB robotic arms
- **Python** – As the core programming language

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- RoboDK installed and running
- A webcam for hand gesture recognition

### Install Dependencies
```bash
pip install opencv-python mediapipe robodk numpy
```

## Usage
1. **Run the script:**
   ```bash
   python gesture_control.py
   ```
2. Ensure the webcam is turned on.
3. Perform hand gestures to control the robotic arms.
   - Left hand gestures control the **white ABB IRB 1100**.
   - Right hand gestures control the **orange ABB IRB 140**.
4. The recognized gesture triggers a corresponding robot movement.

## Hand Gesture Mapping
Each number of raised fingers corresponds to a predefined movement:

| Gesture (Left Hand) | Action (White ABB IRB 1100) |
|---------------------|---------------------------|
| 1 Finger Up        | Move to Position W1       |
| 2 Fingers Up       | Move to Position W2       |
| ...                | ...                        |
| 11 Fingers Up      | Move to Position W11      |

| Gesture (Right Hand) | Action (Orange ABB IRB 140) |
|----------------------|---------------------------|
| 1 Finger Up         | Move to Position O1       |
| 2 Fingers Up        | Move to Position O2       |
| ...                 | ...                        |
| 11 Fingers Up       | Move to Position O11      |

## Features
- **Real-time Hand Gesture Detection** using MediaPipe.
- **Smooth robotic arm control** through RoboDK.
- **Hands-free operation** for industrial automation and robotics applications.

## Potential Applications
- **Industrial Automation** – Hands-free robotic control in factories.
- **Assistive Technology** – Helping individuals with disabilities interact with robots.
- **Remote Manipulation** – Controlling robots in hazardous environments.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [MediaPipe](https://developers.google.com/mediapipe)
- [OpenCV](https://opencv.org/)
- [RoboDK](https://robodk.com/)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

