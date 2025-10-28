// Select canvas and context
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Canvas setup
ctx.fillStyle = 'black';
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.strokeStyle = 'white';
ctx.lineWidth = 15;
ctx.lineCap = 'round';

let drawing = false;

// ---------------- Mouse Events ----------------
canvas.addEventListener('mousedown', (e) => {
  drawing = true;
  draw(e);
});

canvas.addEventListener('mouseup', () => {
  drawing = false;
  ctx.beginPath(); // Prevent unwanted line connections
});

canvas.addEventListener('mousemove', draw);

// ---------------- Touch Events (for mobile) ----------------
canvas.addEventListener('touchstart', (e) => {
  e.preventDefault();
  drawing = true;
  const touch = e.touches[0];
  const x = touch.clientX - canvas.getBoundingClientRect().left;
  const y = touch.clientY - canvas.getBoundingClientRect().top;
  ctx.moveTo(x, y);
});

canvas.addEventListener('touchmove', (e) => {
  e.preventDefault();
  if (!drawing) return;
  const touch = e.touches[0];
  const x = touch.clientX - canvas.getBoundingClientRect().left;
  const y = touch.clientY - canvas.getBoundingClientRect().top;
  ctx.lineTo(x, y);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x, y);
});

canvas.addEventListener('touchend', () => {
  drawing = false;
  ctx.beginPath();
});

// ---------------- Drawing Function ----------------
function draw(e) {
  if (!drawing) return;

  ctx.lineTo(e.offsetX, e.offsetY);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(e.offsetX, e.offsetY);
}

// ---------------- Clear Canvas ----------------
function clearCanvas() {
  ctx.fillStyle = 'black';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
  document.getElementById('result').innerText = 'Predicted Digit: -';
}

// ---------------- Predict Digit ----------------
async function predictDigit() {
  document.getElementById('result').innerText = 'Predicting... ⏳';

  // Convert canvas to image data
  const dataURL = canvas.toDataURL('image/png');

  // Send image to Flask backend
  const response = await fetch('/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: dataURL })
  });

  const result = await response.json();

  // Show prediction result
  document.getElementById('result').innerText = `Predicted ${result.prediction}`;
}

// ---------------- Button Bindings ----------------
document.getElementById('clearBtn').addEventListener('click', clearCanvas);
document.getElementById('predictBtn').addEventListener('click', predictDigit);
