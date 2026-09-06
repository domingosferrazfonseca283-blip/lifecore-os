#!/usr/bin/env python3

import json
import subprocess

def api(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5)
        if result.returncode != 0: return None
        return result.stdout.strip()
    except Exception: return None

def battery():
    data = api("termux-battery-status")
    if not data: return {"estado": "indisponível"}
    try: return json.loads(data)
    except json.JSONDecodeError: return {"estado": "erro", "dados": data}

def wifi():
    data = api("termux-wifi-connectioninfo")
    if not data: return {"estado": "indisponível"}
    try: return json.loads(data)
    except json.JSONDecodeError: return {"estado": "erro", "dados": data}

def vital_signs():
    return {"bateria": battery(), "wifi": wifi()}

if __name__ == "__main__": print(json.dumps(vital_signs(), indent=2, ensure_ascii=False))
