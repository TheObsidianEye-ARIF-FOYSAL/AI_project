import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image
import logging

# Try to import CORS, but make it optional
try:
    from flask_cors import CORS
    cors_available = True
except ImportError:
    cors_available = False
    logger_temp = logging.getLogger(__name__)
    logger_temp.warning("flask_cors not installed. CORS will not be enabled.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------
# Flask App
# -------------------------------
app = Flask(__name__)
if cors_available:
    CORS(app)  # Enable CORS for cross-origin requests

# -------------------------------
# Load Model (Keras 3 compatible)
# -------------------------------
MODEL_PATH = "animals10_model.keras"

try:
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    logger.info(f"✅ Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    logger.error(f"❌ Error loading model: {e}")
    model = None

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
    """Serve the main HTML page"""
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for Render"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "message": "Animal Classification API is running 🚀"
    })

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

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

        result = {
            "prediction": CLASS_NAMES[predicted_index],
            "confidence": round(confidence * 100, 2)
        }
        
        logger.info(f"✅ Prediction: {result['prediction']} ({result['confidence']}%)")
        return jsonify(result)

    except Exception as e:
        logger.error(f"❌ Prediction error: {e}")
        return jsonify({"error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

# -------------------------------
# Run App (Render compatible)
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "False").lower() == "true"
    
    logger.info(f"🚀 Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
