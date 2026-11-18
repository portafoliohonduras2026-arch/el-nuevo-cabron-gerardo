"""Compuerta de Riesgo Local (SafetyGate) — El nuevo cabrón Gerardo"""

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)

class SafetyGate:
    """Valida los límites de riesgo, apalancamiento y esquemas antes de ejecutar."""

    def __init__(
        self,
        allowed_symbols: list[str],
        max_leverage: int = 5,
        max_position_size: float = 100.0,
        kill_switch: bool = False,
    ) -> None:
        self.allowed_symbols = set(allowed_symbols)
        self.max_leverage = max_leverage
        self.max_position_size = max_position_size
        self.kill_switch = kill_switch

    def validate(self, payload: Dict[str, Any]) -> Tuple[bool, str]:
        """Evalúa una señal contra las reglas de riesgo. Devuelve (aprobado, motivo)."""
        if self.kill_switch:
            logger.warning("SafetyGate RECHAZADO: Kill-switch global activado.")
            return False, "KILL_SWITCH_ACTIVE"

        symbol = payload.get("symbol")
        if not symbol or symbol not in self.allowed_symbols:
            logger.warning(f"SafetyGate RECHAZADO: Símbolo inválido o no permitido -> {symbol}")
            return False, "INVALID_SYMBOL"

        leverage = payload.get("leverage", 1)
        if not isinstance(leverage, (int, float)) or leverage > self.max_leverage or leverage < 1:
            logger.warning(f"SafetyGate RECHAZADO: Apalancamiento fuera de rango -> {leverage}")
            return False, "LEVERAGE_OUT_OF_BOUNDS"

        size = payload.get("size", 0.0)
        if not isinstance(size, (int, float)) or size <= 0 or size > self.max_position_size:
            logger.warning(f"SafetyGate RECHAZADO: Tamaño de posición inválido -> {size}")
            return False, "INVALID_POSITION_SIZE"

        logger.info(f"SafetyGate APROBADO: {symbol} | Apalancamiento: {leverage}x | Tamaño: {size}")
        return True, "APPROVED"
