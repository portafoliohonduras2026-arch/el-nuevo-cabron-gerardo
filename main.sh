#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

BASE_DIR="/data/data/com.termux/files/home/el-nuevo-cabron-gerardo"
LOG_DIR="${BASE_DIR}/logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
LOG_FILE="${LOG_DIR}/bot_${TIMESTAMP//[:]/-}.log"

cd "$BASE_DIR"

while true; do
    echo "[$(date -u)] Lanzando ciclo del bot de trading..." | tee -a "$LOG_FILE"
    
    if python3 -c "from core.engine import Engine; print('Motor OK')" >> "$LOG_FILE" 2>&1; then
        echo "[$(date -u)] Ciclo ejecutado con éxito." | tee -a "$LOG_FILE"
    else
        MSG="[ALERTA] Caída detectada en el ciclo de El nuevo cabrón Gerardo."
        echo "[$(date -u)] $MSG" | tee -a "$LOG_FILE"
        python3 -c "from connectors.notifier import TelegramNotifier; TelegramNotifier().send_alert('$MSG')" >> "$LOG_FILE" 2>&1 || true
    fi

    sleep 10
done
