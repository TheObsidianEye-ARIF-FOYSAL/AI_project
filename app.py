import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from PIL import Image

# -------------------------------
# Flask App
# -------------------------------
app = Flask(__name__)

# -------------------------------
# Load Model (Keras 3 compatible)
# -------------------------------
MODEL_PATH = "animals10_model.keras"

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

# -------------------------------
# Class Names (CHANGE if needed)
# -------------------------------
CLASS_NAMES = [
    "cat", "dog", "horse", "sheep", "cow",
    "elephant", "butterfly", "chicken",
    "spider", "squirrel"
]

# -------------------------------
# Image Preprocessing
# -------------------------------
def preprocess_image(image):
    image = image.convert("RGB")
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# -------------------------------
# Routes
# -------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "Animal Classification API is live 🚀"
    })

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        image = Image.open(file)
        processed = preprocess_image(image)

        predictions = model.predict(processed)
        predicted_index = int(np.argmax(predictions))
        confidence = float(np.max(predictions))

        return jsonify({
            "prediction": CLASS_NAMES[predicted_index],
            "confidence": round(confidence * 100, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# Run App (Render compatible)
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
