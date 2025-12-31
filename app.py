import os
import numpy as np
from flask import Flask, request, jsonify, render_template
from PIL import Image
import tensorflow as tf

# --------------------------------------------------
# Flask app
# --------------------------------------------------
app = Flask(__name__)

# --------------------------------------------------
# Model path (folder created by model.export())
# --------------------------------------------------
MODEL_PATH = "animals10_model_export"

# --------------------------------------------------
# Load model (Keras 3 compatible)
# --------------------------------------------------
model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

# --------------------------------------------------
# Class labels (CHANGE ORDER IF YOUR TRAINING ORDER IS DIFFERENT)
# --------------------------------------------------
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
# Image preprocessing
# --------------------------------------------------
def preprocess_image(image):
    image = image.convert("RGB")
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# --------------------------------------------------
# Routes
# --------------------------------------------------
@app.route("/")
def home():
    return """
    <h2>Animal Image Classifier</h2>
    <form action="/predict" method="post" enctype="multipart/form-data">
        <input type="file" name="image" required>
        <button type="submit">Predict</button>
    </form>
    """

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    try:
        image = Image.open(file)
        processed = preprocess_image(image)

        predictions = model.predict(processed)
        class_index = np.argmax(predictions)
        confidence = float(predictions[0][class_index])

        return jsonify({
            "prediction": CLASS_NAMES[class_index],
            "confidence": round(confidence * 100, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------------------------------------
# Run (Render compatible)
# --------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
