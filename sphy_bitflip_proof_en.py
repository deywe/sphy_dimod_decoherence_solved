#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPHY Framework - Bit-Flip Incursion Proof Module (Simulation Node)
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

# Clear the terminal at startup
os.system('cls' if os.name == 'nt' else 'clear')

print("=" * 60)
print(" 🔒 SPHY CORE — BIT-FLIP INCURSION SIMULATOR")
print("=" * 60)

# Operator Input
try:
    base_number = int(input(" 📥 Enter the base number for the infinite summation: "))
    iterations = 100
except ValueError:
    print("[ERROR] Please enter a valid integer!")
    sys.exit(1)

# State Control Variables
bit_flip_status = 0.0  # 0.0 = Disabled, 1.0 = Enabled
frame_id = 0
total_anomalies = 0
last_error_log = "None (Deterministic State)"

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
        # The exact mathematical result expected in a noise-free environment
        expected_value = 0
        for _ in range(iterations):
            expected_value += base_number
            
        processed_value = expected_value
        
        # --- ANOMALY INJECTION (SIMULATED QUBIT BIT-FLIP) ---
        if bit_flip_status == 1.0:
            if random.random() < 0.4:  # 40% noise probability per frame
                # Select a random bit target (power of 2) and apply bitwise XOR (^)
                bit_target = 2 ** random.randint(0, 12)
                processed_value = processed_value ^ bit_target
                total_anomalies += 1
                last_error_log = f"Bit-Flip! Original {expected_value} corrupted to {processed_value}"

        # --- INTEGRITY FORENSIC AUDIT (SHA-256) ---
        expected_hash = hashlib.sha256(str(expected_value).encode('utf-8')).hexdigest()
        processed_hash = hashlib.sha256(str(processed_value).encode('utf-8')).hexdigest()
        
        if expected_hash == processed_hash:
            audit_status = "   STABLE DETERMINISTIC"
        else:
            audit_status = "🚨 BIT-FLIP ANOMALY DETECTED!"

        # --- TERMINAL HUD RENDER ---
        os.system('cls' if os.name == 'nt' else 'clear')
        print(" 🔒 SPHY — INFINITE SUMMATION & BIT COHERENCE MONITOR")
        print(" =============================================================")
        print(f"  🚀 Frame ID        : {frame_id:06d}")
        print(f"  🔢 Base Number      : {base_number}")
        print(f"  🔄 Cycles / Frame  : {iterations} accumulated additions")
        print(" =============================================================")
        print(f"  📊 PROCESS MATHEMATICS:")
        print(f"  🔹 Expected Value   : {expected_value}")
        print(f"  🔸 Processed Value  : {processed_value}")
        print(f"  🔑 Hash Signature   : {processed_hash}")
        print(" =============================================================")
        print(f"  🧬 QUANTUM CONTROLLER:")
        print(f"  ⚙️  Bit-Flip Status : {bit_flip_status}  (Type 1 + Enter to Activate / 0 + Enter to Deactivate)")
        print(f"  ⚡ Audit Status    : {audit_status}")
        print(f"  ⚠️  Total Flips     : {total_anomalias:05d} anomalies registered") if 'total_anomalias' in locals() else print(f"  ⚠️  Total Flips     : {total_anomalies:05d} anomalies registered")
        print(f"  🕒 Historical Log   : {last_error_log}")
        print(" =============================================================")
        print(" Press CTRL+C to halt process.")
        
        frame_id += 1
        time.sleep(0.08)

except KeyboardInterrupt:
    print("\n[-] Simulation halted by operator.")
finally:
    print("[✓] Session terminated securely.")