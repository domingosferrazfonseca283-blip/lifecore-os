#!/usr/bin/env python3
import os,sys
LIFECORE_ROOT=os.path.expanduser("~/lifecore")
if LIFECORE_ROOT not in sys.path: sys.path.insert(0,LIFECORE_ROOT)
from core.health import analyze
from security.permissions import check

def decide():
    health=analyze(); battery=health.get("bateria"); temperature=health.get("temperatura"); state=health.get("estado"); actions=[]
    if isinstance(battery,(int,float)):
        if battery<=5: actions.append({"acao":"energia_critica","prioridade":"ALTA","mensagem":"Ligar o carregador imediatamente."})
        elif battery<=15: actions.append({"acao":"energia_baixa","prioridade":"MEDIA","mensagem":"Recomenda-se carregar o telefone."})
    if isinstance(temperature,(int,float)):
        if temperature>=45: actions.append({"acao":"temperatura_critica","prioridade":"ALTA","mensagem":"Reduzir utilização e permitir arrefecimento."})
        elif temperature>=40: actions.append({"acao":"temperatura_elevada","prioridade":"MEDIA","mensagem":"Evitar carga de trabalho elevada."})
    if state=="NORMAL" and not actions: actions.append({"acao":"nenhuma","prioridade":"NORMAL","mensagem":"Nenhuma intervenção necessária."})
    for action in actions:
        security=check(action["acao"]); action["permitida"]=security["permitida"]; action["confirmacao"]=security["confirmacao"]
    return actions

def show_reflexes():
    print("\n⚡ REFLEXOS DO LIFECORE\n=======================")
    for action in decide():
        print(f"Prioridade: {action['prioridade']}\nAção: {action['acao']}\n→ {action['mensagem']}")
        print("🔐 Segurança: PERMITIDA" if action["permitida"] else "🔴 Segurança: BLOQUEADA")
        if action["confirmacao"]: print("⚠️ Requer confirmação.")
        print()
    print("=======================")
