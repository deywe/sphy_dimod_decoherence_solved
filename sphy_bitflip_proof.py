#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Framework SPHY - Módulo de Prova de Inversão de Bit (Bit-Flip Simulation)
Autor: Deywe Okabe
Organização: Black Swan Research / Harpia Quantum
Ano: 2026
"""

import os
import sys
import time
import hashlib
import random
import threading  # Corrigido: Importação incluída com sucesso

# Limpa o terminal inicial
os.system('cls' if os.name == 'nt' else 'clear')

print("=" * 60)
print(" 🔒 SPHY CORE — SIMULADOR DE INCURSÃO DE BIT-FLIP")
print("=" * 60)

# Entrada do Operador
try:
    numero_base = int(input(" 📥 Digite o número base para a soma eterna: "))
    iteracoes = 100
except ValueError:
    print("[ERRO] Digite um número inteiro válido!")
    sys.exit(1)

# Variáveis de controle de estado
bit_flip_status = 0.0  # 0.0 = Desativado, 1.0 = Ativado
frame_id = 0
total_anomalias = 0
ultimo_erro = "Nenhum (Estado Determinístico)"

# Thread paralela para capturar a alteração do Bit-Flip sem travar os cálculos de alta velocidade
def escutar_operador():
    global bit_flip_status
    while True:
        try:
            entrada = input()
            if entrada.strip() == "1":
                bit_flip_status = 1.0
            elif entrada.strip() == "0":
                bit_flip_status = 0.0
        except Exception:
            pass

# Corrigido: Sintaxe da thread purificada
menu_thread = threading.Thread(target=escutar_operador, daemon=True)
monitor_thread = monitor_thread = menu_thread.start()

# Loop da Soma Eterna
try:
    while True:
        # --- PROCESSAMENTO CLÁSSICO DETERMINÍSTICO ---
        resultado_esperado = 0
        for _ in range(iteracoes):
            resultado_esperado += numero_base
            
        resultado_processado = resultado_esperado
        
        # --- INJEÇÃO DA ANOMALIA (BIT-FLIP SIMULADO) ---
        anomalia_detectada_neste_frame = False
        if bit_flip_status == 1.0:
            if random.random() < 0.4:  # 40% de chance de ruído por frame
                # Seleciona um bit aleatório (potência de 2) e aplica o operador XOR (^)
                bit_alvo = 2 ** random.randint(0, 12)
                resultado_processado = resultado_processado ^ bit_alvo
                anomalia_detectada_neste_frame = True
                total_anomalias += 1
                ultimo_erro = f"Bit-Flip! Original {resultado_esperado} virou {resultado_processado}"

        # --- AUDITORIA DE INTEGRIDADE (SHA-256) ---
        hash_esperado = hashlib.sha256(str(resultado_esperado).encode('utf-8')).hexdigest()
        hash_processado = hashlib.sha256(str(resultado_processado).encode('utf-8')).hexdigest()
        
        if hash_esperado == hash_processado:
            status_auditoria = "   DETERMINISTICO ESTAVEL"
        else:
            status_auditoria = "🚨 ANOMALIA DE BIT-FLIP DETECTADA!"

        # --- IMPRESSÃO DOS DADOS NO TERMINAL ---
        os.system('cls' if os.name == 'nt' else 'clear')
        print(" 🔒 SPHY — MONITOR DE SOMA ETERNA & COERÊNCIA DE BIT")
        print(" =============================================================")
        print(f"  🚀 Frame ID        : {frame_id:06d}")
        print(f"  🔢 Número Base      : {numero_base}")
        print(f"  🔄 Ciclos por Frame : {iteracoes} somas acumuladas")
        print(" =============================================================")
        print(f"  📊 MATEMÁTICA DO PROCESSO:")
        print(f"  🔹 Valor Esperado   : {resultado_esperado}")
        print(f"  🔸 Valor Obtido     : {resultado_processado}")
        print(f"  🔑 Hash Assinatura  : {hash_processado}")
        print(" =============================================================")
        print(f"  🧬 CONTROLADOR QUÂNTICO:")
        print(f"  ⚙️  Bit-Flip Ativo  : {bit_flip_status}  (Digite 1 + Enter para ativar / 0 + Enter para desativar)")
        print(f"  ⚡ Status Auditoria : {status_auditoria}")
        print(f"  ⚠️  Total de Flips  : {total_anomalias:05d} falhas registradas")
        print(f"  🕒 Registro Hist.  : {ultimo_erro}")
        print(" =============================================================")
        print(" Pressione CTRL+C para parar.")
        
        frame_id += 1
        time.sleep(0.08)

except KeyboardInterrupt:
    print("\n[-] Simulação encerrada.")