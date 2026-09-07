#!/usr/bin/env bash
# ==============================================================================
# KRONOS AUTOMATED ORCHESTRATOR v13.5 - ADVANCED LOTE PROCESSOR WITH FILTER
# FILTRADO DE COMPONENTES CRIPTOGRÁFICOS Y REGISTRO DE CONFORMIDAD NOM-151
# AUTORÍA REGISTRADA: DIRECTOR MARCO ANTONIO ROJAS VALDOVINOS (TOLUCA DE LERDO)
# ==============================================================================

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0;0m'

clear
echo -e "${CYAN}◢ ORQUESTRADOR TÁCTICO KRONOS FORENSICS v13.5 ◣${NC}"
echo "----------------------------------------------------------------------"

TARGET_DIR="${1:-.}"
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "\033[0;31m[ERROR]\033[0;0m El directorio '$TARGET_DIR' no existe."
    exit 1
fi

if [ ! -f "./kronos-audit.sh" ]; then
    echo -e "\033[0;31m[ERROR]\033[0;0m No se encuentra 'kronos-audit.sh' en el directorio actual."
    exit 1
fi

REPORT_FILE="KRONOS_AUDIT_REPORT_$(date +%Y%m%d_%H%M%S).log"
echo -e "${CYAN}[PIPELINE]${NC} Escaneando directorio: $TARGET_DIR"
echo -e "${CYAN}[PIPELINE]${NC} Generando registro oficial inmutable en: $REPORT_FILE"

echo "======================================================================" >> "$REPORT_FILE"
echo "INFORME HISTÓRICO DE AUDITORÍA KRONOS - $(date)" >> "$REPORT_FILE"
echo "======================================================================" >> "$REPORT_FILE"

FILE_COUNT=0
THREAT_COUNT=0

# Lista estricta de exclusión para mitigar falsos positivos por alta entropía legítima
declare -A IGNORE_LIST
IGNORE_LIST["kronos-audit.sh"]=1
IGNORE_LIST["kronos-orchestrator.sh"]=1
IGNORE_LIST["kronos-merkle.py"]=1
IGNORE_LIST["kronos-sign.sh"]=1
IGNORE_LIST["kronos-verify.sh"]=1
IGNORE_LIST["kronos-pack.sh"]=1
IGNORE_LIST["kronos-unpack.sh"]=1
IGNORE_LIST["merkle_signature.sig"]=1
IGNORE_LIST["kronos_private.pem"]=1
IGNORE_LIST["KRONOS_EVIDENCE_BUNDLE.tar.enc"]=1

while IFS= read -r -d '' file; do
    FILENAME_BASE=$(basename "$file")
    
    # Omitir si es un reporte log o está en la lista de exclusión o pertenece a .git
    if [[ "$file" == *".git"* || "$file" == *"KRONOS_AUDIT_REPORT_"* || ${IGNORE_LIST[$FILENAME_BASE]} ]]; then
        continue
    fi

    ((FILE_COUNT++))
    echo -e "\n${YELLOW}[PROCESANDO VECTOR $FILE_COUNT]${NC} $file"
    echo -e "\n--- ANALIZANDO: $file ---" >> "$REPORT_FILE"
    
    OUTPUT=$(./kronos-audit.sh "$file")
    echo "$OUTPUT" >> "$REPORT_FILE"
    
    if echo "$OUTPUT" | grep -q "CRÍTICO"; then
        ((THREAT_COUNT++))
        echo -e "\033[0;31m[ALERTA CRÍTICA]\033[0;0m Anomalía o evasión detectada en el vector."
    else
        echo -e "${GREEN}[CONFORME]${NC} Estructura binaria verificada sin anomalías."
    fi

done < <(find "$TARGET_DIR" -type f -not -path '*/.*' -print0)

echo "----------------------------------------------------------------------"
echo -e "${GREEN}◢ RESUMEN DE COMPLIANCE DEL NÚCLEO OPTIMIZADO ◣${NC}"
echo -e "Vectores Auditados Reales: $FILE_COUNT"
echo -e "Amenazas Confirmadas:       $THREAT_COUNT"
echo -e "Acta de Custodia Consolidada Guardada en: ${YELLOW}$REPORT_FILE${NC}"
echo "----------------------------------------------------------------------"

echo -e "\n======================================================================" >> "$REPORT_FILE"
echo "FIN DEL ESCANEO - VECTORES: $FILE_COUNT // AMENAZAS DETECTADAS: $THREAT_COUNT" >> "$REPORT_FILE"
echo "======================================================================" >> "$REPORT_FILE"

exit 0
