import io
from tensorflow import keras
import numpy as np
from PIL import Image, ImageOps

from flask import Flask, request, jsonify

model = keras.models.load_model("keras_model.h5")

def transform_image(pillow_image):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    size = (224, 224)
    image = ImageOps.fit(pillow_image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    return data


def predict(x):
    prediction = model.predict(x)
    index = np.argmax(prediction)
    class_names = ['Batik Bali', 'Batik Betawi', 'Batik Cendrawasih', 'Batik Dayak', 'Batik Geblek Renteng', 'Batik Ikat Celup', 'Batik Insang', 'Batik Kawung', 'Batik Lasem', 'Batik Megamendung', 'Batik Batik Pala', 'Batik Parang', 'Batik Poleng', 'Batik Sekar Jagad', 'Batik Tambal']

    class_name = class_names[index]
    confidence_score = prediction[0][index]
    return f"{class_name}|{confidence_score}"

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            image_bytes = file.read()
            pillow_img = Image.open(io.BytesIO(image_bytes))
            tensor = transform_image(pillow_img)
            prediction = predict(tensor)
            data = {"prediction": (prediction.split("|")[0]), "confidence": float(prediction.split("|")[1])}
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})

    return "OK"


if __name__ == "__main__":
    app.run(debug=True)