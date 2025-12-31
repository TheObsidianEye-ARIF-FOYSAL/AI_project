import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

# --------------------------------------------------
# App configuration
# --------------------------------------------------
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
MODEL_PATH = "animals10_model_tf"   # SavedModel directory
IMG_SIZE = 224

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --------------------------------------------------
# Load model ONCE (important for performance)
# --------------------------------------------------
model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

# Class labels (MUST match training order)
CLASS_NAMES = [
    "butterfly",
    "cat",
    "chicken",
    "cow",
    "dog",
    "elephant",
    "horse",
    "sheep",
    "spider",
    "squirrel"
]

# --------------------------------------------------
# Routes
# --------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Load and preprocess image
    img = image.load_img(filepath, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Prediction
    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions)
    confidence = float(np.max(predictions))

    predicted_class = CLASS_NAMES[predicted_index]

    return jsonify({
        "prediction": predicted_class,
        "confidence": round(confidence * 100, 2)
    })

# --------------------------------------------------
# Main
# --------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
