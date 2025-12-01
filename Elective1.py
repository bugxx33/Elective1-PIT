import os
import io
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
# Prefer tensorflow.keras but fall back to standalone `keras` if needed
try:
    from tensorflow.keras.models import load_model
    _load_model_import_error = None
except Exception:
    try:
        from keras.models import load_model
        _load_model_import_error = None
    except Exception as e:
        load_model = None
        _load_model_import_error = e
import numpy as np
from PIL import Image

# Use project root as template folder so `index.html` at repo root can be served
app = Flask(__name__, template_folder='.')

# Path to the model file (ensure the file path is correct)
# The model in this repo is under `models/potato_leaf_cnn_2.h5` per workspace
model_path = os.path.join('models', 'potato_leaf_cnn_2.h5')
# Lazy-load the model at first request to avoid import-time TensorFlow issues
model = None

def get_model():
    global model
    if model is None:
        if load_model is None:
            raise ImportError(
                "Could not import `load_model` from tensorflow.keras or keras."
                f" Original error: {_load_model_import_error}"
            )
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        model = load_model(model_path)
    return model

# Route for the main page
@app.route('/')
def home():
    return render_template('index.html')

# Route for uploading and predicting
@app.route('/predict', methods=['POST'])
def predict():
    # Get the uploaded image file
    file = request.files['image']

    # Preprocess the image
    img = Image.open(io.BytesIO(file.read()))
    img = img.resize((224, 224))  # Resize to the input shape the model expects
    img = np.array(img) / 255.0  # Normalize the image
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    
    # Predict using the model (load lazily)
    model = get_model()
    prediction = model.predict(img)
    predicted_class = np.argmax(prediction, axis=1)
    
    # Return the predicted class and confidence score
    return jsonify({
        'prediction': str(predicted_class[0]),
        'confidence': float(np.max(prediction)) * 100
    })

if __name__ == '__main__':
    app.run(debug=True)
