#!/usr/bin/env bash
# ==============================================================================
# KRONOS ROTATION ENGINE v13.5 - FORENSIC FILE SYSTEM PURGE
# ROTACIÓN DE BITÁCORAS DE AUDITORÍA: CONSERVACIÓN DE LAS 3 MÁS RECIENTES
# AUTORÍA REGISTRADA: DIRECTOR MARCO ANTONIO ROJAS VALDOVINOS (TOLUCA DE LERDO)
# ==============================================================================

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0;0m'

clear
echo -e "${CYAN}◢ NÚCLEO DE ROTACIÓN Y LIMPIEZA KRONOS FORENSICS ◣${NC}"
echo "----------------------------------------------------------------------"

# Buscar reportes log ordenados por fecha de modificación (del más nuevo al más viejo)
REPORTS=($(ls -t KRONOS_AUDIT_REPORT_*.log 2>/dev/null))
TOTAL_REPORTS=${#REPORTS[@]}

echo -e "${BLUE}[SISTEMA]${NC} Bitácoras históricas localizadas: $TOTAL_REPORTS"

if [ "$TOTAL_REPORTS" -le 3 ]; then
    echo -e "${GREEN}[CONFORME]${NC} El volumen de logs se encuentra en el rango permitido (<= 3). No se requiere purga."
    exit 0
fi

echo -e "${YELLOW}[ADVERTENCIA]${NC} Exceso de almacenamiento detectado. Reteniendo las 3 bitácoras más recientes..."
echo "----------------------------------------------------------------------"

# Iterar sobre los reportes excedentes a partir del índice 3
for ((i=3; i<TOTAL_REPORTS; i++)); do
    FILE_TO_REMOVE="${REPORTS[i]}"
    echo -e "${YELLOW}[PURGANDO]${NC} Destruyendo registro obsoleto de forma segura: $FILE_TO_REMOVE"
    rm -f "$FILE_TO_REMOVE"
done

echo "----------------------------------------------------------------------"
echo -e "${GREEN}◢ OPERACIÓN DE ROTACIÓN CONCLUIDA ◣${NC}"
echo -e "${GREEN}[INFO]${NC} Espacio en disco optimizado correctamente en el repositorio."
exit 0
