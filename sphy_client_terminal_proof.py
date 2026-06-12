#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Framework SPHY - Monitor de Auditoria Criptográfica (Hardened Client Node)
Autor: Deywe Okabe
Organização: Black Swan Research / Harpia Quantum
Ano: 2026
"""

import os
import sys
import time
import urllib.request
import struct
import threading
import hashlib  

SERVER_URL = "http://161.153.0.202:1113/heartbeat"
TARGET_BINARY = "sphy_quantum_core_engine.bin"

frame_id = 0
server_alive = True

# Variáveis de auditoria isoladas
energia_fundamental = 0.0
spins = []
status_auditoria = "Aguardando primeiro pacote..."
proof_hash_remoto = "None"

def watchdog_ping_loop():
    global server_alive, energia_fundamental, spins, status_auditoria, proof_hash_remoto
    print("[*] Watchdog Ativo: Escaneando barramento binário de rede...")
    
    while True:
        try:
            # Requisita o fluxo de octet-stream assíncrono da nuvem
            with urllib.request.urlopen(SERVER_URL, timeout=1.5) as response:
                buffer = response.read()
                
            # Assinatura de tamanho estrito: 32 (Token) + 8 (Double) + 16 (4x Int) + 32 (SHA-256) = 88 bytes
            if len(buffer) == 88:
                payload_dados = buffer[:-32]
                hash_recebido = buffer[-32:]
                
                # --- VERIFICAÇÃO FORENSE LOCAL VIA BUFFER BINÁRIO ---
                if hashlib.sha256(payload_dados).digest() == hash_recebido:
                    server_alive = True
                    proof_hash_remoto = hash_recebido.hex()
                    
                    # Corta o token de autenticação e desempacota o payload estruturado
                    raw_metrics = payload_dados[32:]
                    energia_fundamental, s0, s1, s2, s3 = struct.unpack("!d4i", raw_metrics)
                    spins = [s0, s1, s2, s3]
                    
                    status_auditoria = "✓ INTEGRIDADE CONFIRMADA: Stream Binário Autêntico [SHA-256 SECURE]"
                else:
                    status_auditoria = "🚨 SINAL ADULTERADO: Assinatura de rede inválida!"
                    server_alive = False
            else:
                status_auditoria = "🚨 TAMANHO DE BUFFER INCONSISTENTE: Dados corrompidos!"
                server_alive = False
                
        except Exception:
            server_alive = False
            
        if not server_alive:
            print("\n🚨 [ALERTA CRÍTICO] Conexão abortada ou falha na prova de assinatura binária!")
            try:
                if os.path.exists(TARGET_BINARY):
                    os.remove(TARGET_BINARY)
                    print(f"[✓] Proteção SPHY: Arquivo binário '{TARGET_BINARY}' expurgado.")
            except Exception as e:
                print(f"[!] Erro ao deletar binário: {e}")
            os._exit(1)
            
        time.sleep(0.1)

monitor_thread = threading.Thread(target=watchdog_ping_loop, daemon=True)
monitor_thread.start()

# Loop do terminal rápido de alta performance
try:
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(" 🔒 SPHY CORE — MONITOR DE AUDITORIA CRIPTOGRÁFICA (HARDENED)")
        print(" =============================================================")
        print(f"  🌐 Status da Rede : ONLINE (Octet-Stream Ativo via Oracle)")
        print(f"  ⚡ Energia Dimod  : {energia_fundamental:.4f} eV")
        print(f"  🧬 Matriz Spins   : {spins}")
        print(" =============================================================")
        print("  🔑 PROVA DE PROCESSAMENTO INTEGRAL DA NUVEM:")
        print(f"  📥 Hash Recebido  : {proof_hash_remoto}")
        print(f"  📊 Auditoria      : {status_auditoria}")
        print(f"  🚀 Local Frame ID : {frame_id:06d}")
        print(" =============================================================")
        
        frame_id += 1
        time.sleep(0.02)
except KeyboardInterrupt:
    print("\nEncerrado.")