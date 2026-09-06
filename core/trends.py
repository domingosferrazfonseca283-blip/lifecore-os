#!/usr/bin/env python3

def compare(previous,current):
    trends=[]
    if not previous: return trends
    ob,nb=previous.get("bateria"),current.get("bateria")
    ot,nt=previous.get("temperatura"),current.get("temperatura")
    if isinstance(ob,(int,float)) and isinstance(nb,(int,float)):
        if nb<ob: trends.append("BATERIA_EM_QUEDA")
        elif nb>ob: trends.append("BATERIA_EM_ALTA")
    if isinstance(ot,(int,float)) and isinstance(nt,(int,float)):
        if nt>ot: trends.append("TEMPERATURA_EM_ASCENCAO")
        elif nt<ot: trends.append("TEMPERATURA_EM_QUEDA")
    return trends

def describe(trend):
    return {"BATERIA_EM_QUEDA":"A bateria está diminuindo.","BATERIA_EM_ALTA":"A bateria está aumentando.","TEMPERATURA_EM_ASCENCAO":"A temperatura está aumentando.","TEMPERATURA_EM_QUEDA":"A temperatura está diminuindo."}.get(trend,"Tendência desconhecida.")
