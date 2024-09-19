'''Explanation:

	•	Directory Setup: The code first checks and creates the necessary directories for storing the images.
	•	Camera Initialization: It then tries to access the camera to capture video frames. If the camera isn’t accessible, the program exits.
	•	Data Collection: The code enters a loop for each class, where it prompts the user to get ready before collecting images. Once ready, it captures a specified number of images and saves them in the appropriate directory.
	•	Completion: After collecting images for all classes, the program releases the camera and closes any OpenCV windows.'''

import os
import cv2

DATA_DIR = './data'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 36
dataset_size = 100

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Camera not accessible.")
    exit()

for j in range(number_of_classes):
    class_dir = os.path.join(DATA_DIR, str(j))
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    print(f'Collecting data for class {j}')

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            continue

        cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
        cv2.imshow('frame', frame)

        if cv2.waitKey(25) == ord('q'):
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                continue

            cv2.putText(frame, 'Get ready...', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
            cv2.imshow('frame', frame)
            cv2.waitKey(2000)
            break

    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            continue

        cv2.imshow('frame', frame)
        cv2.waitKey(25)

        file_path = os.path.join(class_dir, f'{counter}.jpg')
        cv2.imwrite(file_path, frame)
        counter += 1

print("Data collection complete.")
cap.release()
cv2.destroyAllWindows()