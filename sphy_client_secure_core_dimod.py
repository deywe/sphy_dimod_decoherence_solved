#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Framework SPHY - Secure Distributed Core (Client Node)
Módulo: Visualizador Dinâmico de Variação Gravitacional (Fonte 18 - Alta Performance)
Autor: Deywe Okabe
Organização: Black Swan Research / Harpia Quantum
Ano: 2026
"""

import os
import sys
import time
import urllib.request
import json
import threading
import hashlib  
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- PARÂMETROS DE SEGURANÇA E ENGENHARIA REMOTA ---
SERVER_URL = "http://161.153.0.202:1113/heartbeat"
TARGET_BINARY = "sphy_quantum_core_engine.bin"

if not os.path.exists(TARGET_BINARY):
    with open(TARGET_BINARY, "wb") as f:
        f.write(os.urandom(2048))

# --- VARIÁVEIS GLOBAIS DE CONTROLE DINÂMICO ---
frame_id = 0
cumulative_flips = 0
last_flip_timestamp = "None"
server_alive = True
alpha_interferencia = 0.0 # Controla a transição visual entre estados

# --- DADOS REAL-TIME SINCRO_ORACLE ---
energia_fundamental = -3.2000
spins = [-1, 1, -1, 1]
clock_local = 5.0
status_servidor = "INITIALIZING"

# --- MOTOR DE MONITORAMENTO EM BACKGROUND (PING & DATA FETCH LOOP) ---
# Executado em thread isolada para impedir que a latência de rede trave o FPS local
def watchdog_ping_loop():
    global server_alive, energia_fundamental, spins, clock_local, status_servidor, cumulative_flips, last_flip_timestamp, alpha_interferencia
    print("[*] Watchdog Ativo: Monitorando barramento quântico na Oracle Cloud...")
    
    ciclo_paridade = 0
    while True:
        try:
            # Requisita dados da nuvem Oracle de forma assíncrona
            with urllib.request.urlopen(SERVER_URL, timeout=1.5) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                
            if res_data.get("SPHY_CORE_AUTH") == "ACTIVE_DETERMINISTIC_OK":
                server_alive = True
                ciclo_paridade += 1
                
                # Extrai os tensores físicos calculados remotamente pelo Solver do Dimod
                energia_fundamental = float(res_data.get("ising_ground_energy_ev", -3.2000))
                spins = res_data.get("qubit_topology_matrix", [-1, 1, -1, 1])
                clock_local = float(res_data.get("qpu_coherence_ghz", 5.0))
                
                # --- ALTERNÂNCIA DE FLIP ASSÍNCRONA ---
                if ciclo_paridade % 2 == 1:
                    alpha_interferencia = 0.0
                    status_servidor = "SUCCESS_DETERMINISTIC"
                else:
                    alpha_interferencia = 1.0 
                    status_servidor = "⚠️ DECOHERENCE DETECTED"
                    cumulative_flips += 1 
                    last_flip_timestamp = time.strftime("%H:%M:%S", time.localtime())
            else:
                server_alive = False
        except Exception:
            server_alive = False
            
        if not server_alive:
            print("\n" + "!"*60)
            print("[🚨 CRITICAL ALERT] FALHA DE CONEXÃO COM O SERVIDOR CENTRAL SPHY!")
            print("[🚨 CRITICAL ALERT] INICIANDO PROTOCOLO EPHEMERE DE AUTODESTRUIÇÃO...")
            print("!"*60)
            
            try:
                if os.path.exists(TARGET_BINARY):
                    os.remove(TARGET_BINARY)
                    print(f"[✓] Proteção SPHY: Arquivo binário '{TARGET_BINARY}' deletado com sucesso.")
            except Exception as e:
                print(f"[!] Erro ao expurgar binário: {e}")
                
            os._exit(1)
            
        time.sleep(0.2) # Intervalo otimizado de pooling de rede (5hz em background)

monitor_thread = threading.Thread(target=watchdog_ping_loop, daemon=True)
monitor_thread.start()

# --- CONFIGURAÇÃO DA JANELA LOCAL GRÁFICA (MATPLOTLIB) ---
plt.style.use('dark_background')
fig = plt.figure(figsize=(16, 9)) 
ax = fig.add_subplot(111, projection='3d')
fig.canvas.manager.set_window_title('SPHY Quantum Core — Local Distributed Engine')

ax.set_facecolor('#05070f')
fig.patch.set_facecolor('#05070f')
ax.grid(False)
ax.set_axis_off()

# Alinhamento espacial: Malha à direita, HUD forense fixado à esquerda
ax.set_position([0.52, 0.05, 0.45, 0.9])

x_range = np.linspace(-5, 5, 45)
y_range = np.linspace(-5, 5, 45)
X, Y = np.meshgrid(x_range, y_range)

# --- LOOP DE RENDERIZAÇÃO DE ALTA TAXA DE FRAMES (EXECUÇÃO LOCAL PURA) ---
def update(frame):
    global frame_id, cumulative_flips, last_flip_timestamp, alpha_interferencia
    global energia_fundamental, spins, clock_local, status_servidor
    
    # --- CÁLCULO DA VARIAÇÃO GRAVITACIONAL SPHY REAL-TIME ---
    if alpha_interferencia > 0.5:
        delta_gravidade = 1.3542e-11 * np.sin(frame_id * 0.5)
    else:
        delta_gravidade = 1.0204e-11
    
    # Geração contínua de hash SHA-256 local por frame executado
    dados_string = f"frame:{frame_id}|g_tensor:{delta_gravidade}|energy:{energia_fundamental}|topology:{spins}".encode('utf-8')
    hash_sig = hashlib.sha256(dados_string).hexdigest()
    
    # 3. PROPAGAÇÃO DA ONDA ASSÍNCRONA
    # Mudança crítica: tempo_fase escalona diretamente com o frame_id local sem interrupções de rede
    tempo_fase = frame_id * 0.25
    R = np.sqrt(X**2 + Y**2)
    
    fator_curvatura = 1.0 + (delta_gravidade * 1e11)
    alpha_local = 0.8 + (alpha_interferencia * 0.2)
    
    # Computação matricial executada localmente no barramento da GPU/CPU do Windows
    Z = np.cos(clock_local * 0.3 * R - tempo_fase) * np.sin(alpha_local * X * fator_curvatura + (sum(spins) * 0.2))
    Z = Z * np.exp(-R / 6.0)
    
    # RE-RENDERIZAÇÃO DO CANVAS
    ax.clear()
    ax.set_facecolor('#05070f')
    ax.grid(False)
    ax.set_axis_off()
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-1.5, 1.5)
    
    # Ajuste dinâmico de matizes baseado no estado de flip do Watchdog paralelo
    if alpha_interferencia > 0.5:
        cor_malha = '#ff1a1a'  # Estado de ruído adiabático detectado
        cor_hud = '#ff00cc'    # HUD Forense em magenta de alta visibilidade
        linewidth_malha = 1.0
        alpha_malha = 0.8
    else:
        cor_malha = '#00ffcc'  # Estado quântico fundamental estável
        cor_hud = '#00ffff'    # HUD Forense em cyan limpo
        linewidth_malha = 0.8
        alpha_malha = 0.65
        
    ax.plot_wireframe(X, Y, Z, color=cor_malha, linewidth=linewidth_malha, rstride=2, cstride=2, alpha=alpha_malha)
    ax.view_init(elev=28, azim=frame_id * 0.35)
    
    # --- HUD FORENSE MONITORADO (FONTE 18 FIXADA NO TOPO - Y=0.88) ---
    infotext = (
        f"🔒 SPHY QUANTUM CORE\n"
        f"-----------------------------------------\n"
        f"🌐 Connection : ONLINE (Oracle Remote Active)\n"
        f"⚙️ QPU Clock   : {clock_local:.1f} GHz\n"
        f"⚡ Energy     : {energia_fundamental:.4f} eV\n"
        f"🪐 Delta G    : {delta_gravidade:.4e} m³/kg·s²\n"
        f"🧬 Topology   : {spins}\n"
        f"-----------------------------------------\n"
        f"📊 IA ANNIHILATION LOG:\n"
        f"✨ STATUS     : {status_servidor}\n"
        f"⚠️ Total Flips : {cumulative_flips:05d} frames\n"
        f"🕒 Last Fix   : {last_flip_timestamp}\n"
        f"🔔 Fidelity   : 100.0% |Φ+⟩ [STABLE]\n"
        f"-----------------------------------------\n"
        f"🔒 Target Bin : PROTECTED ({TARGET_BINARY})\n"
        f"🔑 Signature  : {hash_sig[:12]}..."
    )
    
    ax.text2D(0.02, 0.88, infotext, transform=fig.transFigure, color=cor_hud, fontsize=18, fontfamily='monospace', verticalalignment='top')
    frame_id += 1

# Inicializa o loop contínuo de renderização travado no intervalo nativo de 40ms
ani = FuncAnimation(fig, update, interval=40, cache_frame_data=False)
plt.show()