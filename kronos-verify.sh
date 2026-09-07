#!/usr/bin/env bash
# ==============================================================================
# KRONOS CRYPTO-VERIFY ENGINE v13.1 - FORENSIC AUDIT SUITE
# VALIDACIÓN DE FIRMA DIGITAL CON CLAVE PÚBLICA RSA-2048 (NOM-151 / ISO 27037)
# AUTORÍA REGISTRADA: DIRECTOR MARCO ANTONIO ROJAS VALDOVINOS (TOLUCA DE LERDO)
# ==============================================================================

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0;0m'

clear
echo -e "${CYAN}◢ MÓDULO DE VERIFICACIÓN CRIPTOGRÁFICA KRONOS ◣${NC}"
echo "----------------------------------------------------------------------"

KEY_DIR="./secure_keys"

# Validar la existencia de los componentes mínimos de la cadena
if [ ! -f "$KEY_DIR/kronos_public.pem" ] || [ ! -f "$KEY_DIR/merkle_signature.sig" ] || [ ! -f "$KEY_DIR/root_hash.env" ]; then
    echo -e "${RED}[ERROR]${NC} Faltan elementos esenciales en la bóveda de seguridad '$KEY_DIR'."
    exit 1
fi

echo -e "${BLUE}[AUDITORÍA]${NC} Extrayendo Root Hash firmado originalmente..."
ROOT_HASH_GUARDADO=$(cat "$KEY_DIR/root_hash.env")
echo -e "${CYAN}[METADATA]${NC} Hash bajo análisis: $ROOT_HASH_GUARDADO"

echo -e "${BLUE}[OPENSSL]${NC} Ejecutando validación asimétrica de firma digital PKCS#1..."

# Realizar la verificación matemática real usando la clave pública
VERIFICATION_RESULT=$(openssl dgst -sha256 -verify "$KEY_DIR/kronos_public.pem" -signature "$KEY_DIR/merkle_signature.sig" "$KEY_DIR/root_hash.env" 2>&1)

echo "----------------------------------------------------------------------"
if [[ "$VERIFICATION_RESULT" == *"Verified OK"* ]]; then
    echo -e "${GREEN}◢ VEREDICTO: VERIFICACIÓN CORRECTA ◣${NC}"
    echo -e "${GREEN}[INTEGRIDAD DE LA PRUEBA]${NC} LA FIRMA ES AUTÉNTICA Y CORRESPONDE AL REPOSITORIO."
    echo -e "${GREEN}[COMPLIANCE]${NC} Evidencia digital íntegra e inalterada conforme a NOM-151-SCFI."
    exit 0
else
    echo -e "${RED}◢ VEREDICTO: CADENA CORROMPIDA ◣${NC}"
    echo -e "${RED}[ALERTA DE SEGURIDAD]${NC} LA FIRMA NO COINCIDE O LOS DATOS FUERON ALTERADOS."
    echo -e "${RED}[CUMPLIMIENTO]${NC} Violación a la cadena de custodia (ISO/IEC 27037)."
    exit 2
fi
echo "----------------------------------------------------------------------"
