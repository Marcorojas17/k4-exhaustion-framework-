import os
import sys
import json
import asyncio
import numpy as np

K4 = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
KRYPTOS_ALPHABET = "KRYPTOSABCDEFGHIJLMNQUVWXZ"

k4_numeric = np.array([KRYPTOS_ALPHABET.index(c) for c in K4], dtype=np.int32)
berlin_vec = np.array([KRYPTOS_ALPHABET.index(c) for c in "BERLIN"], dtype=np.int32)
clock_vec = np.array([KRYPTOS_ALPHABET.index(c) for c in "CLOCK"], dtype=np.int32)
all_shifts = np.arange(26, dtype=np.int32).reshape(26, 1)

def col_unshuffle_numpy(arr_numeric, rows=4, cols=25):
    m = np.zeros((rows, cols), dtype=np.int32)
    idx = 0
    for c in range(cols):
        for r in range(rows):
            if idx < len(arr_numeric):
                m[r, c] = arr_numeric[idx]
                idx += 1
    return m.flatten()[:len(arr_numeric)]

def run_autokey_decay(numeric_text, priming_key):
    plaintext = np.zeros(len(numeric_text), dtype=np.int32)
    current_key = list(priming_key)
    for i in range(len(numeric_text)):
        c_val = numeric_text[i]
        k_val = current_key[i]
        p_val = (c_val - k_val) % 26
        plaintext[i] = p_val
        if i % 2 == 0:
            current_key.append(p_val)
        else:
            current_key.append(c_val)
    return plaintext

async def quantum_stream_server():
    import websockets
    print("=========================================================")
    print("🧬 KRONOS LIVE SERVER - TRANSMITIENDO PIPELINE COMBO [8765]")
    print("=========================================================")
    
    k4_unshuffled = col_unshuffle_numpy(k4_numeric, 4, 25)
    priming_options = ["KRYP", "BERL", "CLOC", "PALI", "EDSCH", "SCHEIDT"]

    async def handler(websocket):
        print("[+] Interfaz web KRONOS enlazada de forma remota.")
        try:
            for p_str in priming_options:
                priming_key = [KRYPTOS_ALPHABET.index(c) for c in p_str]
                base_decrypted = run_autokey_decay(k4_unshuffled, priming_key)
                matrix_decrypted = (base_decrypted - all_shifts) % 26
                
                for shift in range(26):
                    row_text = matrix_decrypted[shift]
                    for pos in range(len(row_text) - 5):
                        # Validación para BERLIN
                        if np.sum(row_text[pos:pos+6] == berlin_vec) >= 4:
                            text_str = "".join([KRYPTOS_ALPHABET[x] for x in row_text])
                            payload = {"msg": f"COMBO HIT BERLIN ({np.sum(row_text[pos:pos+6]==berlin_vec)}/6) Priming:{p_str} Shift:{shift} -> {text_str[:40]}..."}
                            await websocket.send(json.dumps(payload))
                            await asyncio.sleep(0.05)
                        
                        # Validación para CLOCK
                        if pos < len(row_text) - 4 and np.sum(row_text[pos:pos+5] == clock_vec) >= 4:
                            text_str = "".join([KRYPTOS_ALPHABET[x] for x in row_text])
                            payload = {"msg": f"COMBO HIT CLOCK ({np.sum(row_text[pos:pos+5]==clock_vec)}/5) Priming:{p_str} Shift:{shift} -> {text_str[:40]}..."}
                            await websocket.send(json.dumps(payload))
                            await asyncio.sleep(0.05)
            print("[+] Transmisión de hits del pipeline finalizada.")
        except websockets.exceptions.ConnectionClosed:
            pass

    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        import websockets
    except ImportError:
        os.system("pip install websockets")
    asyncio.run(quantum_stream_server())
