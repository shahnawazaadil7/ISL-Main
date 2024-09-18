import os
import cv2
import mediapipe as mp
import numpy as np
import pickle
from flask import Flask, Response, render_template, jsonify, request, send_from_directory
import time

app = Flask(__name__)

# Path to the folder containing the hand sign images
HAND_SIGN_FOLDER = "hand_signs/"

# Labels dictionary for sign to word mapping
labels_dict = {
    'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E',
    'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J',
    'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O',
    'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T',
    'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y',
    'Z': 'Z', '1': '1', '2': '2', '3': '3', '4': '4',
    '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    '0': '0'
}

# Load model
model_dict = pickle.load(open('./dnn_model.p', 'rb'))
model = model_dict['model']
label_encoder = model_dict['label_encoder']

# Set up MediaPipe for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.3)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def process_frame(frame):
    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    data_aux = []
    all_x = []
    all_y = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x_ = [hand_landmarks.landmark[i].x for i in range(len(hand_landmarks.landmark))]
            y_ = [hand_landmarks.landmark[i].y for i in range(len(hand_landmarks.landmark))]
            all_x.extend(x_)
            all_y.extend(y_)

            # Add normalized hand landmark positions
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        # Ensure we have 84 features
        if len(data_aux) == 42:
            data_aux.extend([0] * 42)  # Pad for the second hand
        elif len(data_aux) != 84:
            print(f"Feature length mismatch: {len(data_aux)}")
            return 'No sign detected'

        # Predict using the DNN model
        try:
            data_aux = np.asarray([data_aux])  # Reshape for a batch of 1
            probs = model.predict(data_aux)[0]
            predicted_label_index = np.argmax(probs)
            predicted_label = label_encoder.inverse_transform([predicted_label_index])[0]
            max_prob = np.max(probs)

            if max_prob >= 0.4:
                detected_sign = labels_dict.get(predicted_label, 'No sign detected')
                return detected_sign
        except Exception as e:
            print(f"Prediction error: {e}")

    return ' '

app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def generate():
        cap = cv2.VideoCapture(1)  # Ensure this is the correct index for your webcam
        if not cap.isOpened():
            print("Error: Could not open video capture.")
            return
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            detected_sign = process_frame(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                break
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        cap.release()

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_signs')
def get_signs():
    cap = cv2.VideoCapture(1)  # Ensure this is the correct index for your webcam
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Failed to capture image from webcam")
        return jsonify({"detected_sign": ''})

    detected_sign = process_frame(frame)
    return jsonify({"detected_sign": detected_sign})


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/isl_to_english')
def isl_to_english():
    return render_template('isl_to_english.html')

@app.route('/english_to_isl')
def english_to_isl():
    return render_template('english_to_isl.html')

VIDEO_DIRECTORY = '/Users/shahnawazaadil/Desktop/ISL/English words'
@app.route('/learning')
def learning():
    return render_template('learning.html')

@app.route('/videos/<letter>', methods=['GET'])
def get_videos(letter):
    video_folder = os.path.join(VIDEO_DIRECTORY, letter.upper())
    if os.path.exists(video_folder):
        videos = []
        for video_file in os.listdir(video_folder):
            if video_file.endswith('.mp4'):
                videos.append({
                    'name': os.path.splitext(video_file)[0],  # Name of the video without extension
                    'path': f'/videos/{letter}/{video_file}'  # Corrected path to serve videos
                })
        return jsonify(videos)
    return jsonify([])

# Route to serve actual video files
@app.route('/videos/<letter>/<filename>')
def serve_video(letter, filename):
    return send_from_directory(os.path.join(VIDEO_DIRECTORY, letter.upper()), filename)

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

if __name__ == '__main__':
    app.run(debug=True)