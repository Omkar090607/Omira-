"""
status_bridge.py — local-only status feed from Omira to the OMIRA orb UI.

This is intentionally tiny and one-directional:
  - Omira calls set_status(state, detail) whenever its state changes
    (idle / listening / processing / responding / error).
  - Any connected browser (the OMIRA orb) receives that update over a
    WebSocket and reacts visually.
  - The browser CANNOT send commands back through this connection — any
    message it sends is ignored. This is a read-only status broadcast,
    not a control channel.
  - The server binds to 127.0.0.1 by default, so it is not reachable from
    your network, only from your own machine.

If the `websockets` package isn't installed, Omira still runs completely
normally — this module just silently disables the OMIRA status feed.
"""

import asyncio
import json
import os
import threading
import time

try:
    import websockets
except ImportError:
    websockets = None

HOST = os.getenv("OMIRA_STATUS_WS_HOST", "127.0.0.1")
PORT = int(os.getenv("OMIRA_STATUS_WS_PORT", "8765"))

_state_lock = threading.Lock()
_current_status = {"state": "idle", "detail": "", "ts": time.time()}
_clients = set()
_loop = None  # set once the server's asyncio event loop is running


def _snapshot():
    with _state_lock:
        return dict(_current_status)


async def _broadcast(status):
    if not _clients:
        return
    message = json.dumps(status)
    dead = []
    for ws in list(_clients):
        try:
            await ws.send(message)
        except Exception:
            dead.append(ws)
    for ws in dead:
        _clients.discard(ws)


def set_status(state, detail=""):
    """Thread-safe. Call from anywhere in new_omira.py to update what the
    OMIRA orb displays. Safe no-op if the bridge server isn't running."""
    status = {"state": state, "detail": str(detail)[:200], "ts": time.time()}
    with _state_lock:
        _current_status.clear()
        _current_status.update(status)

    if _loop is not None and websockets is not None:
        try:
            asyncio.run_coroutine_threadsafe(_broadcast(status), _loop)
        except Exception:
            pass


async def _handler(websocket):
    _clients.add(websocket)
    try:
        # Send current state immediately so a freshly opened browser tab
        # doesn't wait for the next state change to show anything.
        await websocket.send(json.dumps(_snapshot()))
        async for _ in websocket:
            pass  # read-only feed — anything the client sends is ignored
    except Exception:
        pass
    finally:
        _clients.discard(websocket)


async def _serve():
    global _loop
    _loop = asyncio.get_running_loop()
    async with websockets.serve(_handler, HOST, PORT):
        await asyncio.Future()  # run forever


def start():
    """Start the status server in a background daemon thread. Call once at
    startup. Safe no-op (with a console note) if `websockets` isn't
    installed."""
    if websockets is None:
        print(
            "[status_bridge] `websockets` not installed — OMIRA status feed "
            "disabled. Run: pip install websockets"
        )
        return

    def _run():
        try:
            asyncio.run(_serve())
        except Exception as exc:
            print(f"[status_bridge] server stopped: {exc}")

    threading.Thread(target=_run, daemon=True).start()
    print(f"[status_bridge] OMIRA status feed on ws://{HOST}:{PORT} (localhost only)")
