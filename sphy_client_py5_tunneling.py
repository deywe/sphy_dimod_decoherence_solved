import py5
import urllib.request
import struct
import hashlib
import threading
import time

# --- DIRETRIZES DE REDE REMOTE GATEWAY ---
SERVER_URL = "http://161.153.0.202:1113/tunnel"

# Variáveis de controle assíncrono
prob_density_vector = []
grid_size = 300
server_connected = True
lock = threading.Lock()

def watchdog_binary_stream():
    global prob_density_vector, grid_size, server_connected
    print("[*] Watchdog Binário Ativo: Decodificando pacotes SPHY...")
    
    while True:
        try:
            with urllib.request.urlopen(SERVER_URL, timeout=2.0) as response:
                buffer = response.read()
            
            if len(buffer) >= 2432:  # 32 (token) + 2400 (300 doubles) + 32 (SHA-256)
                payload_dados = buffer[:-32]
                hash_recebido = buffer[-32:]
                
                # Validação Forense do Hash
                if hashlib.sha256(payload_dados).digest() == hash_recebido:
                    token = payload_dados[:32]
                    raw_floats = payload_dados[32:]
                    
                    # Desempacota 300 doubles (8 bytes cada) de big-endian (!)
                    val_array = struct.unpack(f"!{grid_size}d", raw_floats)
                    
                    server_connected = True
                    with lock:
                        prob_density_vector = list(val_array)
                else:
                    server_connected = False  # Hash corrompido ou adulterado
        except Exception as e:
            server_connected = False
            
        time.sleep(0.03)

monitor_thread = threading.Thread(target=watchdog_binary_stream, daemon=True)
monitor_thread.start()

def setup():
    py5.size(1000, 600)  # Corrigido: size substitui o create_canvas
    py5.background(10)
    py5.frame_rate(60)

def draw():
    global prob_density_vector, grid_size, server_connected
    
    py5.no_stroke()
    py5.fill(10, 10, 20, 40)
    py5.rect(0, 0, py5.width, py5.height)
    
    axis_y = 500
    
    # Desenha Barreira
    py5.fill(255, 50, 100, 160)
    barrier_w = 20 * (py5.width / grid_size)
    barrier_x = (grid_size // 2 - 10) * (py5.width / grid_size)
    py5.rect(barrier_x, axis_y, barrier_w, -150)
    
    with lock:
        current_wave = list(prob_density_vector)
        
    if len(current_wave) > 0 and server_connected:
        py5.stroke(0, 255, 200, 240)
        py5.stroke_weight(3)
        py5.no_fill()
        
        py5.begin_shape()
        for i in range(len(current_wave)):
            px = i * (py5.width / grid_size)
            py = axis_y - current_wave[i] * 120000.0
            py5.vertex(px, py)
        py5.end_shape()
        
    # HUD Forense
    py5.fill(255, 50, 100)
    py5.text("🔒 SPHY DISTRIBUTED ENGINE — BINARY STREAM DECODER", 30, 50)
    py5.fill(240, 240, 250)
    py5.text(f" 🌐 Node Gateway : Oracle Cloud Infrastructure (Port 1113/tunnel)", 30, 75)
    py5.text(f" 🔑 Hash Security: SHA-256 ENCRYPTED OCTET-STREAM", 30, 100)
    
    if server_connected:
        py5.fill(0, 255, 200)
        py5.text(" ✨ Connection    : PACKET CAPTURED [DETERMINISTIC BINARY OK]", 30, 125)
    else:
        py5.fill(255, 26, 26)
        py5.text(" 🚨 Connection    : BUFFER COHERENCE CRASH / LINK DOWN", 30, 125)

py5.run_sketch()