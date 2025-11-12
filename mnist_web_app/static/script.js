// static/script.js
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Setup canvas
ctx.fillStyle = 'black';
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.strokeStyle = 'white';
ctx.lineWidth = 18;          // thicker stroke helps prediction
ctx.lineCap = 'round';

let drawing = false;

// Mouse events
canvas.addEventListener('mousedown', (e) => {
  drawing = true;
  drawMouse(e);
});
canvas.addEventListener('mouseup', () => {
  drawing = false;
  ctx.beginPath();
});
canvas.addEventListener('mousemove', drawMouse);

function drawMouse(e) {
  if (!drawing) return;
  ctx.lineTo(e.offsetX, e.offsetY);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(e.offsetX, e.offsetY);
}

// Touch events (mobile)
canvas.addEventListener('touchstart', (e) => {
  e.preventDefault();
  drawing = true;
  const t = e.touches[0];
  const rect = canvas.getBoundingClientRect();
  ctx.moveTo(t.clientX - rect.left, t.clientY - rect.top);
});
canvas.addEventListener('touchmove', (e) => {
  e.preventDefault();
  if (!drawing) return;
  const t = e.touches[0];
  const rect = canvas.getBoundingClientRect();
  const x = t.clientX - rect.left;
  const y = t.clientY - rect.top;
  ctx.lineTo(x, y);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x, y);
});
canvas.addEventListener('touchend', () => {
  drawing = false;
  ctx.beginPath();
});

// Clear canvas
function clearCanvas() {
  ctx.fillStyle = 'black';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
  document.getElementById('result').innerText = 'Predicted Digit: -';
}

// Predict digit
async function predictDigit() {
  document.getElementById('result').innerText = 'Predicting... ⏳';
  const dataURL = canvas.toDataURL('image/png');

  try {
    const resp = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: dataURL })
    });
    const result = await resp.json();
    if (result.error) {
      document.getElementById('result').innerText = `Error: ${result.error}`;
      return;
    }
    document.getElementById('result').innerText =
      `Predicted ${result.prediction} (Confidence: ${result.confidence}%)`;
  } catch (err) {
    document.getElementById('result').innerText = `Request failed: ${err}`;
  }
}

// Button bindings
document.getElementById('clearBtn').addEventListener('click', clearCanvas);
document.getElementById('predictBtn').addEventListener('click', predictDigit);
