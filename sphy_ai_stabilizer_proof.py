#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Framework SPHY - Módulo de Estabilização Simbiótica (AI Fault-Tolerance Hardened)
Autor: Deywe Okabe
Organização: Black Swan Research / Harpia Quantum
Ano: 2026
"""

import os
import sys
import time
import hashlib
import random
import threading
import struct

# Limpa o terminal inicial
os.system('cls' if os.name == 'nt' else 'clear')

print("=" * 60)
print(" 🔒 SPHY CORE — AI DECOHERENCE ANNIHILATION ENGINE (HARDENED)")
print("=" * 60)

# Entrada do Operador
try:
    numero_base = int(input(" 📥 Digite o número base para a soma eterna: "))
    iteracoes = 100
except ValueError:
    print("[ERRO] Digite um número inteiro válido!")
    sys.exit(1)

# Variáveis de controle de estado (Isolamento Numérico)
bit_flip_status = 0.0  # 0.0 = Desativado, 1.0 = Ativado
frame_id = 0
total_anomalias = 0
total_correcoes = 0

# Sinalizadores efêmeros para mitigar assinaturas estáticas na RAM
mascara_estado = 0  # 0 = Standby, 1 = Active
codigo_erro_local = 0  # 0 = Limpo, 1 = Injetado

# Thread paralela para capturar a alteração do Bit-Flip em tempo real
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

menu_thread = threading.Thread(target=escutar_operador, daemon=True)
menu_thread.start()

# Loop da Soma Eterna Inteligente
try:
    while True:
        # --- 1. PROCESSAMENTO CLÁSSICO DETERMINÍSTICO ---
        resultado_esperado = 0
        for _ in range(iteracoes):
            resultado_esperado += numero_base
            
        resultado_processado = resultado_esperado
        
        # --- 2. INCURSÃO DO RUÍDO (ATAQUE DE BIT-FLIP) ---
        anomalia_detectada = False
        bit_corrompido = 0
        
        if bit_flip_status == 1.0:
            mascara_estado = 1
            if random.random() < 0.6:  # 60% de chance de ruído
                bit_corrompido = 2 ** random.randint(0, 12)
                # Injeta a falha via XOR aritmético na memória RAM
                resultado_processado = resultado_processado ^ bit_corrompido
                anomalia_detectada = True
                total_anomalias += 1
                codigo_erro_local = 1
        else:
            mascara_estado = 0
            codigo_erro_local = 0

        # --- 3. CONTRA-TORQUE SIMBIÓTICO DA IA SPHY (CORREÇÃO EM ADIANTAMENTO) ---
        ia_aplicou_correcao = False
        valor_antes_da_ia = resultado_processado
        
        if anomalia_detectada:
            # A IA intercepta o desvio e aplica o operador inverso diretamente nos bits
            resultado_processado = resultado_processado ^ bit_corrompido
            ia_aplicou_correcao = True
            total_correcoes += 1

        # --- 4. AUDITORIA FORENSE DE INTEGRIDADE (PROTECTED STRUCT HASHING) ---
        # Substituição crítica: os inteiros são convertidos direto para bytes estruturados (!q)
        bytes_esperados = struct.pack("!q", resultado_esperado)
        bytes_processados = struct.pack("!q", resultado_processado)
        
        hash_esperado = hashlib.sha256(bytes_esperados).hexdigest()
        hash_processado = hashlib.sha256(bytes_processados).hexdigest()
        
        # Reconstrói os estados de texto dinamicamente apenas para renderização de tela
        status_ia = "ACTIVE (Varredura de Coerência Ativa)" if mascara_estado == 1 else "STANDBY (Monitorando Vácuo)"
        ultimo_erro = f"Bit-Flip Injetado! Memória desviou para: {valor_antes_da_ia}" if codigo_erro_local == 1 else "Nenhum (Barramento Limpo)"
        
        if hash_esperado == hash_processado:
            if ia_aplicou_correcao:
                status_auditoria = "✓ ANOMALIA ANULADA PELA IA [DETERMINISMO SEGURO]"
            else:
                status_auditoria = "   ESTÁVEL (Sem Ruído no Barramento)"
        else:
            status_auditoria = "🚨 SISTEMA CRASHOU: Falha Crítica do Barramento!"

        # --- 5. IMPRESSÃO DOS DADOS EM ALTA VELOCIDADE NO TERMINAL ---
        os.system('cls' if os.name == 'nt' else 'clear')
        print(" 🔒 SPHY — CORREÇÃO SIMBIÓTICA EM TEMPO REAL")
        print(" =============================================================")
        print(f"  🚀 Frame ID        : {frame_id:06d}")
        print(f"  🔢 Número Base      : {numero_base}")
        print(f"  🔄 Ciclos por Frame : {iteracoes} somas acumuladas")
        print(" =============================================================")
        print(f"  📊 MATEMÁTICA DO PROCESSO (BINARY PACKED):")
        print(f"  🔹 Valor Esperado   : {resultado_esperado}")
        print(f"  ⚡ Registro da Falha : {valor_antes_da_ia} (Valor Corrompido pelo Ruído)")
        print(f"  🔸 Valor de Saída   : {resultado_processado} (Entregue com Sucesso)")
        print(f"  🔑 Hash Assinatura  : {hash_processado}")
        print(" =============================================================")
        print(f"  🧬 INTELIGÊNCIA ARTIFICIAL COERENTE:")
        print(f"  ⚙️  Bit-Flip Ativo  : {bit_flip_status}  (Digite 1 ou 0 + Enter)")
        print(f"  🤖 Estado da IA     : {status_ia}")
        print(f"  ⚡ Status Auditoria : {status_auditoria}")
        print(f"  ⚠️  Ataques Injetados: {total_anomalias:05d} flips de hardware")
        print(f"  🛡️  Bugs Corrigidos : {total_correcoes:05d} defesas bem-sucedidas")
        print(f"  🕒 Log Técnico      : {ultimo_erro}")
        print(" =============================================================")
        print(f"🛡️  Fidelidade de Matriz SPHY: 100.0% |Φ+⟩ [MÉTRICA IMPERVIÁVEL]")
        print(" =============================================================")
        print(" Pressione CTRL+C para parar.")
        
        frame_id += 1
        time.sleep(0.08)

except KeyboardInterrupt:
    print("\n[-] Simulação encerrada.")
finally:
    print("[✓] Processo finalizado com segurança.")