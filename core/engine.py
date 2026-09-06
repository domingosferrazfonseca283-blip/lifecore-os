#!/usr/bin/env python3

import os
import sys
from datetime import datetime

LIFECORE_ROOT = os.path.expanduser("~/lifecore")

if LIFECORE_ROOT not in sys.path:
    sys.path.insert(0, LIFECORE_ROOT)

from core.health import analyze
from core.context import evaluate, describe
from core.events import detect, describe as describe_event
from core.trends import compare, describe as describe_trend
from core.memory_context import recent_events, summarize
from core.state import load, save
from core.history import record
from actions.reflexes import decide
from memory.database import remember


class LifeEngine:

    def __init__(self):
        saved = load()

        if saved:
            self.previous_state = saved.get("estado")
            self.previous_context = saved.get("contexto", [])
        else:
            self.previous_state = None
            self.previous_context = []

    def perceive(self):
        health = analyze()

        return {
            "estado": health.get("estado"),
            "bateria": health.get("bateria"),
            "temperatura": health.get("temperatura"),
            "alertas": health.get("alertas", [])
        }

    def recall(self):
        return {
            "recent": recent_events(20),
            "summary": summarize(20)
        }

    def process(self):
        current = self.perceive()
        memory = self.recall()

        events = detect(
            self.previous_state,
            current
        )

        trends = compare(
            self.previous_state,
            current
        )

        context = evaluate(current)

        new_context = [
            item
            for item in context
            if item not in self.previous_context
        ]

        actions = []

        if new_context:
            possible_actions = decide()

            for action in possible_actions:
                relevant = (
                    action["acao"] == "energia_baixa"
                    and "ENERGIA_BAIXA" in new_context
                ) or (
                    action["acao"] == "energia_critica"
                    and "ENERGIA_CRITICA" in new_context
                ) or (
                    action["acao"] == "temperatura_elevada"
                    and "TEMPERATURA_ELEVADA" in new_context
                ) or (
                    action["acao"] == "temperatura_critica"
                    and "TEMPERATURA_CRITICA" in new_context
                )

                if relevant:
                    actions.append(action)

        save(current, context)
        record(current)

        for trend in trends:
            remember(
                "tendencia",
                f"{trend}: {describe_trend(trend)}"
            )

        self.previous_state = current
        self.previous_context = context

        return {
            "estado": current,
            "memoria": memory,
            "eventos": events,
            "tendencias": trends,
            "contexto": new_context,
            "acoes": actions
        }


def show_result(result):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    state = result["estado"]
    summary = result["memoria"]["summary"]

    print()
    print(f"[{now}] 🧠 LIFE ENGINE V1.3")
    print("==============================")

    print()
    print("PERCEPÇÃO")
    print("------------------------------")
    print(f"Estado: {state['estado']}")
    print(f"Bateria: {state['bateria']}%")
    print(f"Temperatura: {state['temperatura']}°C")

    print()
    print("MEMÓRIA")
    print("------------------------------")
    print(f"Registros analisados: {summary['total']}")
    print(
        f"Eventos: {summary['eventos']} | "
        f"Contextos: {summary['contextos']} | "
        f"Reflexos: {summary['reflexos']}"
    )

    print()
    print("EVENTOS")
    print("------------------------------")

    if result["eventos"]:
        for event in result["eventos"]:
            print(f"🧠 {describe_event(event)}")
    else:
        print("• nenhum evento novo")

    print()
    print("TENDÊNCIAS")
    print("------------------------------")

    if result["tendencias"]:
        for trend in result["tendencias"]:
            print(f"📈 {describe_trend(trend)}")
    else:
        print("• nenhuma tendência detectada")

    print()
    print("CONTEXTO")
    print("------------------------------")

    if result["contexto"]:
        for item in result["contexto"]:
            print(f"🔎 {describe(item)}")
    else:
        print("• nenhuma condição nova")

    print()
    print("DECISÃO")
    print("------------------------------")

    if result["acoes"]:
        for action in result["acoes"]:
            print(
                f"⚡ {action['acao']} "
                f"| prioridade={action['prioridade']}"
            )
    else:
        print("• nenhuma ação necessária")

    print()
    print("💾 Estado + contexto + histórico salvos.")
    print("==============================")


if __name__ == "__main__":
    show_result(LifeEngine().process())
