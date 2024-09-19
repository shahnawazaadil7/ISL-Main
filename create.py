import os
import cv2
import numpy as np
import mediapipe as mp
from sklearn.preprocessing import LabelEncoder
import pickle

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = './data'

def process_images_with_hand_presence():
    data = []
    labels = []
    for dir_ in os.listdir(DATA_DIR):
        dir_path = os.path.join(DATA_DIR, dir_)
        if not os.path.isdir(dir_path):
            continue

        for img_name in os.listdir(dir_path):
            img_path = os.path.join(dir_path, img_name)
            img = cv2.imread(img_path)

            if img is None:
                print(f"Warning: Unable to read image {img_path}")
                continue

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            results = hands.process(img_rgb)

            data_aux = []
            all_x = []
            all_y = []
            hand_presence = 0  # Default to no hands detected

            if results.multi_hand_landmarks:
                hand_presence = len(results.multi_hand_landmarks)  # Set hand presence (1 or 2)
                for hand_landmarks in results.multi_hand_landmarks:
                    x_ = [hand_landmarks.landmark[i].x for i in range(len(hand_landmarks.landmark))]
                    y_ = [hand_landmarks.landmark[i].y for i in range(len(hand_landmarks.landmark))]
                    all_x.extend(x_)
                    all_y.extend(y_)

                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                if len(data_aux) == 42:  # Only one hand detected
                    data_aux.extend([0] * 42)  # Pad for the second hand

                if len(data_aux) == 84:  # Two hands detected
                    pass  # No additional changes needed

                # Append hand presence as the 85th feature
                data_aux.append(hand_presence)

                if len(data_aux) == 85:  # Ensure we have exactly 85 features
                    data.append(data_aux)
                    labels.append(dir_)

    return np.asarray(data), np.asarray(labels)

# Load and process data
data, labels = process_images_with_hand_presence()

# Encode labels
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)

# Save the processed data and label encoder for future use
with open('preprocessed_data.p', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels, 'label_encoder': label_encoder}, f)

print("Preprocessing completed and data saved.")