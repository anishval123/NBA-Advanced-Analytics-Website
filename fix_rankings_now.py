"""Restart backend and verify ranking endpoints return data."""
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(ROOT, "rankings_test_out.txt")


def log(msg: str) -> None:
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)


def kill_port_8000() -> None:
    try:
        out = subprocess.check_output(
            'netstat -ano | findstr :8000 | findstr LISTENING',
            shell=True,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        pids = set()
        for line in out.splitlines():
            parts = line.split()
            if parts:
                pids.add(parts[-1])
        for pid in pids:
            subprocess.run(f"taskkill /F /PID {pid}", shell=True, capture_output=True)
            log(f"Killed PID {pid}")
    except subprocess.CalledProcessError:
        log("No process listening on 8000")


def fetch(path: str, timeout: int = 60):
    req = urllib.request.Request(f"http://127.0.0.1:8000{path}")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        return resp.status, body


def main() -> None:
    if os.path.exists(LOG):
        os.remove(LOG)

    log("=== Killing old backend ===")
    kill_port_8000()
    time.sleep(2)

    log("=== Starting backend ===")
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=os.path.join(ROOT, "backend"),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    # Wait for server to come up (BR scrape can take a bit)
    ready = False
    for i in range(40):
        time.sleep(2)
        try:
            status, body = fetch("/", timeout=5)
            if status == 200:
                log(f"Server ready after ~{(i + 1) * 2}s: {body[:120]}")
                ready = True
                break
        except Exception as exc:
            log(f"  wait {i + 1}: {exc}")

    if not ready:
        log("SERVER FAILED TO START")
        try:
            out = proc.stdout.read() if proc.stdout else ""
            log(f"stdout:\n{out[:3000]}")
        except Exception:
            pass
        proc.terminate()
        return

    endpoints = [
        "/underrated",
        "/overrated",
        "/volatility",
        "/role_compression",
        "/defensive_chaos",
    ]

    for ep in endpoints:
        try:
            status, body = fetch(ep, timeout=90)
            data = json.loads(body)
            count = len(data) if isinstance(data, list) else "n/a"
            first = ""
            if isinstance(data, list) and data:
                first = f"{data[0].get('player')} score={data[0].get('score')}"
            log(f"{ep}: status={status} count={count} first={first}")
        except Exception as exc:
            log(f"{ep}: ERROR {exc}")

    log("=== DONE ===")
    # Leave server running for the frontend
    log(f"Backend PID {proc.pid} left running on port 8000")


if __name__ == "__main__":
    main()
