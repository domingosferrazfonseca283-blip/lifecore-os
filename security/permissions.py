#!/usr/bin/env python3
SAFE_ACTIONS={"energia_baixa":{"permitida":True,"requer_confirmacao":False},"energia_critica":{"permitida":True,"requer_confirmacao":False},"temperatura_elevada":{"permitida":True,"requer_confirmacao":False},"temperatura_critica":{"permitida":True,"requer_confirmacao":False},"nenhuma":{"permitida":True,"requer_confirmacao":False}}
def is_allowed(action):
    permission=SAFE_ACTIONS.get(action); return False if permission is None else permission["permitida"]
def needs_confirmation(action):
    permission=SAFE_ACTIONS.get(action); return True if permission is None else permission["requer_confirmacao"]
def check(action): return {"acao":action,"permitida":is_allowed(action),"confirmacao":needs_confirmation(action)}
