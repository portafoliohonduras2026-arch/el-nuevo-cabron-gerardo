#!/data/data/com.termux/files/usr/bin/bash

# Script de Supervisión Continua — El nuevo cabrón Gerardo
# Protocolo: Capturar → Registrar → Aislar → Continuar

set -euo pipefail

BASE_DIR="/data/data/com.termux/files/home/el-nuevo-cabron-gerardo"
LOG_DIR="${BASE_DIR}/logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
LOG_FILE="${LOG_DIR}/bot_${TIMESTAMP//[:]/-}.log"

echo "=== Iniciando Supervisor de El nuevo cabrón Gerardo ===" | tee -a "$LOG_FILE"
echo "Directorio base: $BASE_DIR" | tee -a "$LOG_FILE"

cd "$BASE_DIR"

while true; do
    echo "[$(date -u)] Lanzando ciclo del bot de trading..." | tee -a "$LOG_FILE"
    
    # Ejecución controlada del motor principal (o loop de prueba inicial)
    if python3 -c "from core.engine import Engine; print('Motor OK')" >> "$LOG_FILE" 2>&1; then
        echo "[$(date -u)] Ciclo ejecutado con éxito." | tee -a "$LOG_FILE"
    else
        echo "[$(date -u)] [ALERTA] El motor sufrió una anomalía. Aislando y continuando..." | tee -a "$LOG_FILE"
    fi

    echo "[$(date -u)] Pausa de 10 segundos antes del siguiente ciclo..." | tee -a "$LOG_FILE"
    sleep 10
done
