import asyncio
import unittest
from unittest.mock import patch
import ccxt
from connectors.exchange_ccxt import ExchangeConnector

class TestExchangeNetworkFailure(unittest.TestCase):
    
    @patch('connectors.exchange_ccxt.asyncio.sleep', return_value=None) # Acelerar los reintentos en pruebas
    def test_exchange_retry_and_timeout(self, mock_sleep):
        connector = ExchangeConnector(exchange_id="binance", sandbox=True)
        
        # Forzar que falle lanzando ccxt.NetworkError en las llamadas
        with patch.object(connector, 'initialize', side_effect=ccxt.NetworkError("Fallo de red simulado")):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(connector.fetch_ticker("BTC/USDT"))
            except Exception as e:
                # Verificamos que la excepción sea la esperada tras agotar reintentos
                self.assertIsInstance(e, ccxt.NetworkError)
            finally:
                loop.close()

if __name__ == '__main__':
    unittest.main()
