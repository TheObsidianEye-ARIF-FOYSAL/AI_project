from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

model = load_model("animals10_model.h5")
class_names = [
    'butterfly', 'cat', 'chicken', 'cow',
    'dog', 'elephant', 'horse', 'sheep',
    'spider', 'squirrel'
]

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files['image']
    img_path = "temp.png"
    file.save(img_path)

    img = image.load_img(img_path, target_size=(224,224))
    img = image.img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)
    label = class_names[np.argmax(pred)]

    os.remove(img_path)

    return jsonify({"prediction": label})

if __name__ == "__main__":
    app.run(debug=True)
