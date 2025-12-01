// Event listener for file input change (when the user selects an image)
document.getElementById('uploadInput').addEventListener('change', async function(event) {
    const formData = new FormData();
    formData.append("image", event.target.files[0]); // Attach the selected file to the form data

    // Send the image file to the Flask backend for prediction
    const response = await fetch('/predict', {
        method: 'POST',
        body: formData,
    });

    // Parse the JSON response from Flask
    const data = await response.json();

    // Display the prediction result and confidence value on the page
    document.getElementById('predictionResult').textContent = data.prediction;
    document.getElementById('confidenceValue').textContent = `${data.confidence}%`;
});
