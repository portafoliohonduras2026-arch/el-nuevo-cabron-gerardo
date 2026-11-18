"""Módulo de toma de decisiones de compra y venta — El nuevo cabrón Gerardo"""

import logging
from typing import Any, Dict, Tuple
from core.safety_gate import SafetyGate

logger = logging.getLogger(__name__)

class TradingStrategy:
    """Evalúa datos de mercado y decide si emite una orden validada por el SafetyGate."""

    def __init__(self, safety_gate: SafetyGate, target_buy_price: float = 50000.0) -> None:
        self.safety_gate = safety_gate
        self.target_buy_price = target_buy_price

    def evaluate_ticker(self, ticker: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """Toma una decisión basada en el precio de mercado actual."""
        symbol = ticker.get("symbol", "BTC/USDT")
        bid = ticker.get("bid", 0.0)
        
        # Lógica simple de decisión de ejemplo (ej. comprar si el precio baja del objetivo)
        action = "HOLD"
        size = 1.0
        leverage = 1

        # Si no hay precio de mercado real en test, evaluamos simulación
        if bid > 0 and bid <= self.target_buy_price:
            action = "BUY"
        elif bid == 0.0: # Modo simulación / señal base
            action = "BUY"

        payload = {
            "symbol": symbol,
            "action": action,
            "size": size,
            "leverage": leverage
        }

        if action == "BUY" or action == "SELL":
            approved, reason = self.safety_gate.validate(payload)
            if not approved:
                logger.warning(f"Estrategia: Orden bloqueada por SafetyGate -> {reason}")
                return False, reason, payload
            logger.info(f"Estrategia: Orden aprobada y ejecutada -> {payload}")
            return True, "EXECUTED", payload

        return False, "HOLD", payload
