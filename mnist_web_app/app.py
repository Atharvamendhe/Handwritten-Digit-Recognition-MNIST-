from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import io
import re
import base64
from PIL import Image

app = Flask(__name__)

# Load your trained model (update name if different)
model = load_model("mnist_digit_recognition_model.keras")

# Define homepage
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # Get image data from frontend (Base64)
    data = request.get_json()
    img_data = data['image']

    # Decode the Base64 image
    img_str = re.search(r'base64,(.*)', img_data).group(1)
    img_bytes = base64.b64decode(img_str)

    # Convert to PIL image
    img = Image.open(io.BytesIO(img_bytes)).convert('L')  # Grayscale
    img = img.resize((28, 28))  # MNIST input size
    img = np.array(img)
    img = img.reshape(1, 28, 28, 1)
    img = img / 255.0

    # Predict
    prediction = model.predict(img)
    predicted_digit = np.argmax(prediction)

    return jsonify({'prediction': int(predicted_digit)})

if __name__ == '__main__':
    app.run(debug=True)
