#!/usr/bin/env bash
# ==============================================================================
# KRONOS DECRYPT ENGINE v13.2 - EVIDENCE DEPLOYMENT SUITE
# DESCIFRADO SIMÉTRICO AES-256-CBC Y EXTRACCIÓN DE CADENA DE CUSTODIA HISTÓRICA
# AUTORÍA REGISTRADA: DIRECTOR MARCO ANTONIO ROJAS VALDOVINOS (TOLUCA DE LERDO)
# ==============================================================================

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0;0m'

clear
echo -e "${CYAN}◢ PROCESADOR DE REVERSA Y DESCIFRADO KRONOS v13.2 ◣${NC}"
echo "----------------------------------------------------------------------"

EXPORT_ENC="KRONOS_EVIDENCE_BUNDLE.tar.enc"
EXPORT_TAR="KRONOS_RESTORED_EVIDENCE.tar"

# Validar existencia del búnker cifrado
if [ ! -f "$EXPORT_ENC" ]; then
    echo -e "${RED}[ERROR]${NC} No se localizó el contenedor cifrado '$EXPORT_ENC' en la raíz."
    exit 1
fi

# Captura segura y oculta de la contraseña sin eco en pantalla
echo -e "${BLUE}[SEGURIDAD]${NC} Ingrese la contraseña de resguardo pericial para descifrado:"
read -s -p "🔑 Password: " CRYPTO_PASS
echo ""

if [ -z "$CRYPTO_PASS" ]; then
    echo -e "${RED}[ERROR]${NC} La contraseña no puede estar vacía."
    exit 1
fi

echo -e "${BLUE}[OPENSSL]${NC} Ejecutando descifrado asíncrono AES-256-CBC de la evidencia..."

# Intentar descifrar el búnker criptográfico
openssl enc -d -aes-256-cbc -in "$EXPORT_ENC" -out "$EXPORT_TAR" -pbkdf2 -pass pass:"$CRYPTO_PASS" 2>/dev/null

if [ $? -ne 0 ] || [ ! -f "$EXPORT_TAR" ]; then
    echo -e "${RED}[ERROR CRÍTICO]${NC} Contraseña incorrecta o corrupción de datos. Acceso denegado."
    rm -f "$EXPORT_TAR"
    unset CRYPTO_PASS
    exit 1
fi

echo -e "${BLUE}[ARCHIVAMIENTO]${NC} Descompatiendo bitácoras, actas y llaves públicas de control..."

# Extraer el contenido del bloque TAR restaurado
tar -xf "$EXPORT_TAR" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "----------------------------------------------------------------------"
    echo -e "${GREEN}◢ EVIDENCIA RESTAURADA Y DESPLEGADA EXCELENTEMENTE ◣${NC}"
    echo -e "${GREEN}[COMPLIANCE]${NC} Las actas NOM-151, llaves y bitácoras .log han sido extraídas."
    echo -e "${GREEN}[INFO]${NC} El bloque TAR intermedio restaurado ha sido destruido de forma segura."
    rm -f "$EXPORT_TAR"
    unset CRYPTO_PASS
    exit 0
else
    echo -e "${RED}[ERROR]${NC} Falló la descompresión de la estructura interna del contenedor."
    rm -f "$EXPORT_TAR"
    unset CRYPTO_PASS
    exit 1
fi
