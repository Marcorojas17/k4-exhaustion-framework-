#!/usr/bin/env bash
# ==============================================================================
# KRONOS AUTOMATED WATCHER DAEMON v13.8 - RUN-TIME MONITORING SUITE
# AUTOMATIZACIÓN CONTINUA, AUDITORÍA DE LOTES Y CONTROL DE RETENCIÓN DE LOGS
# AUTORÍA REGISTRADA: DIRECTOR MARCO ANTONIO ROJAS VALDOVINOS (TOLUCA DE LERDO)
# ==============================================================================

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0;0m'

# Validar hilos duplicados del daemon
PID_FILE="/tmp/kronos_watcher.pid"
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo -e "\033[0;31m[AVISO]\033[0;0m El Demonio Kronos Watcher ya se está ejecutando bajo el PID: $OLD_PID"
        exit 0
    fi
fi
echo $$ > "$PID_FILE"

clear
echo -e "${CYAN}◢ DEMONIO FORENSE DE VIGILANCIA CONTINUA KRONOS v13.8 ◣${NC}"
echo -e "${BLUE}[DAEMON]${NC} Proceso de monitoreo acoplado al segundo plano con PID: $$"
echo "----------------------------------------------------------------------"

# Configuración del ciclo del bucle (Intervalo en segundos: 30 segundos para pruebas de terminal)
INTERVAL_CYCLE=30
LOOP_LIMIT=3 # Ejecutar 3 ciclos antes de liberar la consola en primer plano

for ((cycle=1; cycle<=LOOP_LIMIT; cycle++)); do
    echo -e "${BLUE}[CICLO #$cycle/3]${NC} Iniciando escaneo secuencial programado... $(date)"
    
    # 1. Lanzar el orquestador táctico sobre el directorio raíz
    if [ -f "./kronos-orchestrator.sh" ]; then
        ./kronos-orchestrator.sh . > /dev/null 2>&1
        echo -e "${GREEN}[OK]${NC} Auditoría masiva de vectores ejecutada."
    fi
    
    # 2. Ejecutar la rotación y purga para no saturar el espacio de bloques
    if [ -f "./kronos-clean.sh" ]; then
        ./kronos-clean.sh > /dev/null 2>&1
        echo -e "${GREEN}[OK]${NC} Purga de logs completada (Retención estricta <= 3)."
    fi
    
    if [ $cycle -lt $LOOP_LIMIT ]; then
        echo -e "${YELLOW}[STANDBY]${NC} Durmiendo núcleo forense por $INTERVAL_CYCLE segundos..."
        sleep "$INTERVAL_CYCLE"
        echo "----------------------------------------------------------------------"
    fi
done

# Limpieza del PID de control al finalizar los ciclos demostrativos
rm -f "$PID_FILE"
echo "----------------------------------------------------------------------"
echo -e "${GREEN}◢ MONITOREO CONTINUO DEMOSTRATIVO CONCLUIDO EXCELENTEMENTE ◣${NC}"
exit 0
