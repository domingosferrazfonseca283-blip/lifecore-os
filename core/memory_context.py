#!/usr/bin/env python3

import os,sys
LIFECORE_ROOT=os.path.expanduser("~/lifecore")
if LIFECORE_ROOT not in sys.path: sys.path.insert(0,LIFECORE_ROOT)
from memory.database import recall

def recent_events(limit=20):
    events=[]
    for timestamp,tipo,conteudo in recall(limit):
        if tipo in ("evento","contexto","reflexo"):
            events.append({"timestamp":timestamp,"tipo":tipo,"conteudo":conteudo})
    return events

def summarize(limit=20):
    events=recent_events(limit); summary={"total":len(events),"eventos":0,"contextos":0,"reflexos":0}
    for event in events: summary["eventos" if event["tipo"]=="evento" else "contextos" if event["tipo"]=="contexto" else "reflexos"]+=1
    return summary

def show_memory_context(limit=20):
    events=recent_events(limit); summary=summarize(limit)
    print("\n🧠 MEMÓRIA CONTEXTUAL\n=====================")
    print(f"Registros analisados: {summary['total']}"); print(f"Eventos: {summary['eventos']}"); print(f"Contextos: {summary['contextos']}"); print(f"Reflexos: {summary['reflexos']}\n\nHistórico recente:")
    if not events: print("• Nenhum evento contextual.")
    else:
        for event in events: print(f"[{event['timestamp']}] {event['tipo']}: {event['conteudo']}")
    print("=====================")
