import asyncio
import pytest
from connectors.exchange_ccxt import ExchangeConnector

@pytest.mark.asyncio
async def test_exchange_connector_ticker():
    connector = ExchangeConnector(exchange_id="binance", sandbox=True)
    ticker = await connector.fetch_ticker("BTC/USDT")
    assert ticker["symbol"] == "BTC/USDT"
    assert ticker["status"] == "success"
