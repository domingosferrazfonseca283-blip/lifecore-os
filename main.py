#!/usr/bin/env python3

import os
import platform
from datetime import datetime

from sensors.phone import vital_signs
from core.health import analyze
from memory.database import show_memory
from core.history import show_history
from actions.reflexes import decide
from core.autonomy import run as run_autonomy


ROOT = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE = os.path.join(ROOT, "VERSION")


def load_version():
    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    except OSError:
        return "1.3.0"


VERSION = load_version()


def show_status():
    health = analyze()

    print()
    print("🧠 ESTADO DO LIFECORE")
    print("=====================")
    print(f"Estado: {health['estado']}")
    print(f"Energia: {health['bateria']}%")
    print(f"Temperatura: {health['temperatura']} °C")
    print()
    print("Alertas:")

    if health["alertas"]:
        for alert in health["alertas"]:
            print(f"• {alert}")
    else:
        print("• nenhum")

    print("=====================")


def show_vitals():
    data = vital_signs()
    battery = data.get("bateria", {})
    wifi = data.get("wifi", {})

    print()
    print("🫀 SINAIS VITAIS")
    print("================")
    print(f"Bateria: {battery.get('percentage')}%")
    print(f"Temperatura: {battery.get('temperature')} °C")
    print(f"Carregador: {battery.get('plugged')}")
    print(f"Wi-Fi: {wifi.get('ssid')}")
    print("================")


def show_diagnosis():
    show_status()


def show_reflexes():
    print()
    print("⚡ REFLEXOS DO LIFECORE")
    print("=======================")

    for action in decide():
        print(f"Prioridade: {action['prioridade']}")
        print(f"Ação: {action['acao']}")
        print(f"→ {action['mensagem']}")
        print(
            "🔐 Segurança: PERMITIDA"
            if action["permitida"]
            else "🔴 Segurança: BLOQUEADA"
        )

        if action["confirmacao"]:
            print("⚠️ Requer confirmação.")

        print()

    print("=======================")


def show_help():
    print()
    print("🧠 COMANDOS DO LIFECORE")
    print("=======================")
    print("estado       → estado geral")
    print("vital        → sinais vitais")
    print("diagnostico  → diagnóstico")
    print("reflexo      → decisões")
    print("reflexos     → decisões")
    print("auto         → autonomia controlada")
    print("autonomia    → autonomia controlada")
    print("memoria      → memória")
    print("historico    → histórico temporal")
    print("histórico    → histórico temporal")
    print("hora         → hora atual")
    print("sistema      → informações do sistema")
    print("ajuda        → ajuda")
    print("limpar       → limpa terminal")
    print("sair         → encerra")
    print("=======================")


def show_system():
    print()
    print("⚙️ SISTEMA DO LIFECORE")
    print("======================")
    print(f"Versão: V{VERSION}")
    print(f"Sistema: {platform.system()}")
    print(f"Kernel: {platform.release()}")
    print(f"Arquitetura: {platform.machine()}")
    print("======================")


def main():
    print()
    print("🧠 =============================")
    print(f"   LIFECORE V{VERSION}")
    print("   Sistema iniciado")
    print("===============================")
    print()
    print("Cérebro: ONLINE")
    print("Memória: ONLINE")
    print("Núcleo: ONLINE")
    print("Sensores: ONLINE")
    print("Diagnóstico: ONLINE")
    print("Memória persistente: ONLINE")
    print("Reflexos: ONLINE")
    print("Autonomia: ONLINE")
    print("Histórico temporal: ONLINE")
    print()
    print("Escreve 'ajuda' para ver os comandos.")
    print()

    while True:
        try:
            command = input("LIFE > ").strip().lower()

            if command == "estado":
                show_status()
            elif command == "vital":
                show_vitals()
            elif command == "diagnostico":
                show_diagnosis()
            elif command in ("reflexo", "reflexos"):
                show_reflexes()
            elif command in ("auto", "autonomia"):
                run_autonomy()
            elif command == "memoria":
                show_memory()
            elif command in ("historico", "histórico"):
                show_history()
            elif command == "hora":
                print("🕒", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            elif command == "sistema":
                show_system()
            elif command == "ajuda":
                show_help()
            elif command == "limpar":
                os.system("clear")
            elif command == "sair":
                print("👋 LIFECORE desligando...")
                break
            elif command:
                print("❓ Comando desconhecido. Escreve 'ajuda'.")

        except (KeyboardInterrupt, EOFError):
            print("\n👋 LIFECORE desligando...")
            break


if __name__ == "__main__":
    main()
