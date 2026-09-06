#!/usr/bin/env python3
import json,os
STATE_DIR=os.path.expanduser("~/lifecore/memory")
STATE_FILE=os.path.join(STATE_DIR,"state.json")
def save(state,contexto=None):
    os.makedirs(STATE_DIR,exist_ok=True)
    with open(STATE_FILE,"w",encoding="utf-8") as f: json.dump({"estado":state,"contexto":contexto or []},f,ensure_ascii=False,indent=2)
def load():
    if not os.path.exists(STATE_FILE): return None
    try:
        with open(STATE_FILE,encoding="utf-8") as f: data=json.load(f)
        if "estado" in data and isinstance(data["estado"],dict): return data
        return {"estado":data,"contexto":[]}
    except (OSError,json.JSONDecodeError): return None
def exists(): return os.path.exists(STATE_FILE)
