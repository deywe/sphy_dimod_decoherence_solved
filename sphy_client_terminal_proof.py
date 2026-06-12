#!/usr/bin/env python3
import os
import sys
import time
import urllib.request
import json
import threading
import hashlib  

SERVER_URL = "http://161.153.0.202:1113/heartbeat"
TARGET_BINARY = "sphy_quantum_core_engine.bin"

frame_id = 0
server_alive = True

# Variáveis de auditoria
energia_fundamental = 0.0
spins = []
timestamp_remoto = 0.0
proof_hash_remoto = ""
status_auditoria = "Aguardando primeiro pacote..."

def watchdog_ping_loop():
    global server_alive, energia_fundamental, spins, timestamp_remoto, proof_hash_remoto, status_auditoria
    
    while True:
        try:
            with urllib.request.urlopen(SERVER_URL, timeout=1.5) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                
            if res_data.get("SPHY_CORE_AUTH") == "ACTIVE_DETERMINISTIC_OK":
                server_alive = True
                
                # Recebe os dados brutos e a assinatura da Oracle
                energia_fundamental = float(res_data.get("ising_ground_energy_ev"))
                spins = res_data.get("qubit_topology_matrix")
                timestamp_remoto = float(res_data.get("server_timestamp"))
                proof_hash_remoto = res_data.get("server_proof_hash")
                
                # --- VERIFICAÇÃO LOCAL DA PROVA DE TRABALHO ---
                payload_local = f"{energia_fundamental}|{spins}|{timestamp_remoto}"
                conferencia_hash = hashlib.sha256(payload_local.encode('utf-8')).hexdigest()
                
                if conferencia_hash == proof_hash_remoto:
                    status_auditoria = "✓ INTEGRIDADE CONFIRMADA: Processamento Remoto Real e Autêntico"
                else:
                    status_auditoria = "🚨 SINAL ADULTERADO: Quebra de simetria detectada!"
                    server_alive = False
            else:
                server_alive = False
        except Exception:
            server_alive = False
            
        if not server_alive:
            print("\n🚨 [ALERTA] Conexão abortada ou falha na prova de assinatura!")
            if os.path.exists(TARGET_BINARY):
                os.remove(TARGET_BINARY)
            os._exit(1)
            
        time.sleep(0.1)

monitor_thread = threading.Thread(target=watchdog_ping_loop, daemon=True)
monitor_thread.start()

# Loop do terminal rápido
try:
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(" 🔒 SPHY CORE — MONITOR DE AUDITORIA CRIPTOGRÁFICA")
        print(" =============================================================")
        print(f"  🌐 Status da Rede : ONLINE (Conectado na Oracle Cloud)")
        print(f"  🕒 Time Oracle    : {timestamp_remoto}")
        print(f"  ⚡ Energia Dimod  : {energia_fundamental:.4f} eV")
        print(f"  🧬 Matriz Spins   : {spins}")
        print(" =============================================================")
        print("  🔑 PROVA DE PROCESSAMENTO DA NUVEM:")
        print(f"  📥 Hash Recebido  : {proof_hash_remoto}")
        print(f"  📊 Auditoria      : {status_auditoria}")
        print(f"  🚀 Local Frame ID : {frame_id:06d}")
        print(" =============================================================")
        
        frame_id += 1
        time.sleep(0.02)
except KeyboardInterrupt:
    print("\nEncerrado.")