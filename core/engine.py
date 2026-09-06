#!/usr/bin/env python3
import os,sys
from datetime import datetime
LIFECORE_ROOT=os.path.expanduser("~/lifecore")
if LIFECORE_ROOT not in sys.path: sys.path.insert(0,LIFECORE_ROOT)
from core.health import analyze
from core.context import evaluate,describe
from core.events import detect,describe as describe_event
from core.trends import compare,describe as describe_trend
from core.memory_context import recent_events,summarize
from core.state import load,save
from actions.reflexes import decide
from memory.database import remember

class LifeEngine:
    def __init__(self):
        saved=load(); self.previous_state=saved.get("estado") if saved else None; self.previous_context=saved.get("contexto",[]) if saved else []
    def perceive(self):
        health=analyze(); return {"estado":health.get("estado"),"bateria":health.get("bateria"),"temperatura":health.get("temperatura"),"alertas":health.get("alertas",[])}
    def recall(self): return {"recent":recent_events(20),"summary":summarize(20)}
    def process(self):
        current=self.perceive(); memory=self.recall(); events=detect(self.previous_state,current); trends=compare(self.previous_state,current); context=evaluate(current)
        new_context=[x for x in context if x not in self.previous_context]; actions=[]
        if new_context:
            for action in decide():
                relevant=(action["acao"]=="energia_baixa" and "ENERGIA_BAIXA" in new_context) or (action["acao"]=="energia_critica" and "ENERGIA_CRITICA" in new_context) or (action["acao"]=="temperatura_elevada" and "TEMPERATURA_ELEVADA" in new_context) or (action["acao"]=="temperatura_critica" and "TEMPERATURA_CRITICA" in new_context)
                if relevant: actions.append(action)
        save(current,context)
        for trend in trends: remember("tendencia",f"{trend}: {describe_trend(trend)}")
        self.previous_state=current; self.previous_context=context
        return {"estado":current,"memoria":memory,"eventos":events,"tendencias":trends,"contexto":new_context,"acoes":actions}

def show_result(result):
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"); state=result["estado"]; summary=result["memoria"]["summary"]
    print(f"\n[{now}] 🧠 LIFE ENGINE V1.2\n==============================\n\nPERCEPÇÃO\n------------------------------")
    print(f"Estado: {state['estado']}\nBateria: {state['bateria']}%\nTemperatura: {state['temperatura']}°C\n\nMEMÓRIA\n------------------------------")
    print(f"Registros analisados: {summary['total']}\nEventos: {summary['eventos']} | Contextos: {summary['contextos']} | Reflexos: {summary['reflexos']}\n\nEVENTOS\n------------------------------")
    if result["eventos"]:
        for e in result["eventos"]: print(f"🧠 {describe_event(e)}")
    else: print("• nenhum evento novo")
    print("\nTENDÊNCIAS\n------------------------------")
    if result["tendencias"]:
        for t in result["tendencias"]: print(f"📈 {describe_trend(t)}")
    else: print("• nenhuma tendência detectada")
    print("\nCONTEXTO\n------------------------------")
    if result["contexto"]:
        for c in result["contexto"]: print(f"🔎 {describe(c)}")
    else: print("• nenhuma condição nova")
    print("\nDECISÃO\n------------------------------")
    if result["acoes"]:
        for a in result["acoes"]: print(f"⚡ {a['acao']} | prioridade={a['prioridade']}")
    else: print("• nenhuma ação necessária")
    print("\n💾 Estado + contexto salvos.\n==============================")

if __name__=="__main__": show_result(LifeEngine().process())
