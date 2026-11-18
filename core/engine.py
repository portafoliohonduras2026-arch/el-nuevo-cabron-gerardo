"""Bucle de eventos con aislamiento de errores por señal."""

import asyncio
import inspect
import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)
_STOP = object()


class Engine:
    """Recibe señales y las entrega a un manejador sin ejecutar órdenes."""

    def __init__(
        self,
        handler: Callable[[dict[str, Any]], Any],
        max_queue_size: int = 100,
    ) -> None:
        self._handler = handler
        self._queue: asyncio.Queue[object] = asyncio.Queue(
            maxsize=max_queue_size
        )
        self._stopping = False
        self._running = False

    async def submit(self, payload: object) -> bool:
        """Encola un objeto tipo diccionario; devuelve False si se rechaza."""
        if self._stopping:
            logger.warning("Señal descartada: el motor está deteniéndose")
            return False

        if not isinstance(payload, dict):
            logger.warning("Señal descartada: la carga no es un diccionario")
            return False

        try:
            self._queue.put_nowait(payload)
            return True
        except asyncio.QueueFull:
            logger.warning("Señal descartada: cola llena")
            return False
        except Exception:
            logger.exception("Error al encolar una señal")
            return False

    async def run(self) -> None:
        """Procesa la cola; un error de señal no detiene las siguientes."""
        if self._running:
            logger.warning("El motor ya está en ejecución")
            return

        self._running = True
        logger.info("Motor iniciado")

        try:
            while True:
                payload = await self._queue.get()
                try:
                    if payload is _STOP:
                        break

                    result = self._handler(payload)
                    if inspect.isawaitable(result):
                        await result
                except asyncio.CancelledError:
                    logger.info("Cancelación solicitada al motor")
                    raise
                except Exception:
                    logger.exception("Error aislado al procesar una señal")
                finally:
                    self._queue.task_done()
        except asyncio.CancelledError:
            logger.info("Bucle del motor cancelado")
            raise
        except Exception:
            logger.exception("Fallo inesperado en el bucle del motor")
        finally:
            self._running = False
            logger.info("Motor detenido")

    async def stop(self) -> None:
        """Pide al bucle que termine después de procesar lo pendiente."""
        if self._stopping:
            return

        self._stopping = True
        try:
            await self._queue.put(_STOP)
        except Exception:
            logger.exception("Error al solicitar el cierre del motor")
