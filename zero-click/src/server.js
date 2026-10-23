import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { randomUUID } from 'node:crypto';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { WebSocket, WebSocketServer } from 'ws';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const HOST = '127.0.0.1';
const PORT = Number(process.env.PORT ?? 3000);
const PUBLIC_DIR = join(ROOT, 'public');
const ALLOWED_HOSTS = new Set([`${HOST}:${PORT}`, `localhost:${PORT}`]);

// Serve only these files; requests cannot address arbitrary paths on disk.
const PUBLIC_FILES = new Map([
  ['/', ['index.html', 'text/html; charset=utf-8']],
  ['/app.js', ['app.js', 'text/javascript; charset=utf-8']],
  ['/styles.css', ['styles.css', 'text/css; charset=utf-8']],
]);

const FIXTURES = {
  ordinary: {
    filename: 'ordinary-image.fixture',
    label: 'Ordinary training image',
  },
  trigger: {
    filename: 'simulated-trigger.fixture',
    label: 'Simulated parser trigger',
  },
};

const httpServer = createServer(async (request, response) => {
  if (!ALLOWED_HOSTS.has(request.headers.host)) {
    response.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
    response.end('Use the local demo address shown in the terminal.');
    return;
  }

  const pathname = new URL(request.url ?? '/', `http://${HOST}`).pathname;
  const asset = PUBLIC_FILES.get(pathname);

  if (request.method !== 'GET' || !asset) {
    response.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    response.end('Not found');
    return;
  }

  try {
    const body = await readFile(join(PUBLIC_DIR, asset[0]));
    response.writeHead(200, {
      'Content-Type': asset[1],
      'X-Content-Type-Options': 'nosniff',
      'Referrer-Policy': 'no-referrer',
      'Cache-Control': 'no-store',
    });
    response.end(body);
  } catch {
    response.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
    response.end('Could not load the demo page');
  }
});

const webSockets = new WebSocketServer({
  server: httpServer,
  path: '/ws',
  maxPayload: 1024,
});

webSockets.on('connection', (socket, request) => {
  const requestOrigin = request.headers.origin;
  if (requestOrigin !== `http://${request.headers.host}`) {
    socket.close(1008, 'This demo accepts same-origin connections only');
    return;
  }

  const role = new URL(request.url, `http://${HOST}`).searchParams.get('role');
  if (role !== 'sender' && role !== 'receiver') {
    socket.close(1008, 'Choose sender or receiver role');
    return;
  }

  socket.role = role;
  send(socket, { type: 'connected', role });

  socket.on('message', async (rawMessage) => {
    if (socket.role !== 'sender') {
      send(socket, { type: 'error', message: 'Only the sender can send fixtures.' });
      return;
    }

    let requestMessage;
    try {
      requestMessage = JSON.parse(rawMessage.toString());
    } catch {
      send(socket, { type: 'error', message: 'The message was not valid JSON.' });
      return;
    }

    const fixture = FIXTURES[requestMessage.fixture];
    if (requestMessage.type !== 'send-fixture' || !fixture) {
      send(socket, { type: 'error', message: 'Unknown demo fixture.' });
      return;
    }

    try {
      const content = await readFile(
        join(ROOT, 'fixtures', fixture.filename),
        'utf8',
      );
      const event = {
        type: 'fixture-received',
        id: randomUUID(),
        filename: fixture.filename,
        label: fixture.label,
        content,
        sentAt: new Date().toISOString(),
      };

      for (const client of webSockets.clients) {
        if (client.role === 'receiver' && client.readyState === WebSocket.OPEN) {
          send(client, event);
        }
      }

      send(socket, { type: 'sent', label: fixture.label });
    } catch {
      send(socket, { type: 'error', message: 'Could not load the demo fixture.' });
    }
  });
});

function send(socket, message) {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(message));
  }
}

httpServer.listen(PORT, HOST, () => {
  console.log(`Zero-click training demo: http://${HOST}:${PORT}`);
  console.log('Open a receiver tab, then open /?role=sender in another tab.');
  console.log('Local-only simulation; it does not run a real exploit.');
});
