// Clock & update trackers
function updateClock() {
  const now = new Date();
  const opts = {
    hour:'2-digit', minute:'2-digit', second:'2-digit',
    month:'numeric', day:'numeric', year:'numeric', weekday:'short'
  };
  document.getElementById('clock-time').textContent = now.toLocaleString('en-US', opts);
}
setInterval(updateClock, 1000);
window.addEventListener('DOMContentLoaded', updateClock);

// Dev-popup close
document.querySelector('#dev-popup button')
  .addEventListener('click', () => document.getElementById('dev-popup').style.display = 'none');

// Nav highlighting
document.querySelectorAll('nav a').forEach(a => {
  if (location.pathname.endsWith(a.getAttribute('href'))) a.classList.add('active');
});

// Chart.js init
if (window.Chart) {
  document.querySelectorAll('canvas[id$="Chart"]').forEach(canvas => {
    new Chart(canvas.getContext('2d'), {
      type: 'line',
      data: {
        labels: ['2022','2023','2024','2025'],
        datasets: [{ label:'Value', data:[85,83,78,70], borderColor:'#00ff80', tension:0.4 }]
      },
      options:{
        scales:{ x:{ ticks:{ color:'#00ff80' }}, y:{ ticks:{ color:'#00ff80' }, beginAtZero:false }},
        plugins:{ legend:{ labels:{ color:'#00ff80' } }}
      }
    });
  });
}

// Tabs setup
function setupTabs() {
  document.querySelectorAll('.tabs .tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const box = tab.closest('.box');
      box.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const map = { 'state-tracker':'state-info','netwatch-2025':'netwatch-2025-content' };
      Object.values(map).forEach(id => {
        const el = box.querySelector('#' + id);
        if (el) el.style.display = 'none';
      });
      const target = map[tab.dataset.content];
      if (target && box.querySelector('#'+target)) box.querySelector('#'+target).style.display = 'block';
    });
  });
}
document.addEventListener('DOMContentLoaded', setupTabs);

// State-button setup
document.querySelectorAll('.state-button').forEach(btn => {
  btn.addEventListener('click', () => {
    const box = btn.closest('.box');
    box.querySelectorAll('.state-button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    box.querySelector('#state-info').innerHTML = `<p>${btn.dataset.state} data: (live data)</p>`;
  });
});