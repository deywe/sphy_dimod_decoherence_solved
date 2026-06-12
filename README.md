# SPHY Framework & Dimod Annealer Simulation Suite
https://sphywow1977.streamlit.app/
Welcome to the **SPHY Framework** repository. This distributed computing environment is designed to demonstrate, benchmark, and audit the resilience of quantum-inspired algorithms and adiabatic annealing loops against hardware-level noise, such as decoherence and bit-flips.

This project is provided as a **free, open-source service** for any researcher, student, or developer who wants to explore the mechanics of the `dimod` SDK, Ising model optimizations, and real-time fault-tolerance architectures.

---

## 🌌 System Architecture Overview

The framework operates on a **Two-Tier Distributed Architecture** to isolate heavy mathematical workloads from the local rendering and monitoring nodes:

1. **Remote Cloud Layer (Backend):** Anchored on an Ubuntu server (Oracle Cloud), executing the `dimod` ExactSolver to compute ground-state energy configurations.
2. **Local Client Layer (Frontend):** Running on Windows/Linux nodes to capture streaming data, perform cryptographic forensic audits (SHA-256), and render visualizations or high-speed terminal logs.

---

## 📄 Script Directory & Functionality

### 1. `sphy_heartbeat_server.py` (Server-Side)
* **Role:** The Core Engine Backend.
* **Environment:** Ubuntu (Cloud Remote Gateway).
* **Description:** A high-performance FastAPI server that initializes a 4-qubit Ising problem topology. Every time the endpoint `/heartbeat` is pinged, it calls `dimod.ExactSolver()`, handles adiabatic simulations, samples the Binary Quadratic Model (BQM), generates a cryptographically secure server-side timestamp, and signs the execution payload with a unique SHA-256 verification token.

### 2. `sphy_client_secure_core_dimod.py` (Client-Side Visualizer)
* **Role:** 3D Space-Time Metric Render Node.
* **Environment:** Windows / Local Machine (Matplotlib).
* **Description:** Connects to the remote cloud server to fetch real-time spin configurations. It translates the Ising ground-energy state into a geometric grid deformation, rendering an interactive 3D topology wireframe using `matplotlib`. It runs parallel threads to keep network pooling independent of frame rendering rates.

### 3. `sphy_client_terminal_proof.py` (Client-Side Auditor)
* **Role:** Forensic Cryptographic Verifier.
* **Environment:** Windows / Local Machine (Terminal Mode).
* **Description:** A lightweight, high-speed console script built to prove the authenticity of remote processing without graphical overhead. It intercepts the cloud packet, reads the server's proof-hash, and recalculates the SHA-256 string locally. If the hashes match, it mathematically confirms that the data stream is real and untampered.

### 4. `sphy_bitflip_proof_en.py` (Simulation Node)
* **Role:** Hardware Vulnerability Demonstration.
* **Environment:** Windows / Local Machine (Terminal Mode).
* **Description:** Simulates an environment under extreme thermal noise or malicious interference. The operator can toggle a bit-flip state (`0.0` to `1.0`) via the keyboard. When active, it randomly forces bitwise XOR (`^`) operations on active memory addresses during an infinite summation loop, showing how classical calculations instantly crash and lose cryptographic integrity.

### 5. `sphy_ai_stabilizer_proof_en.py` (Simulation Node)
* **Role:** Symbiotic Error-Correction Proof.
* **Environment:** Windows / Local Machine (Terminal Mode).
* **Description:** Demonstrates how intelligent fault-tolerance can make physical bit-flips entirely irrelevant. Even when hardware noise corrups the memory register, a simulated SPHY active error-correction layer calculates the deviation vector and re-stabilizes the bits on the fly. The dashboard shows anomalies ticking up, while the output payload and its SHA-256 signature remain perfectly stable.

---

## 🛠️ Requirements & Installation

To deploy the complete ecosystem (Server and Client environments), you must install the following standard and advanced libraries. 

### Core Dependencies

```bash
pip install dimod fastapi uvicorn numpy matplotlib

```

### Future Media & High-Fidelity Rendering Extensions

For advanced visual deployments, vector physics, and upcoming canvas UI implementations, ensure your environment is equipped with the `py5` ecosystem:

```bash
pip install py5

```

*(Note: `py5` requires a valid Java Runtime Environment (JRE) configured on your system path).*

---

## 🔒 Security Notice & Ephemeral Protocol

All client nodes are equipped with an active network **Watchdog Protection Protocol**. If connection to the remote cloud instance is interrupted or if a signature mismatch is detected, the local runtime automatically triggers an emergency teardown, expurgating volatile target binaries (`sphy_quantum_core_engine.bin`) from disk storage to ensure isolation.

---

## ✒️ Signature & Credits

Developed and maintained as a contribution to open quantum research by:

**Deywe Okabe** *Harpia Quantum Deep Tech* *Black Swan Researcher* *Year: 2026* ---
*Feel free to clone this repository, test your own Ising matrices, and contribute to the development of fault-tolerant quantum software mechanics!*
