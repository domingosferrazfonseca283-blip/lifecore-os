#!/usr/bin/env python3

def evaluate(state):
    battery, temperature, status = state.get("bateria"), state.get("temperatura"), state.get("estado")
    conclusions=[]
    if isinstance(battery,(int,float)):
        if battery<=5: conclusions.append("ENERGIA_CRITICA")
        elif battery<=15: conclusions.append("ENERGIA_BAIXA")
    if isinstance(temperature,(int,float)):
        if temperature>=45: conclusions.append("TEMPERATURA_CRITICA")
        elif temperature>=40: conclusions.append("TEMPERATURA_ELEVADA")
    if status=="NORMAL" and not conclusions: conclusions.append("ESTADO_ESTAVEL")
    return conclusions

def describe(conclusion):
    return {"ENERGIA_CRITICA":"Energia em nível crítico.","ENERGIA_BAIXA":"Energia em nível baixo.","TEMPERATURA_CRITICA":"Temperatura em nível crítico.","TEMPERATURA_ELEVADA":"Temperatura acima do nível normal.","ESTADO_ESTAVEL":"Sistema estável."}.get(conclusion,"Condição desconhecida.")
