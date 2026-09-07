# src/data/generate_ngrams.py
import os
import pickle
import math

def build_linguistic_ngrams(output_path=None):
    """
    Genera y compila el mapa de calor probabilístico de n-gramas (bigramas y trigramas)
    del inglés. Calcula sus log-probabilidades para alimentar la poda temprana.
    """
    if output_path is None:
        # Resolver ruta por defecto en src/data/ngrams.bin
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(current_dir, "ngrams.bin")

    print(f"[*] Inicializando base de conocimiento lingüística en: {output_path}")

    # Muestra estadística de alta frecuencia extraída de corpus militares y literarios estándar
    # Formato: n-grama -> Recuento relativo ponderado
    bigrams_source = {
        "TH": 3560, "HE": 3070, "IN": 2430, "ER": 2050, "AN": 1990, "RE": 1850,
        "ON": 1760, "AT": 1490, "EN": 1450, "ES": 1340, "OF": 1170, "OR": 1150,
        "NT": 1140, "EA": 1100, "TI": 1050, "TO": 1040, "ST": 1000, "ST": 990
    }

    trigrams_source = {
        "THE": 1810, "AND": 730, "THA": 370, "ENT": 350, "ING": 330, "ION": 310,
        "TIO": 270, "FOR": 240, "NDE": 240, "HAS": 230, "NCE": 210, "EDT": 200,
        "TIS": 190, "OFT": 180, "STH": 170, "MEN": 160, "ALL": 150, "BER": 140
    }

    # Transformar recuentos a Log-Probabilidades matemáticas para evitar subdesbordamiento (underflow)
    total_bi = sum(bigrams_source.values())
    total_tri = sum(trigrams_source.values())

    ngrams_database = {
        "bigrams": {ngram: math.log10(count / total_bi) for ngram, count in bigrams_source.items()},
        "trigrams": {ngram: math.log10(count / total_tri) for ngram, count in trigrams_source.items()}
    }

    # Serializar y escribir el binario compacto en el disco duro
    try:
        with open(output_path, "wb") as f:
            pickle.dump(ngrams_database, f, protocol=pickle.HIGHEST_PROTOCOL)
        print("[+] Archivo 'ngrams.bin' compilado y optimizado con éxito.")
    except Exception as e:
        print(f"[!] Error crítico al escribir el diccionario binario: {e}")

if __name__ == "__main__":
    build_linguistic_ngrams()
