const role = new URLSearchParams(window.location.search).get('role') === 'sender'
  ? 'sender'
  : 'receiver';

const status = document.querySelector('#connection-status');
const senderPanel = document.querySelector('#sender-panel');
const receiverPanel = document.querySelector('#receiver-panel');
const senderLink = document.querySelector('#sender-link');
const receiverLink = document.querySelector('#receiver-link');
const senderFeedback = document.querySelector('#sender-feedback');
const sendOrdinaryButton = document.querySelector('#send-ordinary');
const sendTriggerButton = document.querySelector('#send-trigger');
const emptyState = document.querySelector('#empty-state');
const messageCard = document.querySelector('#message-card');
const messageName = document.querySelector('#message-name');
const messageTime = document.querySelector('#message-time');
const previewBox = document.querySelector('#preview-box');
const previewStatus = document.querySelector('#preview-status');
const patchedMode = document.querySelector('#patched-mode');
const activityLog = document.querySelector('#activity-log');

senderPanel.hidden = role !== 'sender';
receiverPanel.hidden = role !== 'receiver';
senderLink.classList.toggle('active', role === 'sender');
receiverLink.classList.toggle('active', role === 'receiver');

const socketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const socket = new WebSocket(
  `${socketProtocol}//${window.location.host}/ws?role=${role}`,
);

socket.addEventListener('open', () => {
  status.textContent = 'Connected';
  status.dataset.state = 'connected';
  if (role === 'sender') {
    senderFeedback.textContent = 'Connected. Choose a fixture to send.';
  }
  addLog('WebSocket connected as ' + role + '.', 'system');
});

socket.addEventListener('close', () => {
  status.textContent = 'Disconnected';
  status.dataset.state = 'disconnected';
  if (role === 'sender') {
    senderFeedback.textContent = 'Connection lost. Refresh this tab to reconnect.';
  }
});

socket.addEventListener('error', () => {
  status.textContent = 'Connection error';
  status.dataset.state = 'disconnected';
});

socket.addEventListener('message', (event) => {
  let message;
  try {
    message = JSON.parse(event.data);
  } catch {
    addLog('Ignored a message that was not valid JSON.', 'warning');
    return;
  }

  if (message.type === 'fixture-received' && role === 'receiver') {
    receiveFixture(message);
  } else if (message.type === 'sent' && role === 'sender') {
    senderFeedback.textContent = `${message.label} sent to receiver tabs.`;
  } else if (message.type === 'error') {
    addLog(message.message, 'warning');
    if (role === 'sender') senderFeedback.textContent = message.message;
  }
});

sendOrdinaryButton?.addEventListener('click', () => sendFixture('ordinary'));
sendTriggerButton?.addEventListener('click', () => sendFixture('trigger'));

function sendFixture(fixture) {
  if (socket.readyState !== WebSocket.OPEN) {
    senderFeedback.textContent = 'Connect before sending a fixture.';
    return;
  }
  socket.send(JSON.stringify({ type: 'send-fixture', fixture }));
  senderFeedback.textContent = 'Sending fixture…';
}

function receiveFixture(message) {
  emptyState.hidden = true;
  messageCard.hidden = false;
  messageName.textContent = message.filename;
  messageTime.textContent = new Date(message.sentAt).toLocaleTimeString();
  previewBox.dataset.state = 'processing';
  previewStatus.textContent = 'Generating preview automatically…';

  addLog(`Received ${message.filename} over WebSocket.`, 'system');
  addLog('Preview processing started automatically; no click was needed.', 'system');

  // The fixture is plain text. This marker only selects a harmless UI outcome.
  const hasDemoMarker = message.content.includes('SIMULATE_PARSER_WARNING');

  window.setTimeout(() => {
    if (hasDemoMarker && patchedMode.checked) {
      previewBox.dataset.state = 'blocked';
      previewStatus.textContent = 'Fixture rejected by the preview guard.';
      addLog('Patched mode rejected the known training marker.', 'safe');
      return;
    }

    if (hasDemoMarker) {
      previewBox.dataset.state = 'warning';
      previewStatus.textContent = 'Simulated alert shown — no exploit ran.';
      addLog('Displayed the harmless training alert; no exploit ran.', 'warning');
      window.alert("This is where the vulnerability lives... \nYou've been hacked!");
      return;
    }

    previewBox.dataset.state = 'ready';
    previewStatus.textContent = 'Ordinary fixture previewed safely.';
    addLog('Ordinary fixture processed by the mock previewer.', 'safe');
  }, 450);
}

function addLog(text, kind = 'system') {
  const empty = activityLog.querySelector('.log-empty');
  empty?.remove();

  const item = document.createElement('li');
  item.className = `log-item log-${kind}`;
  const time = document.createElement('time');
  time.dateTime = new Date().toISOString();
  time.textContent = new Date().toLocaleTimeString();
  const message = document.createElement('span');
  message.textContent = text;
  item.append(time, message);
  activityLog.prepend(item);

  while (activityLog.children.length > 12) {
    activityLog.lastElementChild.remove();
  }
}
