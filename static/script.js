/* ═══════════════════════════════════════════════════════
   Screenova – script.js
   Shared JS utilities + page-specific logic
   ═══════════════════════════════════════════════════════ */

/* ── Animate usage bars on load ─────────────────────────── */
function animateBars() {
  document.querySelectorAll('.usage-bar-fill').forEach(bar => {
    const target = bar.dataset.width || '0';
    bar.style.width = '0%';
    setTimeout(() => { bar.style.width = target + '%'; }, 200);
  });

  document.querySelectorAll('.app-bar-fill').forEach(bar => {
    const target = bar.dataset.width || '0';
    bar.style.width = '0%';
    setTimeout(() => { bar.style.width = target + '%'; }, 200);
  });
}

/* ── Count-up animation for stat numbers ─────────────────── */
function countUp(el, target, duration = 1000) {
  let start = 0;
  const step = target / (duration / 16);
  const timer = setInterval(() => {
    start += step;
    if (start >= target) { start = target; clearInterval(timer); }
    el.textContent = Math.floor(start);
  }, 16);
}

function initCountUps() {
  document.querySelectorAll('[data-countup]').forEach(el => {
    const target = parseFloat(el.dataset.countup);
    if (!isNaN(target)) countUp(el, target);
  });
}

/* ── Chatbot ─────────────────────────────────────────────── */
function initChatbot() {
  const window_ = document.getElementById('chatWindow');
  const input   = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');

  if (!window_ || !input || !sendBtn) return;

  function appendBubble(text, type) {
    const div = document.createElement('div');
    div.className = `chat-bubble ${type}`;
    div.innerHTML = text;
    window_.appendChild(div);
    window_.scrollTop = window_.scrollHeight;
  }

  async function sendMessage(msg) {
    if (!msg.trim()) return;
    appendBubble(msg, 'user');
    input.value = '';

    // Typing indicator
    const typing = document.createElement('div');
    typing.className = 'chat-bubble bot';
    typing.innerHTML = '<span class="typing-dots">●●●</span>';
    window_.appendChild(typing);
    window_.scrollTop = window_.scrollHeight;

    try {
      const res = await fetch('/chat_api', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
      });
      const data = await res.json();
      typing.remove();
      appendBubble(data.reply, 'bot');
    } catch {
      typing.remove();
      appendBubble('⚠️ Connection error. Please try again.', 'bot');
    }
  }

  sendBtn.addEventListener('click', () => sendMessage(input.value));
  input.addEventListener('keydown', e => { if (e.key === 'Enter') sendMessage(input.value); });

  // Quick chip buttons
  document.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => sendMessage(chip.textContent));
  });
}

/* ── Usage form: live total calculator ──────────────────── */
function initUsageForm() {
  const inputs = ['instagram', 'youtube', 'whatsapp', 'other'];
  const totalEl = document.getElementById('liveTotal');
  const levelEl = document.getElementById('liveLevel');
  if (!totalEl) return;

  function update() {
    let total = 0;
    inputs.forEach(id => {
      const v = parseInt(document.getElementById(id)?.value || 0);
      if (!isNaN(v)) total += v;
    });
    totalEl.textContent = total;
    const hours = total / 60;
    let level = 'Healthy 🌿', color = '#00e5a0';
    if (hours >= 6)      { level = 'Severe 🚨';   color = '#ff5370'; }
    else if (hours >= 4) { level = 'High 🔥';     color = '#ff6b35'; }
    else if (hours >= 2) { level = 'Moderate ⚠️'; color = '#f9c846'; }
    if (levelEl) { levelEl.textContent = level; levelEl.style.color = color; }
  }

  inputs.forEach(id => {
    document.getElementById(id)?.addEventListener('input', update);
  });
}

/* ── Detox page: range slider live value ─────────────────── */
function initDetoxSlider() {
  const slider = document.getElementById('limitSlider');
  const display = document.getElementById('limitDisplay');
  if (!slider || !display) return;
  slider.addEventListener('input', () => { display.textContent = slider.value; });
}

/* ── Init on DOM ready ──────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  animateBars();
  initCountUps();
  initChatbot();
  initUsageForm();
  initDetoxSlider();
});
