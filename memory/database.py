#!/usr/bin/env python3

import os
import sqlite3
from datetime import datetime

MEMORY_DIR=os.path.expanduser("~/lifecore/memory")
DATABASE=os.path.join(MEMORY_DIR,"lifecore.db")

def connect():
    os.makedirs(MEMORY_DIR,exist_ok=True)
    return sqlite3.connect(DATABASE)

def initialize():
    with connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT,timestamp TEXT NOT NULL,tipo TEXT NOT NULL,conteudo TEXT NOT NULL)""")
        db.commit()

def remember(tipo,conteudo):
    initialize(); timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with connect() as db:
        db.execute("INSERT INTO memories (timestamp,tipo,conteudo) VALUES (?,?,?)",(timestamp,tipo,conteudo)); db.commit()

def recall(limit=10):
    initialize()
    with connect() as db:
        return db.execute("SELECT timestamp,tipo,conteudo FROM memories ORDER BY id DESC LIMIT ?",(limit,)).fetchall()

def show_memory(limit=10):
    memories=recall(limit)
    print("\n🧠 MEMÓRIA DO LIFECORE\n======================")
    if not memories: print("Memória vazia.")
    else:
        for timestamp,tipo,conteudo in reversed(memories): print(f"[{timestamp}] {tipo}: {conteudo}")
    print("======================")

if __name__=="__main__": initialize(); show_memory()
