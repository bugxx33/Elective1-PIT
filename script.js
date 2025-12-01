// Handle image upload and send it to the Flask backend for prediction
document.getElementById('uploadInput').addEventListener('change', async function(event) {
  const formData = new FormData();
  formData.append("image", event.target.files[0]);

  // Send the image to the Flask backend
  const response = await fetch('/predict', {
    method: 'POST',
    body: formData,
  });

  const data = await response.json();

  // Display the result on the page
  document.getElementById('predictionResult').textContent = data.prediction;
  document.getElementById('confidenceValue').textContent = `${data.confidence}%`;
});
