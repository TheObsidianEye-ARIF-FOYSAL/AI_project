import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image
import logging
import gc  # For garbage collection

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
model = None
model_loading = False
model_error = None

def load_model_sync():
    """Load model synchronously"""
    global model, model_loading, model_error
    
    if model is not None:
        return model
    
    if model_loading:
        logger.info("⏳ Model is already being loaded...")
        return None
    
    model_loading = True
    model_error = None
    
    # Check if model file exists
    if not os.path.exists(MODEL_PATH):
        error_msg = f"Model file not found at: {os.path.abspath(MODEL_PATH)}"
        logger.error(f"❌ {error_msg}")
        logger.error(f"Current directory: {os.getcwd()}")
        logger.error(f"Files in current directory: {os.listdir('.')}")
        model_error = error_msg
        model_loading = False
        return None
    
    try:
        logger.info(f"🔄 Loading model from: {os.path.abspath(MODEL_PATH)}")
        logger.info(f"📦 Model file size: {os.path.getsize(MODEL_PATH) / (1024*1024):.2f} MB")
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        logger.info(f"✅ Model loaded successfully!")
        model_loading = False
        return model
    except Exception as e:
        error_msg = f"Error loading model: {str(e)}"
        logger.error(f"❌ {error_msg}")
        logger.error(f"TensorFlow version: {tf.__version__}")
        import traceback
        logger.error(traceback.format_exc())
        model_error = error_msg
        model_loading = False
        return None

# Try to load model at startup (but don't block)
logger.info("🚀 Attempting to load model at startup...")
load_model_sync()

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

@app.route("/test", methods=["GET"])
def test():
    """Test page for debugging"""
    return render_template("test.html")

@app.route("/diagnostic", methods=["GET"])
def diagnostic():
    """Diagnostic page for troubleshooting"""
    return render_template("diagnostic.html")

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for Render"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "model_loading": model_loading,
        "model_error": model_error,
        "message": "Animal Classification API is running 🚀"
    })

@app.route("/model-status", methods=["GET"])
def model_status():
    """Detailed model status endpoint"""
    status = {
        "model_loaded": model is not None,
        "model_loading": model_loading,
        "model_path": MODEL_PATH,
        "model_exists": os.path.exists(MODEL_PATH),
        "current_directory": os.getcwd(),
        "tensorflow_version": tf.__version__
    }
    
    if model_error:
        status["error"] = model_error
    
    if os.path.exists(MODEL_PATH):
        status["model_size_mb"] = round(os.path.getsize(MODEL_PATH) / (1024*1024), 2)
    
    return jsonify(status)

@app.route("/predict", methods=["POST"])
def predict():
    logger.info(f"🔍 Predict endpoint called. Model status: {model is not None}")
    
    # Try to load model if not loaded
    if model is None:
        logger.info("⚠️ Model not loaded, attempting to load...")
        load_model_sync()
        
        if model is None:
            error_msg = model_error or "Model not loaded. Please try again in a moment."
            logger.error(f"❌ Model still not loaded: {error_msg}")
            return jsonify({
                "error": error_msg,
                "model_loading": model_loading,
                "suggestion": "The model is loading. Please wait 10-20 seconds and try again."
            }), 503

    if "file" not in request.files:
        logger.warning("⚠️ No file in request")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        logger.warning("⚠️ Empty filename")
        return jsonify({"error": "Empty filename"}), 400

    try:
        logger.info(f"📁 Processing file: {file.filename}")
        
        # Limit file size to prevent memory issues
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            return jsonify({"error": f"File too large. Max size: {max_size // (1024*1024)}MB"}), 400
        
        logger.info(f"📏 File size: {file_size / 1024:.2f} KB")
        
        image = Image.open(file)
        processed = preprocess_image(image)
        
        # Close image to free memory
        image.close()

        logger.info("🔮 Running prediction...")
        predictions = model.predict(processed, verbose=0)  # verbose=0 to reduce logging
        predicted_index = int(np.argmax(predictions))
        confidence = float(np.max(predictions))

        result = {
            "prediction": CLASS_NAMES[predicted_index],
            "confidence": round(confidence * 100, 2)
        }
        
        # Clean up memory
        del processed
        del predictions
        gc.collect()
        
        logger.info(f"✅ Prediction: {result['prediction']} ({result['confidence']}%)")
        return jsonify(result)

    except Exception as e:
        logger.error(f"❌ Prediction error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Return more specific error messages
        error_msg = str(e)
        if "out of memory" in error_msg.lower() or "oom" in error_msg.lower():
            error_msg = "Server out of memory. Try a smaller image or upgrade server."
        elif "timeout" in error_msg.lower():
            error_msg = "Prediction timeout. Server is overloaded."
        
        return jsonify({"error": error_msg}), 500

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
