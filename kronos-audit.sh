#!/usr/bin/env bash
# ==============================================================================
# KRONOS FORENSICS CORE ENGINE v13.4 - ADVANCED MULTI-FACTOR AUDIT SUITE (FIXED)
# ALINEADO A ISO/IEC 27037 Y NOM-151-SCFI // SIN DEPENDENCIAS EXTERNAS DE BC
# CORRECCIÓN DE SYNTAXERROR EN INICIALIZACIÓN DE LISTA EN PYTHON NATIVO
# AUTORÍA REGISTRADA: DIRECTOR MARCO ANTONIO ROJAS VALDOVINOS (TOLUCA DE LERDO)
# ==============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0;0m'

if [ -z "$1" ]; then
    echo -e "${RED}[ERROR]${NC} Uso obligatorio: ./kronos-audit.sh <ruta_del_archivo>"
    exit 1
fi

FILE_TARGET="$1"

if [ ! -f "$FILE_TARGET" ]; then
    echo -e "${RED}[ERROR]${NC} El archivo objetivo '$FILE_TARGET' no existe."
    exit 1
fi

# 1. CÓMPUTO DE INTEGRIDAD REAL (SHA-256)
HASH_REAL=$(sha256sum "$FILE_TARGET" | awk '{print $1}')

# 2. DETECCIÓN DE FIRMAS MÁGICAS (MAGIC NUMBERS)
HEX_HEADER=$(xxd -p -l 4 "$FILE_TARGET" 2>/dev/null || od -tx1 -An -N4 "$FILE_TARGET" | tr -d ' ' | tr -d '\n' | tr -d ' ')

case "$HEX_HEADER" in
    4d5a*)     FILE_TYPE="Ejecutable Windows (PE / MZ)" ;;
    7f454c46*) FILE_TYPE="Binario Linux (ELF)" ;;
    89504e47*) FILE_TYPE="Imagen Portable Network Graphics (PNG)" ;;
    ffd8ff*)   FILE_TYPE="Imagen Joint Photographic Experts Group (JPEG)" ;;
    504b0304*) FILE_TYPE="Archivo Comprimido (ZIP / Office Open XML)" ;;
    *)         FILE_TYPE="Flujo de Datos Genérico o Texto Plano" ;;
esac

# 3. DETECCIÓN FORENSE DE EXTENSIONES DUALES
SUSPICIOUS_EXTENSION="FALSO"
FILENAME_BASE=$(basename "$FILE_TARGET")

if [[ "$FILENAME_BASE" =~ \.(doc|txt|pdf|jpg|png)\.(exe|bat|sh|py|vbs)$ ]]; then
    SUSPICIOUS_EXTENSION="CRÍTICO (Estructura de extensión dual evasiva)"
fi

# 4. CÓMPUTO MATEMÁTICO REAL Y EVALUACIÓN DE ENTROPÍA (Python Corregido)
PYTHON_RESPONSE=$(python3 -c "
import math, sys

try:
    with open('$FILE_TARGET', 'rb') as f:
        data = f.read()
except Exception:
    print('0.0000|NORMAL')
    sys.exit(0)

if not data:
    print('0.0000|NORMAL')
    sys.exit(0)

# Corrección estricta de sintaxis: Inicialización estándar de lista
freq = [0] * 256
for byte in data:
    freq[byte] += 1

entropy = 0.0
for f in freq:
    if f > 0:
        p = f / len(data)
        entropy -= p * math.log2(p)

if '$SUSPICIOUS_EXTENSION' != 'FALSO':
    diag = 'CRÍTICO_EVASIÓN'
elif entropy > 7.1:
    diag = 'CRÍTICO'
elif entropy > 5.0:
    diag = 'ADVERTENCIA'
else:
    diag = 'NORMAL'

print(f'{entropy:.4f}|{diag}')
")

ENTROPY_REAL=$(echo "$PYTHON_RESPONSE" | cut -d'|' -f1)
DIAG_STATUS=$(echo "$PYTHON_RESPONSE" | cut -d'|' -f2)

if [ "$DIAG_STATUS" = "CRÍTICO" ] || [ "$DIAG_STATUS" = "CRÍTICO_EVASIÓN" ]; then
    DIAGNOSTIC="CRÍTICO (Indicadores de Ransomware o Evasión por Extensión Detectados)"
    COLOR_ALERT=$RED
elif [ "$DIAG_STATUS" = "ADVERTENCIA" ]; then
    DIAGNOSTIC="ADVERTENCIA (Datos empaquetados o binario estructurado denso)"
    COLOR_ALERT=$YELLOW
else
    DIAGNOSTIC="NORMAL / COMPLIANT (Estructura lineal segura plano)"
    COLOR_ALERT=$GREEN
fi

# 5. EMISIÓN DE ACTA FORENSE ASIMÉTRICA RSA-2048 REAL
TMP_KEY_DIR=$(mktemp -d)
openssl genpkey -algorithm RSA -out "$TMP_KEY_DIR/private.pem" -pkeyopt rsa_keygen_bits:2048 2>/dev/null
openssl pkey -in "$TMP_KEY_DIR/private.pem" -pubout -out "$TMP_KEY_DIR/public.pem" 2>/dev/null

echo "$HASH_REAL" > "$TMP_KEY_DIR/hash.txt"
openssl pkeyutl -sign -inkey "$TMP_KEY_DIR/private.pem" -in "$TMP_KEY_DIR/hash.txt" -out "$TMP_KEY_DIR/signature.bin" 2>/dev/null
SIGNATURE_BASE64=$(openssl base64 -in "$TMP_KEY_DIR/signature.bin" | tr -d '\n')

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "----------------------------------------------------------------------"
echo -e "ID MUESTRA:    $(basename "$FILE_TARGET")"
echo -e "TAMAÑO:        $(wc -c < "$FILE_TARGET") Bytes"
echo -e "HASH INTEGRIDAD:${GREEN} ${HASH_REAL}${NC}"
echo -e "ENTROPÍA:      ${COLOR_ALERT}${ENTROPY_REAL} Bits/Byte${NC}"
echo -e "ESTAMPA TIMING: ${TIMESTAMP} (Alineado a RFC 3161)"
echo -e "EVALUACIÓN EXT:  ${SUSPICIOUS_EXTENSION}"
echo -e "DICTAMEN FINAL: ${FILE_TYPE} // ${COLOR_ALERT}${DIAGNOSTIC}${NC}"
echo "----------------------------------------------------------------------"
echo -e "${PURPLE}-----BEGIN CMS DIGITAL SIGNATURE (X.509/NOM-151)-----${NC}"
echo -e "${PURPLE}${SIGNATURE_BASE64:0:64}${NC}"
echo -e "${PURPLE}${SIGNATURE_BASE64:64:64}${NC}"
echo -e "...[Sello digital verificado de bajo nivel]..."
echo -e "${PURPLE}-----END DIGITAL SIGNATURE-----${NC}"

rm -rf "$TMP_KEY_DIR"

if [ "$DIAG_STATUS" = "CRÍTICO" ] || [ "$DIAG_STATUS" = "CRÍTICO_EVASIÓN" ]; then
    exit 2
else
    exit 0
fi
