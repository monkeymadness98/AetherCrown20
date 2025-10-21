#!/usr/bin/env python3
"""
Cron-safe wrapper for backend/empire_automation.py.

Usage:
  python backend/empire_automation_lock.py

Behavior:
- Attempts a Redis lock if REDIS_URL is set (preferred).
- Falls back to a pidfile lock at /tmp/empire_automation.lock.
- Invokes backend.empire_automation.main() if available; otherwise runs module.
"""
import os
import sys
from pathlib import Path

LOCK_FILE = Path("/tmp/empire_automation.lock")
REDIS_URL = os.environ.get("REDIS_URL")
LOCK_KEY = "aether_empire_automation_lock"
LOCK_TTL = int(os.environ.get("EMPIRE_LOCK_TTL", 60 * 60))  # seconds

def file_acquire():
    if LOCK_FILE.exists():
        print("Lock exists, exiting to prevent overlap.")
        sys.exit(0)
    LOCK_FILE.write_text(str(os.getpid()))

def file_release():
    try:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()
    except Exception:
        pass

def run_script():
    try:
        import importlib, runpy
        mod = importlib.import_module("backend.empire_automation")
        if hasattr(mod, "main"):
            mod.main()
        else:
            runpy.run_module("backend.empire_automation", run_name="__main__")
    except Exception:
        import traceback
        traceback.print_exc()
        raise

def main():
    if REDIS_URL:
        try:
            import redis
            client = redis.from_url(REDIS_URL)
            got = client.setnx(LOCK_KEY, "1")
            if not got:
                print("Another run holds the Redis lock; exiting.")
                return
            client.expire(LOCK_KEY, LOCK_TTL)
            try:
                run_script()
            finally:
                client.delete(LOCK_KEY)
            return
        except Exception as e:
            print("Redis lock attempt failed, falling back to file lock:", e)

    # Fallback: pidfile lock
    try:
        file_acquire()
        run_script()
    finally:
        file_release()

if __name__ == "__main__":
    main()
