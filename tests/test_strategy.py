import unittest
from core.safety_gate import SafetyGate
from core.strategy import TradingStrategy

class TestTradingStrategy(unittest.TestCase):
    def setUp(self):
        self.gate = SafetyGate(
            allowed_symbols=["BTC/USDT"],
            max_leverage=3,
            max_position_size=2.0
        )
        self.strategy = TradingStrategy(safety_gate=self.gate)

    def test_strategy_buy_approved(self):
        ticker = {"symbol": "BTC/USDT", "bid": 45000.0}
        success, reason, payload = self.strategy.evaluate_ticker(ticker)
        self.assertTrue(success)
        self.assertEqual(reason, "EXECUTED")
        self.assertEqual(payload["action"], "BUY")

    def test_strategy_rejected_by_safety_gate(self):
        # Forzar un tamaño de posición prohibido por el SafetyGate
        gate = SafetyGate(allowed_symbols=["BTC/USDT"], max_position_size=0.5)
        strategy = TradingStrategy(safety_gate=gate)
        ticker = {"symbol": "BTC/USDT", "bid": 45000.0}
        
        # Modificamos el payload mediante un mock o alterando la lógica si es necesario, 
        # pero aquí probamos con un símbolo no permitido:
        ticker_invalid = {"symbol": "ETH/USDT", "bid": 2000.0}
        success, reason, payload = strategy.evaluate_ticker(ticker_invalid)
        self.assertFalse(success)
        self.assertEqual(reason, "INVALID_SYMBOL")

if __name__ == '__main__':
    unittest.main()
