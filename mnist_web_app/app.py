# app.py
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image, ImageOps
import io, re, base64
import os

app = Flask(__name__)

# Load trained model (make sure file exists in project root)
MODEL_PATH = "mnist_cnn_model.keras"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}. Run train_model.py first.")

model = load_model(MODEL_PATH)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        img_data = data.get('image', None)
        if img_data is None:
            return jsonify({'error': 'no image data provided'}), 400

        # extract base64 string
        m = re.search(r'base64,(.*)', img_data)
        if not m:
            return jsonify({'error': 'invalid image data'}), 400
        img_bytes = base64.b64decode(m.group(1))

        # open image and convert to grayscale
        img = Image.open(io.BytesIO(img_bytes)).convert('L')

        # Resize/crop to 28x28 while keeping aspect ratio and centering
        img = ImageOps.fit(img, (28, 28), Image.Resampling.LANCZOS)

        # Invert image because canvas draws white on black; MNIST expects black on white
        img = ImageOps.invert(img)

        # Normalize and reshape
        arr = np.array(img).astype('float32') / 255.0
        arr = arr.reshape(1, 28, 28, 1)

        # Predict
        preds = model.predict(arr)
        pred_class = int(np.argmax(preds))
        confidence = float(np.max(preds)) * 100.0  # in percent

        return jsonify({
            'prediction': pred_class,
            'confidence': round(confidence, 2)
        })
    except Exception as e:
        # for debugging, print the error to console/log
        print("Prediction error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

