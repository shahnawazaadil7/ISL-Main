import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load the preprocessed data
with open('preprocessed_data.p', 'rb') as f:
    preprocessed_data = pickle.load(f)

data = preprocessed_data['data']
labels = preprocessed_data['labels']
label_encoder = preprocessed_data['label_encoder']

# Check data shapes
print(f"Data shape: {np.array(data).shape}")
print(f"Labels shape: {np.array(labels).shape}")

# Split the data into train and test sets
x_train, x_test, y_train, y_test = train_test_split(
    data, labels, test_size=0.2, shuffle=True, stratify=labels
)

# Convert labels to one-hot encoding (for multi-class classification)
num_classes = len(np.unique(labels))  # Use labels to get the number of classes
y_train = tf.keras.utils.to_categorical(y_train, num_classes)
y_test = tf.keras.utils.to_categorical(y_test, num_classes)

# Define a Dense Neural Network (DNN) model
model = Sequential()

# Input layer (85 features: 84 landmarks + 1 hand presence feature)
model.add(Dense(128, input_shape=(85,), activation='relu'))

# Hidden layers
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.3))  # Dropout to prevent overfitting
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.3))

# Output layer
model.add(Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(x_train, y_train, batch_size=32, epochs=20, validation_data=(x_test, y_test))

# Evaluate the model
y_predict = np.argmax(model.predict(x_test), axis=-1)
y_test_labels = np.argmax(y_test, axis=-1)
accuracy = accuracy_score(y_test_labels, y_predict)
print('{}% of samples were classified correctly!'.format(accuracy * 100))

# Save the trained model
model.save('dnn_model_with_hand_presence.h5')

# Save the label encoder
with open('label_encoder.p', 'wb') as f:
    pickle.dump(label_encoder, f)

print("Model training completed and saved.")