import cv2 as cv
import mediapipe as mp
import threading
from robodk import robolink  # RoboDK API

# Initialize RoboDK API
RDK = robolink.Robolink()

# Load Robot
orange = RDK.Item('KUKA KR 10 R900 sixx')

# Define target positions
targets = [RDK.Item(f'Target {i}') for i in range(1, 7)]

# Define programs
programs = {
    1: RDK.Item("picking", robolink.ITEM_TYPE_PROGRAM),
    2: RDK.Item("place", robolink.ITEM_TYPE_PROGRAM),
    3: RDK.Item("main", robolink.ITEM_TYPE_PROGRAM),
    4: RDK.Item("Prog1", robolink.ITEM_TYPE_PROGRAM)  # New program
}

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()

# Video Capture with higher FPS
vid = cv.VideoCapture(0)
vid.set(cv.CAP_PROP_FPS, 60)  # Attempt to increase FPS
vid.set(cv.CAP_PROP_FRAME_WIDTH, 640)  # Reduce resolution for performance
vid.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky

def recognize_hands(x_coord, y_coord):
    """Recognizes hand gestures based on finger positions."""
    num_arr = [1 if abs(x_coord[13] - x_coord[4]) > 50 else 0]  # Thumb
    num_arr += [1 if y_coord[f] < y_coord[f - 2] else 0 for f in finger_tips]  # Fingers
    return tuple(num_arr)  # Convert to tuple for dictionary lookup

# Define gesture mappings
gesture_targets = {
    (0, 1, 0, 0, 0): 0,
    (0, 1, 1, 0, 0): 1,
    (0, 1, 1, 1, 0): 2,
    (0, 1, 1, 1, 1): 3,
    (1, 1, 1, 1, 1): 4,
    (1, 0, 0, 0, 0): 5,
}

gesture_programs = {
    (0, 1, 0, 0, 0): 1,
    (0, 1, 1, 0, 0): 2,
    (0, 1, 1, 1, 0): 3,  # Triggers program3, then program4
}

# Store the last processed gesture to avoid redundant calculations
last_left_gesture = None
last_right_gesture = None

# Thread-safe read
frame = None
ret = False

def capture_frame():
    global frame, ret
    while True:
        ret, frame = vid.read()

# Start video capture in a separate thread
thread = threading.Thread(target=capture_frame, daemon=True)
thread.start()

while True:
    if not ret:
        continue

    img = cv.flip(frame, 1)
    h, w, _ = img.shape
    result = hands.process(cv.cvtColor(img, cv.COLOR_BGR2RGB))

    left_hand, right_hand = None, None
    lx, ly, rx, ry = [], [], [], []

    if result.multi_hand_landmarks:
        for i, landmarks in enumerate(result.multi_hand_landmarks):
            label = result.multi_handedness[i].classification[0].label
            if label == "Left":
                left_hand = landmarks
                lx = [int(w * lm.x) for lm in landmarks.landmark]
                ly = [int(h * lm.y) for lm in landmarks.landmark]
            elif label == "Right":
                right_hand = landmarks
                rx = [int(w * lm.x) for lm in landmarks.landmark]
                ry = [int(h * lm.y) for lm in landmarks.landmark]

            # Draw landmarks only when necessary
            if last_left_gesture != lx or last_right_gesture != rx:
                mp_draw.draw_landmarks(img, landmarks, mp_hands.HAND_CONNECTIONS)

    # Process left hand (target selection)
    if lx:
        gesture = recognize_hands(lx, ly)
        if gesture != last_left_gesture and gesture in gesture_targets:
            index = gesture_targets[gesture]
            cv.putText(img, f'Left: Target {index + 1}', (50, 100), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), thickness=1)
            if orange.Valid() and targets[index].Valid():
                orange.MoveJ(targets[index])
            last_left_gesture = gesture  # Cache the gesture for comparison

    # Process right hand (program execution)
    if rx:
        gesture = recognize_hands(rx, ry)
        if gesture != last_right_gesture and gesture in gesture_programs:
            program_index = gesture_programs[gesture]
            cv.putText(img, f'Right: Running Program {program_index}', (450, 100), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), thickness=1)
            if programs[program_index].Valid():
                programs[program_index].RunProgram()
                if program_index == 3 and programs[4].Valid():
                    programs[4].RunProgram()  # Run program4 after program3
            last_right_gesture = gesture  # Cache the gesture for comparison

    # Display image
    cv.imshow('Hand Control', img)

    # Exit on 'q' key press
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
vid.release()
cv.destroyAllWindows()
