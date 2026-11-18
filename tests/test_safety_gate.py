from core.safety_gate import SafetyGate

def test_safety_gate_validation():
    gate = SafetyGate(allowed_symbols=["BTC/USDT", "ETH/USDT"], max_leverage=5, max_position_size=100.0)
    assert gate.validate({"symbol": "BTC/USDT", "leverage": 3, "size": 50.0}) == (True, "APPROVED")
    assert gate.validate({"symbol": "DOGE/USDT", "leverage": 3, "size": 50.0}) == (False, "INVALID_SYMBOL")
    assert gate.validate({"symbol": "BTC/USDT", "leverage": 10, "size": 50.0}) == (False, "LEVERAGE_OUT_OF_BOUNDS")
    assert gate.validate({"symbol": "BTC/USDT", "leverage": 3, "size": 250.0}) == (False, "INVALID_POSITION_SIZE")
    
    gate.kill_switch = True
    assert gate.validate({"symbol": "BTC/USDT", "leverage": 3, "size": 50.0}) == (False, "KILL_SWITCH_ACTIVE")
