from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os

app = Flask(__name__)

# Load model once
model = tf.keras.models.load_model("animals10_model.h5")

# Home page
@app.route("/")
def home():
    return render_template("index.html")  # or simple text

# Prediction API
@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    img_file = request.files['file']
    img_path = os.path.join("uploads", img_file.filename)
    img_file.save(img_path)

    # Preprocess image
    IMG_SIZE = 224
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0) / 255.0

    pred = model.predict(img)
    class_names = list(model.class_names) if hasattr(model, "class_names") else ["cane","cavallo","elefante","farfalla","gallina","gatto","mucca","pecora","ragno","scoiattolo"]
    result = class_names[np.argmax(pred)]
    return jsonify({"prediction": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

