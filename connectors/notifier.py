"""Módulo de Alertas en Tiempo Real (Telegram/Webhooks) — El nuevo cabrón Gerardo"""

import os
import logging
import urllib.request
import json
from typing import Optional

logger = logging.getLogger(__name__)

class TelegramNotifier:
    """Envía alertas en tiempo real con manejo estricto de excepciones para no bloquear el bot."""

    def __init__(self, token: Optional[str] = None, chat_id: Optional[str] = None) -> None:
        self.token = token if token is not None else os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = chat_id if chat_id is not None else os.getenv("TELEGRAM_CHAT_ID", "")
        # Validación estricta: deben ser strings no vacíos y distintos de espacios
        self.enabled = bool(self.token.strip() and self.chat_id.strip())
        if not self.enabled:
            logger.warning("TelegramNotifier deshabilitado: Faltan credenciales válidas (TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID).")

    def send_alert(self, message: str) -> bool:
        """Envía un mensaje de alerta de forma síncrona pero protegida ante caídas de red."""
        if not self.enabled:
            logger.debug(f"Alerta omitida (notifier inactivo): {message}")
            return False

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": f"🚨 **ALERTA TRADING BOT** 🚨\n\n{message}",
            "parse_mode": "Markdown"
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url, 
                data=data, 
                headers={"Content-Type": "application/json"}, 
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    logger.info("Alerta enviada con éxito a Telegram.")
                    return True
        except Exception as e:
            logger.error(f"Error al enviar alerta a Telegram: {e}", exc_info=True)
            
        return False
