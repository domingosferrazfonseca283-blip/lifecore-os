#!/usr/bin/env python3
import platform,os
from datetime import datetime
from sensors.phone import vital_signs
from core.health import analyze
from memory.database import show_memory
from actions.reflexes import decide
from core.autonomy import run as run_autonomy
VERSION="1.2.0"
def show_status():
    h=analyze(); print(f"\n🧠 ESTADO DO LIFECORE\n=====================\nEstado: {h['estado']}\nEnergia: {h['bateria']}%\nTemperatura: {h['temperatura']} °C\n\nAlertas:"); [print(f"• {a}") for a in h['alertas']] if h['alertas'] else print("• nenhum"); print("=====================")
def show_vitals():
    d=vital_signs(); b=d.get('bateria',{}); w=d.get('wifi',{}); print(f"\n🫀 SINAIS VITAIS\n================\nBateria: {b.get('percentage')}%\nTemperatura: {b.get('temperature')} °C\nCarregador: {b.get('plugged')}\nWi-Fi: {w.get('ssid')}\n================")
def show_diagnosis(): show_status()
def show_reflexes():
    print("\n⚡ REFLEXOS DO LIFECORE\n=======================")
    for a in decide(): print(f"Prioridade: {a['prioridade']}\nAção: {a['acao']}\n→ {a['mensagem']}\n"+("🔐 Segurança: PERMITIDA" if a['permitida'] else "🔴 Segurança: BLOQUEADA")+(("\n⚠️ Requer confirmação." if a['confirmacao'] else ""))+"\n")
    print("=======================")
def show_help(): print("\n🧠 COMANDOS DO LIFECORE\n=======================\nestado → estado geral\nvital → sinais vitais\ndiagnostico → diagnóstico\nreflexo → decisões\nauto → autonomia controlada\nmemoria → memória\nhora → hora atual\nsistema → informações do sistema\najuda → ajuda\nlimpar → limpa terminal\nsair → encerra\n=======================")
def show_system(): print(f"\n⚙️ SISTEMA DO LIFECORE\n======================\nVersão: V{VERSION}\nSistema: {platform.system()}\nKernel: {platform.release()}\nArquitetura: {platform.machine()}\n======================")
def main():
    print(f"\n🧠 =============================\n   LIFECORE V{VERSION}\n   Sistema iniciado\n===============================\n\nCérebro: ONLINE\nMemória: ONLINE\nNúcleo: ONLINE\nSensores: ONLINE\nDiagnóstico: ONLINE\nMemória persistente: ONLINE\nReflexos: ONLINE\nAutonomia: ONLINE\n\nEscreve 'ajuda' para ver os comandos.\n")
    while True:
        try:
            c=input("LIFE > ").strip().lower()
            if c=="estado": show_status()
            elif c=="vital": show_vitals()
            elif c=="diagnostico": show_diagnosis()
            elif c in ("reflexo","reflexos"): show_reflexes()
            elif c in ("auto","autonomia"): run_autonomy()
            elif c=="memoria": show_memory()
            elif c=="hora": print("🕒",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            elif c=="sistema": show_system()
            elif c=="ajuda": show_help()
            elif c=="limpar": os.system("clear")
            elif c=="sair": print("👋 LIFECORE desligando..."); break
            elif c: print("❓ Comando desconhecido. Escreve 'ajuda'.")
        except (KeyboardInterrupt,EOFError): print("\n👋 LIFECORE desligando..."); break
if __name__=="__main__": main()
