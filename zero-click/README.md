# Zero-click training demo

A local-only Node.js demo of the *zero-click idea*: an incoming attachment is
processed automatically to create a preview, without the recipient opening it.

The two fixtures are plain text, not images. One contains a marker that makes
the receiver show a browser alert saying `You've been hacked!`. The app does not
contain a real vulnerable parser, exploit payload, command execution, or access
to local files.

## Run locally

```sh
npm install
npm start
```

Open <http://127.0.0.1:3000/> in one tab as the receiver. Open
<http://127.0.0.1:3000/?role=sender> in a second tab and send either fixture.
The Node.js server relays the message over WebSocket to receiver tabs. The
receiver automatically starts the simulated preview and records the steps.

Turn on **Patched preview mode** in the receiver tab and resend the simulated
trigger to compare the harmless guard behavior. The app binds to `127.0.0.1`
and is intended for a local classroom walkthrough.
