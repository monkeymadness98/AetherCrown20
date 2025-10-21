// Time Zone Clocks — plain JS, Intl-based, DST-aware
const DEFAULT_ZONES = [
  'UTC',
  Intl.DateTimeFormat().resolvedOptions().timeZone || 'local',
  'America/New_York',
  'Europe/London',
  'Asia/Tokyo',
  'Australia/Sydney'
];

const clocksEl = document.getElementById('clocks');
const addBtn = document.getElementById('add-btn');
const tzInput = document.getElementById('tz-input');
const presetSelect = document.getElementById('preset-select');
const hourToggle = document.getElementById('hour-toggle');

let zones = JSON.parse(localStorage.getItem('tz_zones') || 'null') || DEFAULT_ZONES.slice();
let use24 = JSON.parse(localStorage.getItem('tz_24') || 'false');

hourToggle.checked = !!use24;

function save() {
  localStorage.setItem('tz_zones', JSON.stringify(zones));
  localStorage.setItem('tz_24', JSON.stringify(use24));
}

function fmtDateForZone(d, tz) {
  try {
    const opts = { timeZone: tz, hour12: !use24, hour: 'numeric', minute: '2-digit', second: '2-digit' };
    return new Intl.DateTimeFormat(undefined, opts).format(d);
  } catch (e) {
    return 'Invalid TZ';
  }
}

function fmtLongForZone(d, tz) {
  try {
    const opts = { timeZone: tz, weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
    return new Intl.DateTimeFormat(undefined, opts).format(d);
  } catch (e) {
    return '';
  }
}

function render() {
  clocksEl.innerHTML = '';
  const now = new Date();
  zones.forEach((tz, i) => {
    const card = document.createElement('section');
    card.className = 'clock';
    const zoneRow = document.createElement('div');
    zoneRow.className = 'zone';

    const zoneName = document.createElement('div');
    zoneName.textContent = tz === 'local' ? 'Local' : tz;

    const actions = document.createElement('div');
    actions.className = 'actions';

    const removeBtn = document.createElement('button');
    removeBtn.className = 'btn remove';
    removeBtn.title = 'Remove zone';
    removeBtn.textContent = 'Remove';
    removeBtn.addEventListener('click', () => {
      zones.splice(i, 1);
      save();
      render();
    });

    actions.appendChild(removeBtn);
    zoneRow.appendChild(zoneName);
    zoneRow.appendChild(actions);

    const timeEl = document.createElement('div');
    timeEl.className = 'time';
    timeEl.textContent = fmtDateForZone(now, tz === 'local' ? Intl.DateTimeFormat().resolvedOptions().timeZone : tz);

    const dateEl = document.createElement('div');
    dateEl.className = 'date';
    dateEl.textContent = fmtLongForZone(now, tz === 'local' ? Intl.DateTimeFormat().resolvedOptions().timeZone : tz);

    card.appendChild(zoneRow);
    card.appendChild(timeEl);
    card.appendChild(dateEl);
    clocksEl.appendChild(card);
  });
}

// Update every second
let tickInterval = null;
function startTicker() {
  if (tickInterval) clearInterval(tickInterval);
  tickInterval = setInterval(() => {
    const now = new Date();
    document.querySelectorAll('.clock').forEach((card, idx) => {
      const tz = zones[idx] === 'local' ? Intl.DateTimeFormat().resolvedOptions().timeZone : zones[idx];
      const timeEl = card.querySelector('.time');
      const dateEl = card.querySelector('.date');
      timeEl.textContent = fmtDateForZone(now, tz);
      dateEl.textContent = fmtLongForZone(now, tz);
    });
  }, 1000);
}

// Add new zone safely (validate via Intl)
function tryAddZone(tz) {
  if (!tz) return;
  const normalized = tz.trim();
  try {
    // Validate by attempting to format with the timeZone option
    new Intl.DateTimeFormat(undefined, { timeZone: normalized }).format(new Date());
    zones.push(normalized);
    save();
    render();
  } catch (e) {
    alert('Invalid IANA time zone: ' + normalized);
  }
}

addBtn.addEventListener('click', () => {
  tryAddZone(tzInput.value);
  tzInput.value = '';
});

presetSelect.addEventListener('change', (e) => {
  const v = e.target.value;
  if (!v) return;
  if (v === 'local') tryAddZone('local');
  else tryAddZone(v);
  e.target.selectedIndex = 0;
});

hourToggle.addEventListener('change', (e) => {
  use24 = e.target.checked;
  save();
  render();
});

document.addEventListener('keydown', (e) => {
  if ((e.key === 'Enter' || e.key === 'NumpadEnter') && document.activeElement === tzInput) {
    tryAddZone(tzInput.value);
    tzInput.value = '';
  }
});

// Initialize
render();
startTicker();
