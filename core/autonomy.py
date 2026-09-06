#!/usr/bin/env python3
import os,sys,time
from datetime import datetime
LIFECORE_ROOT=os.path.expanduser("~/lifecore")
if LIFECORE_ROOT not in sys.path: sys.path.insert(0,LIFECORE_ROOT)
from core.health import analyze
from core.events import detect,describe as describe_event
from core.context import evaluate,describe
from actions.reflexes import decide
from memory.database import remember
INTERVAL=30

def get_state():
    h=analyze(); return {"estado":h.get("estado"),"bateria":h.get("bateria"),"temperatura":h.get("temperatura")}

def run():
    print(f"\n🤖 AUTONOMIA DO LIFECORE V0.9.1\n===============================\nObservação a cada {INTERVAL} segundos.\nCTRL+C para interromper.\n")
    previous=None; previous_context=[]
    try:
        while True:
            current=get_state(); now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{now}] estado={current['estado']} | energia={current['bateria']}% | temp={current['temperatura']}°C")
            for event in detect(previous,current):
                if event!="INICIO_MONITORAMENTO":
                    print(f"🧠 Evento: {describe_event(event)}"); remember("evento",f"{event}: {describe_event(event)}")
            context=evaluate(current); new_context=[x for x in context if x not in previous_context]
            for c in new_context:
                print(f"🔎 Contexto: {describe(c)}"); remember("contexto",f"{c}: {describe(c)}")
            if new_context:
                for action in decide():
                    relevant=(action["acao"]=="energia_baixa" and "ENERGIA_BAIXA" in new_context) or (action["acao"]=="energia_critica" and "ENERGIA_CRITICA" in new_context) or (action["acao"]=="temperatura_elevada" and "TEMPERATURA_ELEVADA" in new_context) or (action["acao"]=="temperatura_critica" and "TEMPERATURA_CRITICA" in new_context)
                    if relevant:
                        print(f"⚡ Reflexo contextual: {action['acao']} | prioridade={action['prioridade']}"); remember("reflexo",f"{action['acao']} | prioridade={action['prioridade']}")
            previous=current; previous_context=context; time.sleep(INTERVAL)
    except KeyboardInterrupt: print("\n🤖 Autonomia interrompida.\n=============================")
