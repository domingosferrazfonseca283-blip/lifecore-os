#!/usr/bin/env python3

import os
import sys

LIFECORE_ROOT = os.path.expanduser("~/lifecore")
if LIFECORE_ROOT not in sys.path:
    sys.path.insert(0, LIFECORE_ROOT)

from sensors.phone import vital_signs

def analyze():
    data = vital_signs()
    battery = data.get("bateria", {})
    wifi = data.get("wifi", {})
    alerts = []
    state = "NORMAL"
    percentage = battery.get("percentage")
    if isinstance(percentage, (int, float)):
        if percentage <= 5:
            alerts.append("ENERGIA CRÍTICA")
            state = "CRÍTICO"
        elif percentage <= 15:
            alerts.append("ENERGIA BAIXA")
            state = "ATENÇÃO"
    temperature = battery.get("temperature")
    if isinstance(temperature, (int, float)):
        if temperature >= 45:
            alerts.append("TEMPERATURA MUITO ALTA")
            state = "CRÍTICO"
        elif temperature >= 40:
            alerts.append("TEMPERATURA ELEVADA")
            if state == "NORMAL": state = "ATENÇÃO"
    ip = wifi.get("ip")
    if ip == "0.0.0.0" or ip is None:
        alerts.append("SEM CONECTIVIDADE WI-FI")
    return {"estado": state, "alertas": alerts, "bateria": percentage, "temperatura": temperature, "wifi": wifi.get("ssid")}

def show_health():
    health = analyze()
    print("\n🧠 ANÁLISE DO LIFECORE\n----------------------")
    print(f"estado geral: {health['estado']}")
    if health["bateria"] is not None: print(f"energia: {health['bateria']}%")
    if health["temperatura"] is not None: print(f"temperatura: {health['temperatura']} °C")
    print("\n⚠️ ALERTAS")
    if health["alertas"]:
        for alert in health["alertas"]: print(f"• {alert}")
    else: print("• nenhum")
    print("----------------------")

if __name__ == "__main__": show_health()
