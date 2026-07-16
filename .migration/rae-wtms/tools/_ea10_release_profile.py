#!/usr/bin/env python3
"""Release m365 profile lock — only migration Playwright Chromium."""
import os
import subprocess
import sys
import time

PROFILE = r'G:\ProjectAI\document-center\.browser-profile\m365'
MARKERS = ('m365', 'playwright', 'ea10', 'ea7a', 'ea8', 'ea9')


def list_processes():
    ps = subprocess.run(
        ['powershell', '-NoProfile', '-Command',
         'Get-CimInstance Win32_Process | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress'],
        capture_output=True, text=True, cwd=r'G:\ProjectAI\document-center',
    )
    if ps.returncode != 0:
        return []
    import json
    raw = ps.stdout.strip()
    if not raw:
        return []
    data = json.loads(raw)
    if isinstance(data, dict):
        data = [data]
    return data


def main():
    killed = []
    for p in list_processes():
        cmd = (p.get('CommandLine') or '')
        name = (p.get('Name') or '').lower()
        if PROFILE.replace('\\', '/') not in cmd.replace('\\', '/'):
            continue
        if not any(m in cmd.lower() for m in MARKERS):
            continue
        pid = p.get('ProcessId')
        if not pid:
            continue
        subprocess.run(['taskkill', '/PID', str(pid), '/F'], capture_output=True)
        killed.append(pid)
    lock = os.path.join(PROFILE, 'SingletonLock')
    if killed:
        time.sleep(2)
    if os.path.lexists(lock) and not killed:
        print('Lock file present but no matching process found; not removing', file=sys.stderr)
    elif os.path.lexists(lock):
        try:
            os.remove(lock)
        except OSError:
            pass
    print({'killed': killed, 'lock_removed': os.path.lexists(lock) is False})


if __name__ == '__main__':
    main()
