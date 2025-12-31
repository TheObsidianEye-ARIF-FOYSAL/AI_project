from flask import Flask, request, jsonify, render_template
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import gdown

# =========================
# CONFIGURATION
# =========================
app = Flask(__name__)

MODEL_PATH = "animals10_model.h5"
MODEL_URL = "YOUR_MODEL_DOWNLOAD_LINK_HERE"  # Replace with your Google Drive / cloud link

# Download the model if it doesn't exist
if not os.path.exists(MODEL_PATH):
    print("Downloading model...")
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

# Load the model
model = tf.keras.models.load_model(MODEL_PATH)

# Get class names from training dataset (replace with your classes)
class_names = ['butterfly', 'cat', 'chicken', 'cow', 'dog', 'elephant', 'horse', 'sheep', 'spider', 'squirrel']

IMG_SIZE = 224  # Image size used in training

# =========================
# ROUTES
# =========================
@app.route('/')
def index():
    return render_template('index.html')  # HTML page for uploading image

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file temporarily
    filepath = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    # Process the image
    img = image.load_img(filepath, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Predict
    pred = model.predict(img_array)
    predicted_class = class_names[np.argmax(pred)]
    confidence = float(np.max(pred))

    # Remove temporary file
    os.remove(filepath)

    return jsonify({
        "predicted_class": predicted_class,
        "confidence": confidence
    })

# =========================
# RUN THE APP
# =========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
