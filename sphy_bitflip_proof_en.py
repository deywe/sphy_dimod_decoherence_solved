#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPHY Framework - Bit-Flip Incursion Proof Module (Hardened Simulation Node)
Author: Deywe Okabe
Organization: Black Swan Research / Harpia Quantum
Year: 2026
"""

import os
import sys
import time
import hashlib
import random
import threading
import struct

# Clear the terminal at startup
os.system('cls' if os.name == 'nt' else 'clear')

print("=" * 60)
print(" 🔒 SPHY CORE — BIT-FLIP INCURSION SIMULATOR (HARDENED)")
print("=" * 60)

# Operator Input
try:
    base_number = int(input(" 📥 Enter the base number for the infinite summation: "))
    iterations = 100
except ValueError:
    print("[ERROR] Please enter a valid integer!")
    sys.exit(1)

# State Control Variables (Numeric Isolation)
bit_flip_status = 0.0  # 0.0 = Disabled, 1.0 = Enabled
frame_id = 0
total_anomalies = 0

# Sinalizadores dinâmicos em RAM para mitigar strings estáticas
corruption_flag = 0  # 0 = Clean, 1 = Corrupted
value_at_drift = 0

# Parallel thread to capture operator toggles without freezing the high-speed execution
def operator_input_listener():
    global bit_flip_status
    while True:
        try:
            user_input = input()
            if user_input.strip() == "1":
                bit_flip_status = 1.0
            elif user_input.strip() == "0":
                bit_flip_status = 0.0
        except Exception:
            pass

menu_thread = threading.Thread(target=operator_input_listener, daemon=True)
menu_thread.start()

# Infinite Summation Loop
try:
    while True:
        # --- DETERMINISTIC CLASSICAL PROCESSING ---
        expected_value = 0
        for _ in range(iterations):
            expected_value += base_number
            
        processed_value = expected_value
        
        # --- ANOMALY INJECTION (SIMULATED QUBIT BIT-FLIP) ---
        if bit_flip_status == 1.0:
            if random.random() < 0.4:  # 40% noise probability per frame
                bit_target = 2 ** random.randint(0, 12)
                # Aplica a falha via XOR aritmético direto no registrador
                processed_value = processed_value ^ bit_target
                total_anomalies += 1
                corruption_flag = 1
                value_at_drift = processed_value
        else:
            if frame_id == 0 or corruption_flag == 0:
                corruption_flag = 0

        # --- INTEGRITY FORENSIC AUDIT (PROTECTED STRUCT HASHING) ---
        # Removido o overhead de texto clássico: processamento 100% binário em Quadword (!q)
        bytes_expected = struct.pack("!q", expected_value)
        bytes_processed = struct.pack("!q", processed_value)
        
        expected_hash = hashlib.sha256(bytes_expected).hexdigest()
        processed_hash = hashlib.sha256(bytes_processed).hexdigest()
        
        # Montagem efêmera das strings textuais apenas no buffer de renderização do frame
        if expected_hash == processed_hash:
            audit_status = "   STABLE DETERMINISTIC"
            corruption_flag = 0  # Auto-reseta flag se o estado for idêntico
        else:
            audit_status = "🚨 BIT-FLIP ANOMALY DETECTED!"
            
        last_error_log = f"Bit-Flip! Original {expected_value} corrupted to {value_at_drift}" if corruption_flag == 1 else "None (Deterministic State)"

        # --- TERMINAL HUD RENDER ---
        os.system('cls' if os.name == 'nt' else 'clear')
        print(" 🔒 SPHY — INFINITE SUMMATION & BIT COHERENCE MONITOR")
        print(" =============================================================")
        print(f"  🚀 Frame ID        : {frame_id:06d}")
        print(f"  🔢 Base Number      : {base_number}")
        print(f"  🔄 Cycles / Frame  : {iterations} accumulated additions")
        print(" =============================================================")
        print(f"  📊 PROCESS MATHEMATICS (BINARY PACKED):")
        print(f"  🔹 Expected Value   : {expected_value}")
        print(f"  🔸 Processed Value  : {processed_value}")
        print(f"  🔑 Hash Signature  : {processed_hash}")
        print(" =============================================================")
        print(f"  🧬 QUANTUM CONTROLLER:")
        print(f"  ⚙️  Bit-Flip Status : {bit_flip_status}  (Type 1 + Enter to Activate / 0 + Enter to Deactivate)")
        print(f"  ⚡ Audit Status    : {audit_status}")
        print(f"  ⚠️  Total Flips     : {total_anomalies:05d} anomalies registered")
        print(f"  🕒 Historical Log   : {last_error_log}")
        print(" =============================================================")
        print(" Press CTRL+C to halt process.")
        
        frame_id += 1
        time.sleep(0.08)

except KeyboardInterrupt:
    print("\n[-] Simulation halted by operator.")
finally:
    print("[✓] Session terminated securely.")