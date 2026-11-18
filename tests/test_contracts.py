import pytest
from core.contracts.events import MarketEvent
from core.contracts.signals import Signal
from core.validation.contracts import validate_market_event, validate_signal_contract

def test_valid_market_event():
    event = MarketEvent(event_type="TICK", symbol="BTCUSD", timestamp="2026-09-10T19:00:00Z", payload={"price": 60000.0})
    validate_market_event(event)
    assert True

def test_invalid_market_event():
    event = MarketEvent(event_type="", symbol="BTCUSD", timestamp="2026-09-10T19:00:00Z", payload=None)
    with pytest.raises(ValueError):
        validate_market_event(event)

def test_valid_signal_contract():
    signal = Signal(symbol="ETHUSD", direction="BUY", confidence=0.85, timestamp="2026-09-10T19:00:00Z", timeframe="1h")
    validate_signal_contract(signal)
    assert True

def test_invalid_signal_confidence():
    signal = Signal(symbol="ETHUSD", direction="BUY", confidence=1.5, timestamp="2026-09-10T19:00:00Z", timeframe="1h")
    with pytest.raises(ValueError):
        validate_signal_contract(signal)
