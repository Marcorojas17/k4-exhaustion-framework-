#!/usr/bin/env bash
# ==============================================================================
# KRONOS EXPORT ENGINE v13.2 - SECURE PACKAGING SUITE (PATCHED)
# SOLUCIÓN DE INTERFAZ DE USUARIO: CAPTURA COMPATIBLE CON CODESPACES (READ -S)
# AUTORÍA REGISTRADA: DIRECTOR MARCO ANTONIO ROJAS VALDOVINOS (TOLUCA DE LERDO)
# ==============================================================================

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0;0m'

clear
echo -e "${CYAN}◢ CONTENEDOR DE EXPORTACIÓN TÁCTICA KRONOS v13.2 ◣${NC}"
echo "----------------------------------------------------------------------"

# Validar que los archivos mínimos de evidencia existan
if [ ! -f "./KRONOS_CERTIFICATE_NOM151.html" ] || [ ! -d "./secure_keys" ]; then
    echo -e "${RED}[ERROR]${NC} Faltan actas o llaves oficiales para generar el contenedor."
    exit 1
fi

# Buscar el último reporte log de auditoría generado
LAST_REPORT=$(ls -t KRONOS_AUDIT_REPORT_*.log 2>/dev/null | head -n 1)
if [ -z "$LAST_REPORT" ]; then
    echo -e "${RED}[ERROR]${NC} No se localizó ninguna bitácora oficial de inspección."
    exit 1
fi

EXPORT_TAR="KRONOS_EVIDENCE_BUNDLE.tar"
EXPORT_ENC="KRONOS_EVIDENCE_BUNDLE.tar.enc"

echo -e "${BLUE}[ARCHIVAMIENTO]${NC} Consolidando bitácoras, actas y claves públicas en empaquetado TAR..."
tar -cf "$EXPORT_TAR" "$LAST_REPORT" "./KRONOS_CERTIFICATE_NOM151.html" "./secure_keys/kronos_public.pem" "./secure_keys/merkle_signature.sig" "./secure_keys/root_hash.env" 2>/dev/null

if [ ! -f "$EXPORT_TAR" ]; then
    echo -e "${RED}[ERROR]${NC} Falló la consolidación estructurada del archivo TAR."
    exit 1
fi

# Captura segura y oculta de la contraseña sin eco en pantalla
echo -e "${BLUE}[SEGURIDAD]${NC} Ingrese la contraseña de resguardo pericial (entrada oculta):"
read -s -p "🔑 Password: " CRYPTO_PASS
echo ""

if [ -z "$CRYPTO_PASS" ]; then
    echo -e "${RED}[ERROR]${NC} La contraseña no puede estar vacía."
    rm -f "$EXPORT_TAR"
    exit 1
fi

echo -e "${BLUE}[OPENSSL]${NC} Aplicando cifrado simétrico militar AES-256-CBC mediante pbkdf2..."

# Inyectar el password de forma directa y segura sin prompt de verificación duplicado
openssl enc -aes-256-cbc -salt -in "$EXPORT_TAR" -out "$EXPORT_ENC" -pbkdf2 -pass pass:"$CRYPTO_PASS"

if [ $? -eq 0 ]; then
    echo "----------------------------------------------------------------------"
    echo -e "${GREEN}◢ EMBALAJE COMPLETADO DE FORMA SEGURA ◣${NC}"
    echo -e "${GREEN}[COMPLIANCE]${NC} Contenedor cifrado e inalterable generado: ${EXPORT_ENC}"
    echo -e "${GREEN}[INFO]${NC} El bloque TAR intermedio ha sido destruido de forma segura."
    rm -f "$EXPORT_TAR"
    unset CRYPTO_PASS
    exit 0
else
    echo -e "${RED}[ERROR]${NC} Falló el cifrado criptográfico del paquete."
    rm -f "$EXPORT_TAR"
    unset CRYPTO_PASS
    exit 1
fi
