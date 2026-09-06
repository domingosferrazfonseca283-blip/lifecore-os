#!/usr/bin/env python3

def detect(previous, current):
    events=[]
    if previous is None: return ["INICIO_MONITORAMENTO"]
    ob, nb = previous.get("bateria"), current.get("bateria")
    ot, nt = previous.get("temperatura"), current.get("temperatura")
    if isinstance(ob,(int,float)) and isinstance(nb,(int,float)):
        if nb>ob: events.append("BATERIA_SUBIU")
        elif nb<ob: events.append("BATERIA_DESCEU")
    if isinstance(ot,(int,float)) and isinstance(nt,(int,float)):
        if nt>ot: events.append("TEMPERATURA_SUBIU")
        elif nt<ot: events.append("TEMPERATURA_DESCEU")
    if previous.get("estado") != current.get("estado"): events.append("ESTADO_MUDOU")
    return events

def describe(event):
    return {"INICIO_MONITORAMENTO":"Monitoramento iniciado.","BATERIA_SUBIU":"Nível de bateria aumentou.","BATERIA_DESCEU":"Nível de bateria diminuiu.","TEMPERATURA_SUBIU":"Temperatura aumentou.","TEMPERATURA_DESCEU":"Temperatura diminuiu.","ESTADO_MUDOU":"Estado geral do sistema mudou."}.get(event,"Evento desconhecido.")
